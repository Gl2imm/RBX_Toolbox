"""
RBX Toolbox Invaders -- a shooter that plays inside Blender's 3D viewport.

The addon's easter egg. Nothing here is drawn until the user clicks the panel
title ten times, at which point menu_ui grows a box with the Play button. The
unlock is a module global on purpose: it dies with the Blender session, so the
egg has to be found again next launch.

    Left / Right arrows  move
    Space                fire
    M                    music on/off
    Esc                  quit

Playing snaps the view to front-orthographic and locks it, hides everything
already in the scene AND every viewport region (N-panel, toolbar, header,
gizmos), and spawns the game objects into their own collection. Quitting puts
all of it back exactly as it was: object visibility, region visibility, the view
matrix, shading mode and overlays are saved on entry and restored on exit.

The front view looks down +Y, so the game is played on the XZ plane: X is
across, Z is up, and everything sits at Y=0.

The HUD is drawn with blf/gpu in a POST_PIXEL draw handler rather than with text
meshes: screen-space text stays crisp, pins to the corners regardless of zoom,
needs no geometry or cleanup, and lets the game-over buttons be hit-tested.

Levels cycle through three casts: RBX Toolbox dummies, Blender primitives, then
arcade bug sprites. The dummy level reads the addon's template .blend; if that
file is missing the level quietly falls back to primitives.

Sound is synthesised at startup with Blender's bundled aud + numpy -- there are
no audio files to ship. If audio is unavailable the game plays silently.
"""

import bpy
import bmesh
import blf
import gpu
import math
import time
import random
from gpu_extras.batch import batch_for_shader
from mathutils import Matrix, Quaternion, Vector

# Blender bundles Audaspace (aud) and numpy, so every sound effect is
# synthesised from scratch at startup -- no .wav files to ship, nothing to
# download, and the script stays paste-and-run. Both are guarded anyway: a
# Blender built without them, or with "Audio Device: None" set in preferences,
# just plays the game silently.
try:
    import aud
except Exception:
    aud = None
try:
    import numpy as np
except Exception:
    np = None

GAME_NAME = "RBX Toolbox Invaders"
COLL_NAME = "RBX_BestFeature"
PREFIX = "RBX_BF"

# --- the unlock ---
# Ten clicks on the panel title. Both counters are plain module globals rather
# than Scene properties or preferences: a Scene property would be written into
# the user's .blend and a preference would survive forever, and the egg is meant
# to be re-found every session. Module state dies with the Blender process,
# which is exactly the requested lifetime.
UNLOCK_CLICKS = 10

_clicks = 0
_unlocked = False


def is_unlocked():
    return _unlocked

# Blender's Text Editor execs this file into a FRESH namespace on every Run, so
# a plain module global can't see a game started by a previous run -- re-running
# mid-game would strand the hidden scene and leave the old modal alive. The
# driver namespace outlives script runs, so the live game is parked there and any
# future run can find and shut it down.
STORE_KEY = "RBX_BEST_FEATURE_ACTIVE"


def get_active():
    return bpy.app.driver_namespace.get(STORE_KEY)


def set_active(game):
    if game is None:
        bpy.app.driver_namespace.pop(STORE_KEY, None)
    else:
        bpy.app.driver_namespace[STORE_KEY] = game


# --- playfield ---
X_MIN, X_MAX = -9.0, 9.0
PLAYER_Z = 0.0
TOP_Z = 11.0

# What the camera must fit on screen, with a little breathing room.
FIELD_W = (X_MAX - X_MIN) + 2.0
FIELD_H = (TOP_Z + 1.0) - (PLAYER_Z - 1.5)
FIELD_CZ = (TOP_Z + 1.0 + PLAYER_Z - 1.5) * 0.5

# Blender's viewport behaves like a 72mm sensor; with the space's lens this gives
# the world units visible per unit of view_distance. Verified against a measured
# viewport: lens 50 -> 1.44 world units across, exactly 72/50.
SENSOR_MM = 72.0

# --- tuning ---
PLAYER_SPEED = 11.0      # units/sec
BULLET_SPEED = 20.0
BOMB_SPEED = 7.0
FIRE_COOLDOWN = 0.16     # sec between shots
BULLET_POOL = 24
BOMB_POOL = 16
ENEMY_COLS = 8
ENEMY_DX = 1.9
ENEMY_DZ = 1.4
ENEMY_TOP = 10.2
ENEMY_DROP = 0.65        # z step when the block hits an edge
START_LIVES = 3

# Swarm speed is a function of the LEVEL, not of how many are left. Scaling with
# survivors meant the last few enemies became uncatchably fast; each level just
# nudges it up a little instead, and it's capped.
ENEMY_SPEED_BASE = 1.6      # x units/sec on level 1
ENEMY_SPEED_PER_LEVEL = 0.2
ENEMY_SPEED_CAP = 5.0

# Difficulty leans on how OFTEN they shoot rather than on speed -- bombs get
# denser each level while falling at the same pace, which stays readable.
BOMB_CHANCE_BASE = 0.55     # expected bombs/sec across the whole swarm
BOMB_CHANCE_PER_LEVEL = 0.18
BOMB_CHANCE_CAP = 2.4

# The swarm's marching thump. Per level for the same reason as the two above:
# nothing in this game speeds up while a level is being played.
MARCH_BASE = 0.85           # sec between thumps on level 1
MARCH_PER_LEVEL = 0.07
MARCH_FLOOR = 0.24

# Row layout, top-down. Names describe the sprite silhouettes.
ROWS = ("BOSS", "BUTTERFLY", "BEE")

# --- starfield ---
# Drifting downward sells the ship flying UP the screen. Parked at positive Y,
# behind the gameplay plane at Y=0, so the depth buffer keeps them in the
# background without any draw-order trickery.
#
# The camera is orthographic, so distance can't shrink them -- the parallax has
# to come from speed, size and brightness varying per layer instead.
# (material, half-size, units/sec, Y depth, count)
STAR_LAYERS = (
    ("star_dim",  0.014, 1.3, 6.0, 26),
    ("star_mid",  0.022, 2.4, 4.0, 18),
    ("star_near", 0.032, 4.2, 2.5, 10),
)
STAR_TOP = 13.0          # respawn height; above anything the camera shows
STAR_BOTTOM = -2.5
STAR_X = 10.5

COMET_POOL = 3
COMET_SPEED = (9.0, 15.0)
COMET_GAP = (2.2, 7.0)   # sec between comets, drawn fresh each time
COMET_Y = 5.0
COMET_ANGLE = (30.0, 45.0)   # degrees off vertical; direction is coin-flipped

# --- explosions ---
# Pooled like the bullets: objects are made once and recycled, because creating
# and deleting datablocks mid-modal is slow and churns the undo stack.
SHARD_POOL = 90
SHARD_GRAVITY = 9.0      # z units/sec^2; the arc is what sells the pop
SHARD_SPIN = 11.0        # max rad/sec, sign random per shard

# count, (speed lo, hi), (life lo, hi), (scale lo, hi), material keys
BURSTS = {
    'ENEMY':  (11, (3.0, 8.5), (0.30, 0.55), (0.7, 1.5),
               ("spark_hot", "spark_ember")),
    'PLAYER': (26, (2.5, 11.0), (0.55, 1.00), (0.9, 2.1),
               ("spark_cool", "spark_pale", "spark_hot")),
}
SCORE_FOR = {"BOSS": 150, "BUTTERFLY": 80, "BEE": 50}

# Levels cycle through three casts: Roblox dummies, Blender primitives, bugs.
STYLE_CYCLE = ('DUMMY', 'SOLID', 'SPRITE')

SPIN_SPEED = 0.9         # rad/sec
SPIN_TILT = 0.32         # rad; tilting the spin axis makes solids read as 3D
SPIN_PHASE = 0.35        # per-enemy offset, so the swarm doesn't spin in lockstep
DUMMY_SPIN_SPEED = 0.55  # slower: a dummy needs to be readable, not a blur

# --- RBX Toolbox dummies ---
# Pulled out of the addon's template .blend. Every name here is an Object in
# that file; each is a single mesh with no rig, which is what makes them usable
# as cheap instanced enemies.
DUMMY_NAMES = (
    'R15 Blocky', 'R15 Boy', 'R15 Girl', 'R15 Woman',
    '4.0 Lin', '4.0 Oakley', '3.0 Man', '3.0 Woman',
    'Robloxian 2.0', 'Neoclassic Skyler', 'R6 (1.0)', 'SKN Anime',
)

# The dummies are authored ~5 units tall; the primitives are ~1. This is the
# height every dummy gets normalised to, picked to sit between the cube (0.85)
# and the monkey (~1.15) so all three casts feel like the same-size enemy.
DUMMY_HEIGHT = 1.05


def style_for_level(level):
    return STYLE_CYCLE[(level - 1) % len(STYLE_CYCLE)]


def speed_for_level(level):
    return min(ENEMY_SPEED_BASE + (level - 1) * ENEMY_SPEED_PER_LEVEL,
               ENEMY_SPEED_CAP)


def bomb_rate_for_level(level):
    return min(BOMB_CHANCE_BASE + (level - 1) * BOMB_CHANCE_PER_LEVEL,
               BOMB_CHANCE_CAP)


def march_rate_for_level(level):
    return max(MARCH_BASE - (level - 1) * MARCH_PER_LEVEL, MARCH_FLOOR)


# --------------------------------------------------------------------------
# Colours / materials
#
# ob.color gives one flat colour per object, which can't do the two-tone sprites.
# Materials with a viewport display colour can, so the enemies carry a body/wing
# material each and the viewport runs in MATERIAL colour mode.
# --------------------------------------------------------------------------

PALETTE = {
    "ship":        (0.30, 0.85, 1.00, 1.0),
    "ship_trim":   (0.95, 0.95, 1.00, 1.0),
    "bee_body":    (0.25, 0.55, 1.00, 1.0),
    "bee_wing":    (1.00, 0.85, 0.20, 1.0),
    "bfly_body":   (0.95, 0.25, 0.25, 1.0),
    "bfly_wing":   (0.35, 0.60, 1.00, 1.0),
    "boss_body":   (0.20, 0.80, 0.45, 1.0),
    "boss_wing":   (0.70, 0.40, 0.95, 1.0),
    "bullet":      (0.60, 1.00, 0.50, 1.0),
    "bomb":        (1.00, 0.45, 0.95, 1.0),
    # Explosion shards. Each burst mixes two tones so it reads as fire rather
    # than as a flat-coloured cloud.
    "spark_hot":   (1.00, 0.78, 0.20, 1.0),
    "spark_ember": (1.00, 0.33, 0.08, 1.0),
    "spark_cool":  (0.55, 0.90, 1.00, 1.0),
    "spark_pale":  (0.95, 0.98, 1.00, 1.0),
    # Starfield. Three tiers of brightness, dimmest = "furthest".
    "star_dim":    (0.34, 0.40, 0.60, 1.0),
    "star_mid":    (0.62, 0.70, 0.88, 1.0),
    "star_near":   (0.95, 0.98, 1.00, 1.0),
    # Dimmed twice, 30% each time (0.49x of full brightness), so a comet reads
    # as a passing detail rather than competing with the ship and enemies.
    "comet_head":  (0.49, 0.49, 0.49, 1.0),
    "comet_tail":  (0.20, 0.39, 0.49, 1.0),
}


def _material(key):
    name = PREFIX + "_" + key
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat.diffuse_color = PALETTE[key]      # what SOLID/MATERIAL shading shows
        mat.roughness = 0.6
    return mat


# --------------------------------------------------------------------------
# Geometry -- flat polygons on the XZ plane, built from raw vert/face data
# rather than bpy.ops primitives (those depend on context and would fight the
# modal operator). Each shape is a list of (material_key, [(x, z), ...]).
# --------------------------------------------------------------------------

def _mirror(poly):
    return [(-x, z) for (x, z) in reversed(poly)]


def _shape_mesh(name, parts):
    verts, faces, mat_idx = [], [], []
    keys = []
    for key, poly in parts:
        if key not in keys:
            keys.append(key)
        start = len(verts)
        for (x, z) in poly:
            verts.append((x, 0.0, z))
        faces.append(tuple(range(start, len(verts))))
        mat_idx.append(keys.index(key))

    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for k in keys:
        me.materials.append(_material(k))
    for poly, i in zip(me.polygons, mat_idx):
        poly.material_index = i
    return me


def _ship_parts():
    return [
        ("ship", [(0.0, 0.62), (-0.16, 0.10), (0.16, 0.10)]),            # nose
        ("ship", [(-0.62, -0.42), (-0.20, -0.42), (-0.16, 0.10),
                  (-0.34, -0.10)]),                                      # left wing
        ("ship", [(0.34, -0.10), (0.16, 0.10), (0.20, -0.42),
                  (0.62, -0.42)]),                                       # right wing
        ("ship_trim", [(-0.20, -0.42), (0.20, -0.42), (0.16, 0.10),
                       (-0.16, 0.10)]),                                  # fuselage
    ]


def _bee_parts():
    """Compact body, stubby side wings, two antennae."""
    wing = [(-0.20, 0.12), (-0.54, 0.28), (-0.58, -0.04), (-0.32, -0.16), (-0.18, -0.04)]
    ant = [(-0.09, 0.26), (-0.21, 0.48), (-0.03, 0.30)]
    return [
        ("bee_body", [(-0.13, -0.30), (0.13, -0.30), (0.21, 0.02),
                      (0.12, 0.28), (-0.12, 0.28), (-0.21, 0.02)]),
        ("bee_wing", wing),
        ("bee_wing", _mirror(wing)),
        ("bee_wing", ant),
        ("bee_wing", _mirror(ant)),
    ]


def _butterfly_parts():
    """Pointed body, wings swept up and out."""
    wing = [(-0.16, 0.10), (-0.60, 0.36), (-0.64, 0.02), (-0.30, -0.18), (-0.13, -0.12)]
    return [
        ("bfly_body", [(-0.11, -0.32), (0.11, -0.32), (0.17, 0.10),
                       (0.0, 0.34), (-0.17, 0.10)]),
        ("bfly_wing", wing),
        ("bfly_wing", _mirror(wing)),
    ]


def _boss_parts():
    """Wide and helmeted -- the one at the top of the formation."""
    wing = [(-0.30, 0.04), (-0.72, 0.26), (-0.76, -0.12), (-0.38, -0.28)]
    return [
        ("boss_body", [(-0.22, 0.06), (-0.13, 0.38), (0.13, 0.38), (0.22, 0.06)]),
        ("boss_wing", [(-0.30, -0.34), (0.30, -0.34), (0.32, 0.06), (-0.32, 0.06)]),
        ("boss_wing", wing),
        ("boss_wing", _mirror(wing)),
    ]


ENEMY_PARTS = {"BEE": _bee_parts, "BUTTERFLY": _butterfly_parts, "BOSS": _boss_parts}


# --- the alternate level: plain Blender primitives, slowly spinning ---
# Built with bmesh.ops rather than bpy.ops.mesh.primitive_*_add, which needs a
# context and an active object -- neither is safe to rely on inside a modal.

def _solid_bee(bm):
    bmesh.ops.create_cube(bm, size=0.85)


def _solid_butterfly(bm):
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=6,
                          radius1=0.55, radius2=0.0, depth=1.0)


def _solid_boss(bm):
    # Suzanne, because the Blender level ought to have one. She's 2.73 wide by
    # default, which would overlap her neighbours at 1.9 spacing.
    bmesh.ops.create_monkey(bm)
    bmesh.ops.scale(bm, vec=Vector((0.42, 0.42, 0.42)), verts=bm.verts)


SOLID_PARTS = {
    "BEE":       ("bee_body", _solid_bee),
    "BUTTERFLY": ("bfly_body", _solid_butterfly),
    "BOSS":      ("boss_body", _solid_boss),
}


def _solid_mesh(name, key, build):
    bm = bmesh.new()
    build(bm)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(_material(key))
    return me


def _half_extents(me):
    """Hitbox straight from the geometry, so it tracks whatever shape a level
    uses instead of needing a hand-tuned constant per sprite."""
    xs = [v.co.x for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    return ((max(xs) - min(xs)) * 0.5 * 0.9,
            (max(zs) - min(zs)) * 0.5 * 0.9)


def _shot_mesh(name, key, w, h):
    return _shape_mesh(name, [(key, [(-w, -h), (w, -h), (w, h), (-w, h)])])


def _comet_parts():
    """Bright head with a tail tapering off behind it. The comet travels DOWN,
    so the tail streams upward."""
    return [
        ("comet_head", [(-0.055, -0.10), (0.055, -0.10), (0.048, 0.03),
                        (-0.048, 0.03)]),
        ("comet_tail", [(-0.048, 0.03), (0.048, 0.03), (0.011, 1.00),
                        (-0.011, 1.00)]),
    ]


def _dummy_blend_path():
    """Locate RBX Toolbox's template .blend, asking the addon itself rather than
    hardcoding a path -- it moves with the user's Blender version."""
    try:
        from ... import glob_vars
    except Exception:
        return None
    try:
        path = glob_vars.addon_path + glob_vars.rbx_blend_file
    except AttributeError:
        return None
    import os
    return path if os.path.exists(path) else None


def _normalise_dummy(me, target_h):
    """Stand a dummy up, face it at the camera, and scale it to target_h.

    The roster is NOT authored consistently: half the dummies are Y-up and half
    are Z-up, so any fixed rotation lays six of them on their back. The axes are
    derived from the geometry instead -- for a humanoid the extents always sort
    the same way, so longest is height, middle is shoulder width and shortest is
    depth. Mapping those to Z / X / Y puts every dummy upright and broadside to
    the camera no matter how it was modelled.

    Done to the MESH, not the object, so enemies need no special rotation and
    the shared hitbox code keeps working. Safe to mutate: append gave us a
    private copy that teardown throws away.
    """
    co = [v.co for v in me.vertices]
    if not co:
        return
    lo = [min(c[i] for c in co) for i in range(3)]
    hi = [max(c[i] for c in co) for i in range(3)]
    ext = [hi[i] - lo[i] for i in range(3)]

    a_deep, a_wide, a_up = sorted(range(3), key=lambda i: ext[i])
    rows = [[0.0] * 3 for _ in range(3)]
    rows[0][a_wide] = 1.0
    rows[1][a_deep] = 1.0
    rows[2][a_up] = 1.0
    if Matrix(rows).determinant() < 0.0:
        # An odd permutation mirrors the model. Flip the depth axis to fix the
        # handedness: it points into the screen, so it's the one change the
        # player cannot see.
        rows[1][a_deep] = -1.0

    s = target_h / ext[a_up] if ext[a_up] > 1e-6 else 1.0
    me.transform(Matrix.Scale(s, 4) @ Matrix(rows).to_4x4())

    # Re-measure and centre: the permutation moved everything, and an off-centre
    # dummy would sit crooked in the formation grid.
    co = [v.co for v in me.vertices]
    mid = [(min(c[i] for c in co) + max(c[i] for c in co)) * 0.5 for i in range(3)]
    me.transform(Matrix.Translation((-mid[0], -mid[1], -mid[2])))


def _load_dummy_meshes():
    """Append the dummy roster and hand back (meshes, images).

    Returns ([], []) if RBX Toolbox isn't installed -- a missing addon must
    downgrade the level, never break the game for someone who just pasted the
    script in.
    """
    path = _dummy_blend_path()
    if not path:
        return [], []
    before = set(bpy.data.images)
    try:
        with bpy.data.libraries.load(path, link=False) as (src, dst):
            dst.objects = [n for n in DUMMY_NAMES if n in src.objects]
    except Exception:
        return [], []

    meshes = []
    for ob in dst.objects:
        if ob is None:
            continue
        me = ob.data if ob.type == 'MESH' else None
        # The wrapper object has done its job -- only the mesh is wanted, and
        # dropping it also drops any geometry-nodes modifier riding on it.
        bpy.data.objects.remove(ob, do_unlink=True)
        if me is not None and len(me.vertices):
            _normalise_dummy(me, DUMMY_HEIGHT)
            meshes.append(me)
    return meshes, [i for i in bpy.data.images if i not in before]


def _shard_mesh(name, key):
    """One small irregular quad. Irregular on purpose -- four identical squares
    tumbling together look like confetti, a ragged one looks like debris."""
    return _shape_mesh(name, [(key, [(-0.075, -0.055), (0.085, -0.075),
                                     (0.065, 0.080), (-0.060, 0.060)])])


def _spawn(coll, name, me):
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


# --------------------------------------------------------------------------
# Sound
#
# Everything here is generated into a numpy buffer and handed to aud once, at
# startup. Playing is then just dev.play() on a buffer that already lives in
# RAM -- measured at ~0.02ms per call, which is what makes it safe to trigger
# from inside the modal loop.
# --------------------------------------------------------------------------

SFX_VOLUME = 0.30        # master; everything below is relative to this


def _osc(rate, dur, f0, f1, wave='square'):
    """One oscillator with an exponential pitch glide from f0 to f1.

    The glide is why this integrates frequency instead of the more obvious
    sin(2*pi*f*t): with f varying, that expression gives the wrong instantaneous
    pitch and the sweep comes out audibly wrong. Accumulating phase per sample
    is the correct form.
    """
    n = max(1, int(rate * dur))
    t = np.arange(n, dtype=np.float32) / rate
    f = f0 * (f1 / f0) ** (t / dur)
    ph = np.cumsum(2.0 * np.pi * f / rate).astype(np.float32)
    if wave == 'square':
        return np.sign(np.sin(ph)).astype(np.float32)
    if wave == 'saw':
        return (2.0 * ((ph / (2.0 * np.pi)) % 1.0) - 1.0).astype(np.float32)
    return np.sin(ph).astype(np.float32)


def _decay(rate, dur, k):
    n = max(1, int(rate * dur))
    t = np.linspace(0.0, 1.0, n, dtype=np.float32)
    # The tiny ramp on the front kills the click a hard start would make.
    env = np.exp(-k * t).astype(np.float32)
    a = max(1, int(rate * 0.004))
    env[:a] *= np.linspace(0.0, 1.0, a, dtype=np.float32)
    return env


def _noise(rate, dur, rng, softness=1):
    n = max(1, int(rate * dur))
    w = rng.uniform(-1.0, 1.0, n).astype(np.float32)
    if softness > 1:
        # Moving average = cheap lowpass. Raw white noise reads as hiss; taking
        # the top off is what makes it read as an explosion.
        k = np.ones(softness, dtype=np.float32) / softness
        w = np.convolve(w, k, mode='same').astype(np.float32)
    return w


def _norm(w, peak):
    m = float(np.max(np.abs(w))) if len(w) else 0.0
    return (w * (peak / m)).astype(np.float32) if m > 1e-9 else w


def _pad(parts):
    return np.concatenate(parts).astype(np.float32) if parts else np.zeros(1, np.float32)


def _build_sfx(rate):
    """The whole sound set. Returns {name: float32 mono array}."""
    rng = np.random.default_rng(7)      # fixed seed: same game every session
    s = {}

    # Laser: fast square sweep downward. The classic, and it cuts through
    # everything else without being loud.
    s['shoot'] = _norm(_osc(rate, 0.09, 1500, 320, 'square')
                       * _decay(rate, 0.09, 5.0), 0.32)

    # Enemy death: softened noise for the debris, plus a low sine drop that
    # gives it a body rather than just a hiss.
    d = 0.26
    s['enemy_die'] = _norm(_noise(rate, d, rng, 9) * _decay(rate, d, 8.0)
                           + _osc(rate, d, 420, 90, 'sine') * _decay(rate, d, 6.0) * 0.8,
                           0.55)

    # Player death: longer, lower, and dirtier -- a saw layer under the noise.
    d = 0.85
    s['player_die'] = _norm(_noise(rate, d, rng, 17) * _decay(rate, d, 4.0)
                            + _osc(rate, d, 300, 40, 'saw') * _decay(rate, d, 3.0) * 0.9
                            + _osc(rate, d, 90, 28, 'sine') * _decay(rate, d, 2.2), 0.85)

    # Jingles: plain square notes, arcade-style.
    def notes(seq, note_d, k=4.0, wave='square'):
        env = _decay(rate, note_d, k)
        return _pad([_osc(rate, note_d, f, f, wave) * env for f in seq])

    s['level_up'] = _norm(notes([523, 659, 784, 1047], 0.085, 3.5), 0.42)
    s['game_over'] = _norm(notes([392, 330, 262, 196], 0.20, 2.2), 0.50)

    # The marching thump. Four descending tones cycled one per step, exactly
    # like the arcade original -- the swarm's pulse, not a one-off effect.
    for i, f in enumerate((110, 98, 87, 78)):
        s['march%d' % i] = _norm(_osc(rate, 0.09, f, f * 0.85, 'square')
                                 * _decay(rate, 0.09, 7.0), 0.30)
    return s


# --------------------------------------------------------------------------
# Chiptune
#
# Modelled on the NES APU's voice layout, because that layout IS the sound:
# two pulse channels (lead + arpeggio), one triangle (bass), one noise (drums).
# The track is rendered once into a single buffer and looped by the device, so
# playing it costs nothing per frame.
# --------------------------------------------------------------------------

MUSIC_VOLUME = 0.24         # relative to SFX_VOLUME
MUSIC_BPM = 152
# Each level nudges playback rate up, which raises key and tempo together --
# the old arcade trick. Per level, so it holds steady while a level is played.
MUSIC_PITCH_PER_LEVEL = 0.028
MUSIC_PITCH_CAP = 1.22

# A minor. Eight bars: Am F C G | Am F G Am.
_BASS_ROOTS = (45, 41, 48, 43, 45, 41, 43, 45)
_CHORDS = ((57, 60, 64, 69), (53, 57, 60, 65), (52, 55, 60, 64), (55, 59, 62, 67),
           (57, 60, 64, 69), (53, 57, 60, 65), (55, 59, 62, 67), (57, 60, 64, 69))

# (midi, beats) per bar; None is a rest. Every bar totals 4 beats.
_LEAD = (
    ((64, 1), (69, .5), (67, .5), (64, 1), (62, 1)),
    ((60, 1), (64, .5), (65, .5), (64, 2)),
    ((67, 1), (64, .5), (60, .5), (62, 2)),
    ((59, 1), (62, .5), (67, .5), (62, 1), (59, 1)),
    ((69, 1), (64, .5), (69, .5), (72, 1), (71, 1)),
    ((69, 1.5), (67, .5), (65, 1), (64, 1)),
    ((62, 1), (67, .5), (71, .5), (74, 2)),
    ((72, 1), (71, .5), (69, .5), (69, 2)),
)

# 16 steps per bar. K kick, S snare, h hat, . rest.
_DRUMS = (
    "Kh.hSh.hKhKhSh.h", "Kh.hSh.hKhKhSh.h",
    "Kh.hSh.hKhKhSh.h", "Kh.hSh.hKhKhSh.h",
    "Kh.hSh.hKhKhSh.h", "Kh.hSh.hKhKhSh.h",
    "Kh.hSh.hKhKhSh.h", "KhKhShShKhKhSSSS",
)


def _midi_hz(n):
    return 440.0 * (2.0 ** ((n - 69) / 12.0))


def _phase(rate, n, f):
    return ((np.arange(n, dtype=np.float32) * (f / rate)) % 1.0).astype(np.float32)


def _v_pulse(rate, n, f, duty=0.5):
    return np.where(_phase(rate, n, f) < duty, 1.0, -1.0).astype(np.float32)


def _v_triangle(rate, n, f):
    """NES triangle, quantised to 16 steps -- that staircase is where its
    slightly gritty bass character comes from, so a smooth triangle is wrong."""
    tri = 2.0 * np.abs(2.0 * _phase(rate, n, f) - 1.0) - 1.0
    return (np.round(tri * 7.5) / 7.5).astype(np.float32)


def _note_env(rate, n, k):
    """Fast attack, exponential decay, forced release. The release matters: a
    note cut mid-cycle clicks, and in a loop that click repeats forever."""
    if n <= 0:
        return np.zeros(0, np.float32)
    env = np.exp(-k * np.linspace(0.0, 1.0, n, dtype=np.float32)).astype(np.float32)
    a = min(max(1, int(rate * 0.003)), n)
    env[:a] *= np.linspace(0.0, 1.0, a, dtype=np.float32)
    r = min(max(1, int(rate * 0.008)), n)
    env[-r:] *= np.linspace(1.0, 0.0, r, dtype=np.float32)
    return env


def _lay(buf, start, w):
    """Mix w into buf at sample `start`, clipped to the buffer end."""
    i0 = max(0, int(start))
    n = min(len(w), len(buf) - i0)
    if n > 0:
        buf[i0:i0 + n] += w[:n]


def _build_music(rate):
    """Render the loop. Returns a float32 mono array of exactly 8 bars."""
    rng = np.random.default_rng(11)
    beat = 60.0 / MUSIC_BPM
    bar = beat * 4.0
    total = int(round(bar * len(_LEAD) * rate))
    lead = np.zeros(total, np.float32)
    arp = np.zeros(total, np.float32)
    bass = np.zeros(total, np.float32)
    drum = np.zeros(total, np.float32)

    for b in range(len(_LEAD)):
        t_bar = b * bar

        # -- lead: 50% pulse, the melody
        t = t_bar
        for midi, beats in _LEAD[b]:
            d = beats * beat
            n = int(d * 0.92 * rate)
            if midi is not None and n > 0:
                _lay(lead, t * rate,
                     _v_pulse(rate, n, _midi_hz(midi), 0.5) * _note_env(rate, n, 1.6))
            t += d

        # -- arpeggio: 25% pulse running 16ths through the chord
        chord = _CHORDS[b]
        step = beat / 4.0
        n = int(step * 0.9 * rate)
        for i in range(16):
            _lay(arp, (t_bar + i * step) * rate,
                 _v_pulse(rate, n, _midi_hz(chord[i % len(chord)] + 12), 0.25)
                 * _note_env(rate, n, 3.0))

        # -- bass: triangle, octave-jumping eighths
        root = _BASS_ROOTS[b]
        step = beat / 2.0
        n = int(step * 0.95 * rate)
        for i in range(8):
            midi = root + (12 if i in (2, 5) else 0)
            _lay(bass, (t_bar + i * step) * rate,
                 _v_triangle(rate, n, _midi_hz(midi)) * _note_env(rate, n, 1.1))

        # -- drums: the noise channel
        step = beat / 4.0
        for i, c in enumerate(_DRUMS[b]):
            if c == '.':
                continue
            at = (t_bar + i * step) * rate
            if c == 'K':
                # NES kicks are a fast pitch drop, not noise.
                n = int(0.09 * rate)
                _lay(drum, at, _osc(rate, 0.09, 150, 45, 'sine')
                     * _note_env(rate, n, 7.0) * 1.0)
            elif c == 'S':
                n = int(0.11 * rate)
                _lay(drum, at, _noise(rate, 0.11, rng, 5) * _note_env(rate, n, 9.0) * 0.7)
            else:
                n = int(0.035 * rate)
                _lay(drum, at, _noise(rate, 0.035, rng, 2) * _note_env(rate, n, 12.0) * 0.28)

    mix = (_norm(lead, 0.60) + _norm(arp, 0.26)
           + _norm(bass, 0.75) + _norm(drum, 0.55))
    return _norm(mix, 0.85)


class Jukebox:
    """Owns the audio device and the buffers. Every method is a no-op when
    audio is unavailable, so the game never needs to check first."""

    def __init__(self):
        self.dev = None
        self.sounds = {}
        self._handles = []
        self._march = 0
        self.music = None
        self._music_h = None
        self.muted = False

    def build(self):
        if aud is None or np is None:
            return
        try:
            self.dev = aud.Device()
        except Exception:
            self.dev = None            # e.g. Audio Device set to None
            return
        rate = int(getattr(self.dev, "rate", 0) or 48000)
        try:
            raw = _build_sfx(rate)
            for k, w in raw.items():
                # aud documents a 2-D (samples, channels) buffer; mono is (n, 1)
                # and the device rechannels it to stereo itself.
                buf = np.ascontiguousarray(w.reshape(-1, 1) * SFX_VOLUME,
                                           dtype=np.float32)
                self.sounds[k] = aud.Sound.buffer(buf, rate)
        except Exception:
            self.sounds = {}
        try:
            song = _build_music(rate).reshape(-1, 1) * MUSIC_VOLUME
            self.music = aud.Sound.buffer(
                np.ascontiguousarray(song, dtype=np.float32), rate)
        except Exception:
            self.music = None

    # -- music --

    def start_music(self, level=1):
        if self.music is None or self.dev is None or self.muted:
            return
        self.stop_music()
        try:
            h = self.dev.play(self.music)
            h.loop_count = -1                  # -1 is loop forever
            h.pitch = self.music_pitch(level)
            self._music_h = h
        except Exception:
            self._music_h = None

    @staticmethod
    def music_pitch(level):
        return min(1.0 + (level - 1) * MUSIC_PITCH_PER_LEVEL, MUSIC_PITCH_CAP)

    def set_level(self, level):
        """Retune the running loop instead of restarting it, so the track keeps
        playing across a level change rather than jumping back to bar one."""
        if self._music_h is None:
            return
        try:
            self._music_h.pitch = self.music_pitch(level)
        except Exception:
            self._music_h = None

    def stop_music(self):
        if self._music_h is not None:
            try:
                self._music_h.stop()
            except Exception:
                pass
            self._music_h = None

    def toggle_mute(self, level=1):
        self.muted = not self.muted
        if self.muted:
            self.stop_music()
        else:
            self.start_music(level)
        return self.muted

    def play(self, key, jitter=0.0):
        snd = self.sounds.get(key)
        if snd is None or self.dev is None:
            return
        try:
            h = self.dev.play(snd)
            if jitter:
                # Same buffer, different pitch each time. Without this a run of
                # kills sounds like a stuck record.
                h.pitch = 1.0 + random.uniform(-jitter, jitter)
            self._handles.append(h)
        except Exception:
            return
        if len(self._handles) > 24:
            self._handles = [x for x in self._handles if self._playing(x)]

    @staticmethod
    def _playing(h):
        try:
            return bool(h.status)
        except Exception:
            return False

    def march(self):
        self.play('march%d' % self._march)
        self._march = (self._march + 1) % 4

    def stop(self):
        """Stop only OUR handles. dev.stopAll() would also cut the user's
        sequencer or animation playback, which isn't ours to touch."""
        self.stop_music()
        for h in self._handles:
            try:
                h.stop()
            except Exception:
                pass
        self._handles = []


# --------------------------------------------------------------------------
# HUD
# --------------------------------------------------------------------------

def _set_font_size(fid, size):
    try:
        blf.size(fid, size)          # Blender 4.0+
    except TypeError:
        blf.size(fid, size, 72)      # older signature


def _text(fid, x, y, size, color, s):
    _set_font_size(fid, size)
    blf.color(fid, *color)
    blf.position(fid, x, y, 0)
    blf.draw(fid, s)


def _text_w(fid, size, s):
    _set_font_size(fid, size)
    return blf.dimensions(fid, s)[0]


_SHADER = None
_SHADER_TRIED = False


def _uniform_shader():
    """The builtin's name changed at Blender 4.0: 3.x wanted '2D_UNIFORM_COLOR'
    and 5.1 raises ValueError for it, while 'UNIFORM_COLOR' is the modern name.
    Try both, cache the winner, and give up gracefully -- losing the game-over
    panel's boxes is survivable, an exception every redraw is not."""
    global _SHADER, _SHADER_TRIED
    if not _SHADER_TRIED:
        _SHADER_TRIED = True
        for name in ('UNIFORM_COLOR', '2D_UNIFORM_COLOR'):
            try:
                _SHADER = gpu.shader.from_builtin(name)
                break
            except Exception:
                continue
    return _SHADER


def _rect(x1, y1, x2, y2, color):
    shader = _uniform_shader()
    if shader is None:
        return
    batch = batch_for_shader(
        shader, 'TRIS',
        {"pos": [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]},
        indices=[(0, 1, 2), (0, 2, 3)])
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    gpu.state.blend_set('NONE')


def _draw_hud():
    """POST_PIXEL draw handler, wrapped so it can never raise.

    A draw callback runs on EVERY redraw, so one bad frame becomes an endless
    console spew -- and the references it touches (the area, the game's objects)
    can genuinely go stale underneath it if a new .blend is loaded mid-game.
    Swallowing here is right: there is no safe way to unregister or mutate data
    from inside a draw callback, so the only correct move is to draw nothing.
    """
    try:
        _draw_hud_body()
    except Exception:
        pass


def _draw_hud_body():
    game = get_active()
    if game is None or game.closed:
        return
    ctx = bpy.context
    area = getattr(game, "_area_ref", None)
    if area is None or ctx.area != area:
        return                       # only paint the viewport we took over
    region = ctx.region
    if region is None:
        return
    W, H = region.width, region.height
    ui = ctx.preferences.system.ui_scale
    fid = 0

    s_big = int(22 * ui)
    s_small = int(13 * ui)
    pad = int(16 * ui)

    _text(fid, pad, H - pad - s_big, s_big, (0.85, 0.95, 1.0, 1.0),
          "SCORE  %d" % game.score)

    lives = "LIVES  %d" % max(game.lives, 0)
    _text(fid, W - pad - _text_w(fid, s_big, lives), H - pad - s_big, s_big,
          (0.85, 0.95, 1.0, 1.0), lives)

    lvl = "LEVEL %d" % game.wave
    _text(fid, (W - _text_w(fid, s_small, lvl)) * 0.5, H - pad - s_small,
          s_small, (0.55, 0.65, 0.8, 1.0), lvl)

    hint = "← →  move     SPACE  fire     M  %s     ESC  quit" % (
        "music on" if game.audio.muted else "music off")
    _text(fid, (W - _text_w(fid, s_small, hint)) * 0.5, pad, s_small,
          (0.55, 0.65, 0.80, 1.0), hint)

    game._buttons = {}
    if not game.over:
        return

    # --- game over panel ---
    _rect(0, 0, W, H, (0.0, 0.0, 0.02, 0.78))
    s_huge = int(46 * ui)
    msg = game.message
    cy = H * 0.5
    _text(fid, (W - _text_w(fid, s_huge, msg)) * 0.5, cy + int(60 * ui), s_huge,
          (1.0, 0.35, 0.35, 1.0), msg)
    fin = "FINAL SCORE  %d" % game.score
    _text(fid, (W - _text_w(fid, s_big, fin)) * 0.5, cy + int(24 * ui), s_big,
          (0.9, 0.95, 1.0, 1.0), fin)

    bw, bh, gap = int(190 * ui), int(44 * ui), int(18 * ui)
    by = cy - int(50 * ui)
    total = bw * 2 + gap
    x0 = (W - total) * 0.5
    for key, label, bx, col in (
        ("start", "START GAME", x0, (0.15, 0.45, 0.30, 0.95)),
        ("quit", "QUIT GAME", x0 + bw + gap, (0.45, 0.18, 0.20, 0.95)),
    ):
        hot = game._hover == key
        c = tuple(min(1.0, v * 1.5) if i < 3 else v for i, v in enumerate(col)) if hot else col
        _rect(bx, by, bx + bw, by + bh, c)
        _rect(bx, by, bx + bw, by + int(2 * ui), (1, 1, 1, 0.25))
        _text(fid, bx + (bw - _text_w(fid, s_small, label)) * 0.5,
              by + bh * 0.5 - s_small * 0.5, s_small, (1, 1, 1, 1), label)
        game._buttons[key] = (bx, by, bx + bw, by + bh)

    keys = "ENTER restart        ESC quit"
    _text(fid, (W - _text_w(fid, s_small, keys)) * 0.5, by - int(30 * ui),
          s_small, (0.5, 0.6, 0.75, 1.0), keys)


# --------------------------------------------------------------------------
# Game state
# --------------------------------------------------------------------------

class BestFeatureGame:
    def __init__(self):
        self.coll = None
        self.player = None
        self.bullets = []
        self.bombs = []
        self.shards = []           # [obj, alive, vx, vz, spin, t, life, size]
        self.stars = []            # [obj, speed]
        self.comets = []           # [obj, alive, speed]
        self._comet_at = 0.0
        # [obj, alive, kind, (half_x, half_z)] -- the hitbox rides on the entry
        # because a DUMMY wave mixes twelve differently-sized models in one grid,
        # so it can no longer be looked up per (style, kind).
        self.enemies = []
        self.score = 0
        self.lives = START_LIVES
        self.wave = 1
        self.over = False
        self.message = ""
        self.style = 'SOLID'
        self._spin = 0.0
        self._meshes = {}
        self._shard_meshes = {}
        self._dummies = []
        self._dummy_images = []
        self._hit = {}
        self._last_fire = 0.0
        self._enemy_dir = 1.0
        self._respawn_at = 0.0
        self.audio = Jukebox()
        self._march_at = 0.0
        self.closed = False
        self._saved = None
        self._handle = None
        self._area_ref = None
        self._buttons = {}
        self._hover = None

    # -- take over / hand back the user's viewport --
    # These live on the game rather than the operator so that ANY later script
    # run can restore the user's scene, even one that never saw the operator.

    @staticmethod
    def _fit_distance(area, region):
        """The view_distance that fits the whole playfield on screen.

        Computed rather than measured. Sampling the viewport is a trap here:
        before the takeover the matrices describe the user's old view (and if it
        was perspective, its scale doesn't carry to ortho at all), and after the
        takeover they're stale until a redraw. Both give a wrong answer.

        Blender's ortho viewport shows `view_distance * SENSOR / lens` world
        units across the region's longer axis, with the shorter axis scaled by
        aspect -- so the exact distance falls straight out of the region size.
        """
        if not region or region.width < 2 or region.height < 2:
            return 20.0
        sp = area.spaces.active
        lens = getattr(sp, "lens", 50.0) or 50.0
        k_long = SENSOR_MM / lens
        big = float(max(region.width, region.height))
        small = float(min(region.width, region.height))
        k_short = k_long * (small / big)
        if region.width >= region.height:
            k_w, k_h = k_long, k_short
        else:
            k_w, k_h = k_short, k_long
        d = max(FIELD_W / k_w, FIELD_H / k_h)
        return min(max(d, 1.0), 500.0)

    def take_over(self, context, area, region):
        sp = area.spaces.active
        rv = sp.region_3d
        fit = self._fit_distance(area, region)
        self._area_ref = area

        self._saved = {
            "area": area,
            "space": sp,
            "hidden": [(ob, ob.hide_viewport) for ob in context.scene.objects],
            "view": (rv.view_perspective, rv.view_rotation.copy(),
                     rv.view_location.copy(), rv.view_distance),
            "shading": (sp.shading.type, sp.shading.color_type,
                        sp.shading.background_type, sp.shading.background_color[:]),
            "overlay": sp.overlay.show_overlays,
            # Regions: the score/lives HUD is useless if the N-panel covers it,
            # and a closed N-panel used to hide the score entirely. Everything
            # goes, and comes back on exit.
            "regions": (sp.show_region_ui, sp.show_region_toolbar,
                        sp.show_region_header, sp.show_region_tool_header),
            "gizmo": sp.show_gizmo,
        }
        for ob, _ in self._saved["hidden"]:
            ob.hide_viewport = True

        rv.view_perspective = 'ORTHO'
        rv.view_rotation = FRONT_VIEW.copy()
        rv.view_location = (0.0, 0.0, FIELD_CZ)
        rv.view_distance = fit
        sp.shading.type = 'SOLID'
        # TEXTURE, not MATERIAL: it shows the dummies' real Roblox skins, and
        # everything else in the game has no image texture, so it falls back to
        # the material's viewport colour -- identical to what MATERIAL gave.
        sp.shading.color_type = 'TEXTURE'
        sp.shading.background_type = 'VIEWPORT'
        sp.shading.background_color = (0.02, 0.02, 0.05)
        sp.overlay.show_overlays = False
        sp.show_region_ui = False
        sp.show_region_toolbar = False
        sp.show_region_header = False
        sp.show_region_tool_header = False
        sp.show_gizmo = False

        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            _draw_hud, (), 'WINDOW', 'POST_PIXEL')

    def hand_back(self):
        if self._handle is not None:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            except Exception:
                pass
            self._handle = None

        s = self._saved
        if not s:
            return
        for ob, hidden in s["hidden"]:
            try:
                ob.hide_viewport = hidden
            except ReferenceError:
                pass                       # object deleted while playing
        try:
            sp = s["space"]
            rv = sp.region_3d
            persp, rot, loc, dist = s["view"]
            rv.view_perspective = persp
            rv.view_rotation = rot
            rv.view_location = loc
            rv.view_distance = dist
            (sp.shading.type, sp.shading.color_type,
             sp.shading.background_type, bg) = s["shading"]
            sp.shading.background_color = bg
            sp.overlay.show_overlays = s["overlay"]
            (sp.show_region_ui, sp.show_region_toolbar,
             sp.show_region_header, sp.show_region_tool_header) = s["regions"]
            sp.show_gizmo = s["gizmo"]
            s["area"].tag_redraw()
        except (ReferenceError, AttributeError):
            pass                           # viewport closed while playing
        self._saved = None

    def shutdown(self):
        """Idempotent: safe from the operator, from unregister(), or both."""
        if self.closed:
            return
        self.closed = True
        self.audio.stop()          # a death sound must not outlive the game
        self.teardown()
        self.hand_back()

    # -- build / destroy --

    def build(self, context):
        self.audio.build()
        self.coll = bpy.data.collections.new(COLL_NAME)
        context.scene.collection.children.link(self.coll)

        self.player = _spawn(self.coll, PREFIX + "_player",
                             _shape_mesh(PREFIX + "_ship", _ship_parts()))
        self.player.location = (0.0, 0.0, PLAYER_Z)

        bm = _shot_mesh(PREFIX + "_bullet", "bullet", 0.07, 0.24)
        for i in range(BULLET_POOL):
            ob = _spawn(self.coll, PREFIX + "_bullet_%02d" % i, bm)
            ob.hide_viewport = True
            self.bullets.append([ob, False])

        km = _shot_mesh(PREFIX + "_bomb", "bomb", 0.09, 0.20)
        for i in range(BOMB_POOL):
            ob = _spawn(self.coll, PREFIX + "_bomb_%02d" % i, km)
            ob.hide_viewport = True
            self.bombs.append([ob, False])

        for key, size, speed, y, count in STAR_LAYERS:
            me = _shot_mesh(PREFIX + "_star_" + key, key, size, size)
            for i in range(count):
                ob = _spawn(self.coll, "%s_star_%s_%02d" % (PREFIX, key, i), me)
                # Seeded across the whole field, not all at the top: starting
                # them in a row would read as a curtain dropping in.
                ob.location = (random.uniform(-STAR_X, STAR_X), y,
                               random.uniform(STAR_BOTTOM, STAR_TOP))
                self.stars.append([ob, speed])

        cm = _shape_mesh(PREFIX + "_comet", _comet_parts())
        for i in range(COMET_POOL):
            ob = _spawn(self.coll, PREFIX + "_comet_%02d" % i, cm)
            ob.hide_viewport = True
            self.comets.append([ob, False, 0.0, 0.0])   # [obj, alive, vx, vz]

        # One shared pool for every burst; the colour comes from swapping the
        # shard's mesh at spawn time, so 90 objects cover all burst types.
        self._shard_meshes = {}
        for kind, (_, _, _, _, keys) in BURSTS.items():
            self._shard_meshes[kind] = [
                _shard_mesh(PREFIX + "_shard_" + k, k) for k in keys]
        sm = self._shard_meshes['ENEMY'][0]
        for i in range(SHARD_POOL):
            ob = _spawn(self.coll, PREFIX + "_shard_%02d" % i, sm)
            ob.hide_viewport = True
            self.shards.append([ob, False, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0])

        self._meshes = {
            'SPRITE': {k: _shape_mesh(PREFIX + "_" + k.lower(), f())
                       for k, f in ENEMY_PARTS.items()},
            'SOLID': {k: _solid_mesh(PREFIX + "_solid_" + k.lower(), key, build)
                      for k, (key, build) in SOLID_PARTS.items()},
        }
        self._dummies, self._dummy_images = _load_dummy_meshes()

        # Keyed by mesh, not by (style, kind): one lookup now covers the sprites,
        # the primitives and every dummy.
        self._hit = {me.name: _half_extents(me)
                     for group in self._meshes.values()
                     for me in group.values()}
        self._hit.update({me.name: _half_extents(me) for me in self._dummies})
        self.spawn_wave()
        self.audio.start_music(self.wave)

    def spawn_wave(self):
        for e in self.enemies:
            try:
                bpy.data.objects.remove(e[0], do_unlink=True)
            except ReferenceError:
                pass
        self.enemies = []
        self.style = style_for_level(self.wave)
        if self.style == 'DUMMY' and not self._dummies:
            self.style = 'SOLID'          # RBX Toolbox absent -- skip the cast
        self._spin = 0.0
        x0 = -(ENEMY_COLS - 1) * ENEMY_DX * 0.5
        for r, kind in enumerate(ROWS):
            for c in range(ENEMY_COLS):
                if self.style == 'DUMMY':
                    # Drawn per slot rather than per row: the roster is twelve
                    # distinct characters, and scattering them is the whole
                    # point of the level. The row still sets the score.
                    me = random.choice(self._dummies)
                else:
                    me = self._meshes[self.style][kind]
                ob = _spawn(self.coll, "%s_%s_%d" % (PREFIX, kind.lower(), c), me)
                ob.location = (x0 + c * ENEMY_DX, 0.0, ENEMY_TOP - r * ENEMY_DZ)
                if self.style == 'SOLID':
                    ob.rotation_euler = (SPIN_TILT, 0.0, 0.0)
                self.enemies.append([ob, True, kind, self._hit[me.name]])
        self._enemy_dir = 1.0

    def reset(self):
        """Start Game from the game-over panel: same objects, fresh run."""
        self.score = 0
        self.lives = START_LIVES
        self.wave = 1
        self.over = False
        self.message = ""
        self._respawn_at = 0.0
        self.audio.stop()          # cut the game-over jingle on restart
        self._march_at = 0.0
        self.audio.start_music(self.wave)
        for b in self.bullets + self.bombs + self.shards:
            self._kill(b)
        self.player.location = (0.0, 0.0, PLAYER_Z)
        self.spawn_wave()

    def teardown(self):
        if not self.coll:
            return
        meshes, mats = set(), set()
        for ob in list(self.coll.objects):
            if ob.data:
                meshes.add(ob.data)
            bpy.data.objects.remove(ob, do_unlink=True)
        # The style that wasn't on screen when we quit is referenced by no
        # object, so the loop above never sees its meshes -- they'd leak, along
        # with their materials, on every play.
        for group in self._meshes.values():
            meshes.update(group.values())
        # Same story for the shard tints no shard happened to be wearing.
        for group in self._shard_meshes.values():
            meshes.update(group)
        meshes.update(self._dummies)
        for me in meshes:
            for m in me.materials:
                if m:
                    mats.add(m)
            if me.users == 0:
                bpy.data.meshes.remove(me)
        for m in mats:
            if m.users == 0:
                bpy.data.materials.remove(m)
        # Appending the dummies dragged their textures in too. Without this the
        # user's .blend gains twelve images every single time they press Play.
        for img in self._dummy_images:
            try:
                if img.users == 0:
                    bpy.data.images.remove(img)
            except ReferenceError:
                pass
        self._dummies = []
        self._dummy_images = []
        self._meshes = {}
        self._shard_meshes = {}
        self._hit = {}
        bpy.data.collections.remove(self.coll)
        self.coll = None

    # -- helpers --

    def _alive_enemies(self):
        return [e for e in self.enemies if e[1]]

    def fire(self, now):
        if self.over or now - self._last_fire < FIRE_COOLDOWN:
            return
        for b in self.bullets:
            if not b[1]:
                b[1] = True
                b[0].hide_viewport = False
                b[0].location = (self.player.location.x, 0.0, PLAYER_Z + 0.6)
                self._last_fire = now
                self.audio.play('shoot', 0.06)
                return

    def _drop_bomb(self, enemy):
        for k in self.bombs:
            if not k[1]:
                k[1] = True
                k[0].hide_viewport = False
                k[0].location = (enemy.location.x, 0.0, enemy.location.z - 0.5)
                return

    def burst(self, x, z, kind):
        """Throw a ring of shards out of (x, z). Silently does less than asked
        if the pool is dry -- dropping a few shards off a big pile-up is far
        better than stalling the frame to grow the pool."""
        count, spd, life, size, _ = BURSTS[kind]
        tints = self._shard_meshes[kind]
        free = (s for s in self.shards if not s[1])
        for _ in range(count):
            s = next(free, None)
            if s is None:
                return
            ang = random.uniform(0.0, math.tau)
            v = random.uniform(*spd)
            s[1] = True
            s[2] = math.cos(ang) * v
            s[3] = math.sin(ang) * v
            s[4] = random.uniform(-SHARD_SPIN, SHARD_SPIN)
            s[5] = 0.0
            s[6] = random.uniform(*life)
            s[7] = random.uniform(*size)
            ob = s[0]
            ob.data = random.choice(tints)
            ob.location = (x + random.uniform(-0.14, 0.14), 0.0,
                           z + random.uniform(-0.14, 0.14))
            # Spin is around Y: the shards are flat on XZ, so Y is the axis that
            # tumbles them in the plane the player is looking at.
            ob.rotation_euler = (0.0, random.uniform(0.0, math.tau), 0.0)
            ob.scale = (s[7], s[7], s[7])
            ob.hide_viewport = False

    def _update_sky(self, dt, now):
        """Scroll the background. Runs whatever the game state is -- a frozen
        starfield behind the game-over panel would look like a crash."""
        for s in self.stars:
            ob = s[0]
            ob.location.z -= s[1] * dt
            if ob.location.z < STAR_BOTTOM:
                # Wrap to the top with a fresh column, so the field never
                # settles into a visible repeating pattern.
                ob.location.z = STAR_TOP
                ob.location.x = random.uniform(-STAR_X, STAR_X)

        for c in self.comets:
            if not c[1]:
                continue
            c[0].location.x += c[2] * dt
            c[0].location.z += c[3] * dt
            # Now that they travel sideways they can leave past an edge as well
            # as the bottom, so retire on either.
            if c[0].location.z < STAR_BOTTOM - 1.6 or \
                    abs(c[0].location.x) > STAR_X + 2.5:
                self._kill(c)

        if now >= self._comet_at:
            self._comet_at = now + random.uniform(*COMET_GAP)
            for c in self.comets:
                if not c[1]:
                    self._launch_comet(c)
                    break

    @staticmethod
    def _launch_comet(c):
        ang = math.radians(random.uniform(*COMET_ANGLE))
        way = random.choice((-1.0, 1.0))          # -1 flies left, +1 flies right
        sp = random.uniform(*COMET_SPEED)
        c[1] = True
        c[2] = math.sin(ang) * way * sp
        c[3] = -math.cos(ang) * sp

        ob = c[0]
        # The mesh is built pointing head-down (-Z). Rotating about Y -- the axis
        # running into the screen -- swings it within the play plane, and -ang*way
        # is the angle that lines the streak up with the velocity above.
        ob.rotation_euler = (0.0, -ang * way, 0.0)
        # Start on the side it's flying AWAY from, so it crosses the screen
        # instead of clipping straight out of the near edge.
        x0 = random.uniform(-STAR_X, STAR_X * 0.15) if way > 0 else \
            random.uniform(-STAR_X * 0.15, STAR_X)
        ob.location = (x0, COMET_Y, STAR_TOP)
        ob.hide_viewport = False

    def _update_shards(self, dt):
        for s in self.shards:
            if not s[1]:
                continue
            t = s[5] + dt
            if t >= s[6]:
                self._kill(s)
                continue
            s[5] = t
            s[3] -= SHARD_GRAVITY * dt
            ob = s[0]
            ob.location.x += s[2] * dt
            ob.location.z += s[3] * dt
            ob.rotation_euler = (0.0, s[4] * t, 0.0)
            # Shrink to nothing instead of fading: SOLID shading has no alpha to
            # animate, and the power curve holds the shard big for most of its
            # life then snaps it away, which reads as a flash rather than a melt.
            k = (1.0 - t / s[6]) ** 0.45
            f = s[7] * k
            ob.scale = (f, f, f)

    def _kill(self, entry):
        entry[1] = False
        try:
            entry[0].hide_viewport = True
        except ReferenceError:
            pass

    def _lose_life(self, now):
        self.lives -= 1
        self.burst(self.player.location.x, PLAYER_Z, 'PLAYER')
        self.audio.play('player_die')
        for k in self.bombs:
            if k[1]:
                self._kill(k)
        if self.lives <= 0:
            self.over = True
            self.message = "GAME OVER"
            self.audio.stop_music()       # clear the air for the jingle
            self.audio.play('game_over')
        else:
            self.player.location = (0.0, 0.0, PLAYER_Z)
            self._respawn_at = now + 0.6

    def hit_button(self, x, y):
        for key, (x1, y1, x2, y2) in self._buttons.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return key
        return None

    # -- per-frame update --

    def step(self, dt, now, keys):
        # Before the game-over gate: the shot that ends the run still gets to
        # finish exploding under the panel, instead of freezing mid-air, and
        # the sky keeps drifting so the scene stays alive.
        self._update_sky(dt, now)
        self._update_shards(dt)
        if self.over:
            return

        if now >= self._respawn_at:
            dx = 0.0
            if 'LEFT_ARROW' in keys:
                dx -= 1.0
            if 'RIGHT_ARROW' in keys:
                dx += 1.0
            if dx:
                x = self.player.location.x + dx * PLAYER_SPEED * dt
                self.player.location.x = max(X_MIN, min(X_MAX, x))

        alive = self._alive_enemies()
        if not alive:
            self.wave += 1
            self.score += 500
            self.audio.play('level_up')
            self.audio.set_level(self.wave)
            self.spawn_wave()
            return

        # The swarm's heartbeat. Fixed for the whole level, like its speed.
        if now >= self._march_at:
            self._march_at = now + march_rate_for_level(self.wave)
            self.audio.march()

        if self.style == 'SOLID':
            self._spin += SPIN_SPEED * dt
            for i, e in enumerate(self.enemies):
                if e[1]:
                    e[0].rotation_euler = (SPIN_TILT, 0.0, self._spin + i * SPIN_PHASE)
        elif self.style == 'DUMMY':
            # Turntable about their own up axis, and untilted: a dummy leaning
            # like a primitive just reads as broken, and the slow spin shows off
            # that these are real models rather than flat sprites.
            self._spin += DUMMY_SPIN_SPEED * dt
            for i, e in enumerate(self.enemies):
                if e[1]:
                    e[0].rotation_euler = (0.0, 0.0, self._spin + i * SPIN_PHASE)

        # One speed for the whole level -- it does not creep up as the swarm
        # thins, only when a new level starts.
        step = self._enemy_dir * speed_for_level(self.wave) * dt
        xs = [e[0].location.x for e in alive]
        if (self._enemy_dir > 0 and max(xs) + step > X_MAX) or \
           (self._enemy_dir < 0 and min(xs) + step < X_MIN):
            self._enemy_dir *= -1.0
            for e in alive:
                e[0].location.z -= ENEMY_DROP
        else:
            for e in alive:
                e[0].location.x += step

        if min(e[0].location.z for e in alive) <= PLAYER_Z + 0.5:
            self.over = True
            self.message = "THEY GOT THROUGH"
            self.audio.stop_music()
            self.audio.play('game_over')
            return

        if random.random() < bomb_rate_for_level(self.wave) * dt:
            self._drop_bomb(random.choice(alive)[0])

        for b in self.bullets:
            if not b[1]:
                continue
            b[0].location.z += BULLET_SPEED * dt
            if b[0].location.z > TOP_Z + 1.0:
                self._kill(b)
                continue
            bx, bz = b[0].location.x, b[0].location.z
            for e in alive:
                hx, hz = e[3]
                if e[1] and abs(e[0].location.x - bx) < hx and \
                        abs(e[0].location.z - bz) < hz:
                    self.burst(e[0].location.x, e[0].location.z, 'ENEMY')
                    self.audio.play('enemy_die', 0.14)
                    self._kill(e)
                    self._kill(b)
                    self.score += SCORE_FOR[e[2]]
                    break

        for k in self.bombs:
            if not k[1]:
                continue
            k[0].location.z -= BOMB_SPEED * dt
            if k[0].location.z < PLAYER_Z - 1.5:
                self._kill(k)
                continue
            if now >= self._respawn_at and \
                    abs(k[0].location.x - self.player.location.x) < 0.55 and \
                    abs(k[0].location.z - PLAYER_Z) < 0.55:
                self._kill(k)
                self._lose_life(now)
                return


# --------------------------------------------------------------------------
# Operator
# --------------------------------------------------------------------------

# Navigation events are swallowed so the locked front view can't be nudged.
NAV = {
    'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE',
    'WHEELOUTMOUSE', 'TRACKPADPAN', 'TRACKPADZOOM', 'MOUSEROTATE', 'MOUSESMARTZOOM',
}
GAME_KEYS = {'LEFT_ARROW', 'RIGHT_ARROW', 'SPACE'}

FRONT_VIEW = Quaternion((0.7071067811865476, 0.7071067811865476, 0.0, 0.0))


class RBX_OT_BestFeature(bpy.types.Operator):
    bl_idname = "rbx.best_feature"
    bl_label = "Play " + GAME_NAME
    bl_description = "Take over the viewport for a game. Esc restores everything"

    @classmethod
    def poll(cls, context):
        return (context.area and context.area.type == 'VIEW_3D'
                and get_active() is None)

    def invoke(self, context, event):
        # Both of these break the takeover in ways that look like a crash rather
        # than a refusal, so bail out early and say which key gets them out.
        # Local view is the worse one: objects spawned by a script aren't added
        # to it, so the game would render an EMPTY field while the view is
        # already locked and the scene hidden.
        sp = context.area.spaces.active
        if getattr(sp, "local_view", None):
            self.report({'WARNING'}, 'Exit local view ("/") to play')
            return {'CANCELLED'}
        if len(getattr(sp, "region_quadviews", ())):
            self.report({'WARNING'}, 'Exit quad view ("Ctrl+Alt+Q") to play')
            return {'CANCELLED'}

        self._area = context.area
        self._space = context.area.spaces.active
        self._region = context.region
        self._keys = set()
        self._last = time.perf_counter()
        self._done = False

        game = BestFeatureGame()
        game.take_over(context, context.area, context.region)
        game.build(context)
        self._game = game
        set_active(game)

        wm = context.window_manager
        self._timer = wm.event_timer_add(1.0 / 60.0, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _finish(self, context):
        """Safe to call twice, and from any exit path. Whatever else happens the
        user's scene and viewport must come back -- a game must never be able to
        strand someone with a hidden scene and a hijacked view."""
        if self._done:
            return
        self._done = True
        try:
            context.window_manager.event_timer_remove(self._timer)
        except Exception:
            pass
        # Shut down OUR instance rather than whatever is in the store: if a later
        # script run replaced it, those objects must still get cleaned up.
        if self._game is not None:
            self._game.shutdown()
            if get_active() is self._game:
                set_active(None)
            self._game = None
        try:
            context.workspace.status_text_set(None)
            self._area.tag_redraw()
        except (ReferenceError, AttributeError):
            pass

    def cancel(self, context):
        """Blender calls this when it interrupts the modal itself -- loading a
        file, closing the window, unregistering. Without it those paths never
        reach _finish and the user is left with a hidden scene and a locked
        view, which is the one thing this game must never do."""
        self._finish(context)

    def modal(self, context, event):
        try:
            return self._modal(context, event)
        except Exception:
            # An unhandled error must not strand the user mid-takeover. Print it
            # (so the bug is still visible) and hand the viewport back.
            import traceback
            traceback.print_exc()
            self._finish(context)
            return {'CANCELLED'}

    def _modal(self, context, event):
        # Someone pulled the game out from under us (script re-run, unregister).
        # Still owe the user their scene back.
        game = get_active()
        if game is None or game is not self._game:
            self._finish(context)
            return {'FINISHED'}

        if event.type == 'ESC' and event.value == 'PRESS':
            self._finish(context)
            return {'FINISHED'}

        if event.type in NAV:
            return {'RUNNING_MODAL'}          # view stays locked

        if game.over:
            if event.type == 'MOUSEMOVE':
                hov = game.hit_button(event.mouse_region_x, event.mouse_region_y)
                if hov != game._hover:
                    game._hover = hov
                    self._area.tag_redraw()
                return {'RUNNING_MODAL'}
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                hit = game.hit_button(event.mouse_region_x, event.mouse_region_y)
                if hit == 'start':
                    game.reset()
                    self._area.tag_redraw()
                elif hit == 'quit':
                    self._finish(context)
                    return {'FINISHED'}
                return {'RUNNING_MODAL'}
            if event.type in {'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
                game.reset()
                self._area.tag_redraw()
                return {'RUNNING_MODAL'}

        if event.type == 'M' and event.value == 'PRESS':
            game.audio.toggle_mute(game.wave)
            self._area.tag_redraw()
            return {'RUNNING_MODAL'}

        if event.type in GAME_KEYS:
            if event.value == 'PRESS':
                self._keys.add(event.type)
                if event.type == 'SPACE':
                    game.fire(time.perf_counter())
            elif event.value == 'RELEASE':
                self._keys.discard(event.type)
            return {'RUNNING_MODAL'}

        # Swallow clicks so the hidden scene can't be selected mid-game.
        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'}:
            return {'RUNNING_MODAL'}

        if event.type == 'TIMER':
            now = time.perf_counter()
            dt = min(now - self._last, 0.05)   # clamp: a stall must not teleport things
            self._last = now
            game.step(dt, now, self._keys)
            # Re-assert the view every tick: cheap insurance against anything
            # that slips past the NAV filter.
            rv = self._space.region_3d
            rv.view_rotation = FRONT_VIEW.copy()
            rv.view_perspective = 'ORTHO'
            self._area.tag_redraw()

        # Swallow EVERYTHING else rather than passing it to Blender. While the
        # game runs the scene is hidden and full of game objects, so a stray
        # Ctrl+Z, Tab, X or Delete lands somewhere the user can't see -- and a
        # stray Ctrl+S would save the file with their whole scene hidden. Esc is
        # the way out, and it's on screen.
        return {'RUNNING_MODAL'}


class RBX_OT_BestFeatureUnlock(bpy.types.Operator):
    """Counts clicks on the addon panel title. Drawn as the title itself, with
    emboss off, so it reads as a plain label until the tenth click."""

    bl_idname = "rbx.best_feature_unlock"
    bl_label = ""
    bl_description = "RBX Toolbox"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        global _clicks, _unlocked
        if _unlocked:
            return {'CANCELLED'}
        _clicks += 1
        if _clicks >= UNLOCK_CLICKS:
            _unlocked = True
            self.report({'INFO'}, "%s unlocked!" % GAME_NAME)
            # The box lives in the N-panel, which will not repaint on its own
            # after an operator that changed nothing it can see.
            for area in getattr(context.screen, "areas", ()):
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        return {'FINISHED'}


CLASSES = (RBX_OT_BestFeature, RBX_OT_BestFeatureUnlock)


def register():
    # A game left running by a previous registration owns a hidden scene and a
    # hijacked viewport. Give them back before doing anything else.
    stale = get_active()
    if stale is not None:
        stale.shutdown()
        set_active(None)
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    game = get_active()
    if game is not None:
        game.shutdown()
        set_active(None)
    for c in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass
