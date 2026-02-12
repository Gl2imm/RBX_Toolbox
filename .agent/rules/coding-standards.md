
---
trigger: always_on
---

# Coding Standards

This document defines coding standards for the Blender-to-Roblox integration project. All code changes should follow these guidelines.

---

## 1. Naming Conventions (Multi-Language)

### Python (Blender Addon)
* **Variables/Functions:** `snake_case` (e.g., `def export_mesh():`)
* **Classes:** `PascalCase` (strictly for `bpy` types like `class ROBLOX_OT_Export(bpy.types.Operator):`)
* **Constants:** `UPPER_SNAKE_CASE` (e.g., `ROBLOX_API_URL`)

### Luau (Roblox)
* **Variables/Parameters:** `camelCase` (e.g., `local playerPosition`)
* **Services/Classes:** `PascalCase` (e.g., `ReplicatedStorage`)

---

## 2. Code Readability

### Break Long Lines
Split long statements into multiple lines for clarity (applies to both Lua and Python).

**Luau Example:**
```lua
-- ✅ CORRECT
local mainLabel = Instance.new("TextLabel", screenGui)
mainLabel.Name = "MainStatus"
mainLabel.Size = UDim2.new(0.6, 0, 0.1, 0)
mainLabel.Position = UDim2.new(0.2, 0, 0.1, 0)
mainLabel.BackgroundTransparency = 1

-- ❌ AVOID
local mainLabel = Instance.new("TextLabel", screenGui); mainLabel.Name = "MainStatus"; mainLabel.Size = UDim2.new(0.6, 0, 0.1, 0)
```

**Python Example:**
```python
# ✅ CORRECT
bpy.ops.mesh.primitive_cube_add(
    size=2, 
    enter_editmode=False, 
    align='WORLD', 
    location=(0, 0, 0)
)
```

### Split Complex Conditionals
Do not combine complex logic into single lines.

```lua
-- ✅ CORRECT
if isSpectating then
    lobbyActionEvent:FireServer("Spectate")
    spectateButton.Text = "TO LOBBY"
else
    lobbyActionEvent:FireServer("ToLobby")
    spectateButton.Text = "SPECTATE"
end
```

---

## 3. Blender & API Specifics

### Context Safety
* **Validation:** Never assume `bpy.context.active_object` exists. Always check `if obj is not None:` before operations.
* **Operators:** Avoid `bpy.ops` in loops where possible. Use direct data manipulation (`obj.data.vertices[0].co`) or `bmesh` for performance.

### API Error Handling
* **Network Calls:** All Roblox API requests from Python must be wrapped in `try/except` blocks to handle connection failures or 403 errors gracefully.

### .NET Library Usage (RobloxFiles)
* **Dictionaries:** When using `rbxm_net_lib` objects (e.g., `Properties`), remember they are .NET `IReadOnlyDictionary` objects, not Python dictionaries. 
  * **Incorrect:** `obj.Properties.get("Key")` (Throws AttributeError)
  * **Correct:** Check existence with `if "Key" in obj.Properties:` then access via `obj.Properties["Key"]`.
* **Reference:** Check `func_import_v2/Roblox engine API reference_for_Antigravity.txt` or `roblox-cloud` skill for API details if unsure.

---

## 4. Documentation & Comments

### Add Comments For:
* **Coordinate Conversion:** Explicitly comment where Z-up (Blender) is converted to Y-up (Roblox).
* **Bug fixes:** Explain what was broken and why the fix works.
* **Non-obvious logic:** Complex calculations or state management.

### Examples:

```python
# BUG FIX: Ensure mode is explicitly set to OBJECT before export
bpy.ops.object.mode_set(mode='OBJECT')
```

---

## 5. Indentation

* **Python:** Use **4 spaces** (Standard PEP 8).
* **Luau:** Use **Tabs** (Roblox Standard).
* **Consistency:** Do not mix tabs and spaces in the same file.

---

## 6. Roblox to Blender Coordinate Conversion

To explain the XYZ conversion between Roblox and Blender, use the following breakdown.

### The Core Coordinate Mismatch
The fundamental difference lies in which axis represents "Up" and which axis represents "Forward."

| Feature | Roblox Engine | Blender |
| :--- | :--- | :--- |
| Up Axis | +Y (0, 1, 0) | +Z (0, 0, 1) |
| Forward Axis | -Z (0, 0, -1) | -Y (0, -1, 0)* |
| Right Axis | +X (1, 0, 0) | +X (1, 0, 0) |
| Handedness | Right-Handed | Right-Handed |

*Note: In Blender, the "Front" View (Numpad 1) looks along the +Y axis. Therefore, for a character to look at the camera in Front View, they must face -Y.*

### The Conversion Formula (Math)
To convert a position vector or vertex from Roblox space to Blender space, you effectively need to rotate the world 90 degrees around the X-axis.

From Roblox $(x, y, z)$ $\rightarrow$ To Blender $(x', y', z')$:

$$
\begin{bmatrix} x' \\ y' \\ z' \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix}
$$

**Simplified Logic:**
*   Blender X = Roblox X
*   Blender Y = Roblox -Z (Swaps depth to horizontal plane)
*   Blender Z = Roblox Y (Swaps height to vertical axis)

### Practical Instructions

**A. If Importing Animations/CFrames manually:**
You must apply a rotational offset matrix. In Roblox Lua, this looks like:

```lua
local ROB_TO_BLENDER_ROTATION = CFrame.fromEulerAnglesXYZ(math.rad(90), 0, 0)
-- Apply this to the CFrame to align it with Blender's world space
```

**B. If Exporting FBX (The "Auto" Fix):**
When exporting from Blender to Roblox, do not manually rotate the mesh. Instead, change the Export Settings in the operator panel:
*   Forward: -Z Forward
*   Up: Y Up

This forces Blender's internal exporter to apply the matrix transform automatically.

**C. Scale Factor:**
*   Roblox: 1 Stud
*   Blender: 1 Meter
*   Conversion: usually 1 Stud $\approx$ 0.28 Meters (historically), but most modern pipelines use 1 Stud = 1 Meter for simplicity. Ensure you check if the imported model is 100x too small (needs 0.01 scaling) or correct.