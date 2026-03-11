"""
RBXM Reader for Roblox Binary Model Files
-----------------------------------------

Copyright (c) 2026
https://www.roblox.com/users/1244794402/profile
Papa_boss332

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use,
copy, modify, merge, publish, distribute, and/or sublicense the Software.

Conditions:
1. This notice and the attribution information below must remain intact in all
   copies or substantial portions of the Software.
2. The origin of this file must not be misrepresented.

Attribution:
Project Repository:
https://github.com/Gl2imm/RBX_Toolbox

This RBXM reader was created with the assistance of AI
(Claude Opus 4.6 Thinking) and with reference to the documentation:
https://dom.rojo.space/binary.html. Supports .rbxm and .rbxl files.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"""

import struct
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Optional

# ─────────────────────────────────────────────
#  DEBUG FLAG — set True to write to rbxm_out.txt
# ─────────────────────────────────────────────
### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

_debug_lines: list[str] = []


def _dbg(msg: str) -> None:
    """Write a debug message to the internal buffer (flushed at end if DEBUG is True)."""
    if DEBUG:
        _debug_lines.append(msg)


def _flush_debug(source_path: str) -> None:
    """Flush all accumulated debug lines to rbxm_out.txt next to the source file."""
    if not DEBUG or not _debug_lines:
        return
    out_path = os.path.join(os.path.dirname(os.path.abspath(source_path)), "rbxm_out.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(_debug_lines))
    dprint(f"[DEBUG] Output written to: {out_path}")


# ─────────────────────────────────────────────
#  Low-level byte helpers
# ─────────────────────────────────────────────

def read_bytes(data: bytes, offset: int, n: int) -> tuple[bytes, int]:
    """Read exactly n bytes from data at offset; return (bytes_read, new_offset)."""
    return data[offset:offset + n], offset + n


def read_u8(data: bytes, offset: int) -> tuple[int, int]:
    """Read a single unsigned byte."""
    return data[offset], offset + 1


def read_u16_le(data: bytes, offset: int) -> tuple[int, int]:
    """Read a little-endian unsigned 16-bit integer."""
    val = struct.unpack_from("<H", data, offset)[0]
    return val, offset + 2


def read_u32_le(data: bytes, offset: int) -> tuple[int, int]:
    """Read a little-endian unsigned 32-bit integer."""
    val = struct.unpack_from("<I", data, offset)[0]
    return val, offset + 4


def read_u32_be(data: bytes, offset: int) -> tuple[int, int]:
    """Read a big-endian unsigned 32-bit integer."""
    val = struct.unpack_from(">I", data, offset)[0]
    return val, offset + 4


def read_i32_le(data: bytes, offset: int) -> tuple[int, int]:
    """Read a little-endian signed 32-bit integer."""
    val = struct.unpack_from("<i", data, offset)[0]
    return val, offset + 4


def read_f32_le(data: bytes, offset: int) -> tuple[float, int]:
    """Read a little-endian IEEE-754 32-bit float."""
    val = struct.unpack_from("<f", data, offset)[0]
    return val, offset + 4


def read_f64_le(data: bytes, offset: int) -> tuple[float, int]:
    """Read a little-endian IEEE-754 64-bit float."""
    val = struct.unpack_from("<d", data, offset)[0]
    return val, offset + 8


# ─────────────────────────────────────────────
#  Integer transformation helpers (spec §Data Storage Notes)
# ─────────────────────────────────────────────

def untransform_i32(x: int) -> int:
    """Undo the zigzag transformation applied to Int32 values.
    Formula: (x >> 1) ^ -(x & 1)  (treating as unsigned then re-interpreting)."""
    return (x >> 1) ^ (-(x & 1))


def untransform_i64(x: int) -> int:
    """Undo the zigzag transformation applied to Int64 values (63-bit shift variant)."""
    return (x >> 1) ^ (-(x & 1))


# ─────────────────────────────────────────────
#  Byte de-interleaving (spec §Byte Interleaving)
# ─────────────────────────────────────────────

def deinterleave(data: bytes, count: int, word_size: int) -> list[bytes]:
    """Reverse byte-interleaving for an array of 'count' values each 'word_size' bytes wide.
    The format stores bytes column-by-column (all first-bytes, then all second-bytes, …)."""
    result = []
    for i in range(count):
        word = bytes(data[i + j * count] for j in range(word_size))
        result.append(word)
    return result


def deinterleave_u32_be(data: bytes, count: int) -> list[int]:
    """De-interleave an array of big-endian u32 values."""
    words = deinterleave(data, count, 4)
    return [struct.unpack(">I", w)[0] for w in words]


def deinterleave_i32(data: bytes, count: int) -> list[int]:
    """De-interleave and zigzag-untransform an array of Int32 values."""
    raw = deinterleave_u32_be(data, count)
    return [untransform_i32(v) for v in raw]


def deinterleave_i64(data: bytes, count: int) -> list[int]:
    """De-interleave and zigzag-untransform an array of Int64 values."""
    words = deinterleave(data, count, 8)
    raws = [struct.unpack(">Q", w)[0] for w in words]
    return [untransform_i64(v) for v in raws]


# ─────────────────────────────────────────────
#  Roblox float format (spec §Roblox Float Format)
# ─────────────────────────────────────────────

def roblox_float_to_ieee(rbx: int) -> float:
    """Convert a Roblox-format 32-bit float (sign bit last) to a standard IEEE-754 float.
    Roblox layout: eeeeeeee mmmmmmmm mmmmmmmm mmmmmmms
    Standard:      seeeeeee emmmmmmm mmmmmmmm mmmmmmmm"""
    sign = rbx & 1
    ieee = (sign << 31) | (rbx >> 1)
    return struct.unpack(">f", struct.pack(">I", ieee))[0]


def deinterleave_roblox_f32(data: bytes, count: int) -> list[float]:
    """De-interleave an array of Roblox-format Float32 values."""
    words = deinterleave(data, count, 4)
    return [roblox_float_to_ieee(struct.unpack(">I", w)[0]) for w in words]


# ─────────────────────────────────────────────
#  String reader (spec §String)
# ─────────────────────────────────────────────

def read_string(data: bytes, offset: int) -> tuple[str, int]:
    """Read a length-prefixed UTF-8 string (u32 length followed by raw bytes)."""
    length, offset = read_u32_le(data, offset)
    raw, offset = read_bytes(data, offset, length)
    return raw.decode("utf-8", errors="replace"), offset


# ─────────────────────────────────────────────
#  Chunk decompression
# ─────────────────────────────────────────────

def _lz4_block_decompress(src: bytes, uncompressed_len: int) -> bytes:
    """Pure-Python LZ4 block decompressor (no external libraries required).

    LZ4 block format is a series of sequences, each with:
      1. Token byte — high nibble = literal count hint, low nibble = match length hint
      2. Optional extra literal-length bytes (keep reading while byte == 255)
      3. Literal bytes copied verbatim into output
      4. 2-byte little-endian match offset (absent at the very last sequence)
      5. Optional extra match-length bytes (keep reading while byte == 255)
      6. Back-reference copy of (match_len + 4) bytes from offset bytes ago

    Reference: https://lz4.github.io/lz4/lz4_Block_format.html
    """
    dst = bytearray(uncompressed_len)
    src_pos = 0
    dst_pos = 0
    src_len = len(src)

    while src_pos < src_len:
        # ── 1. Read token ──────────────────────────────────────────────
        token = src[src_pos]
        src_pos += 1

        lit_len     = (token >> 4) & 0xF   # high nibble
        match_extra =  token       & 0xF   # low nibble (match length above minimum of 4)

        # ── 2. Extend literal length if nibble saturated at 15 ─────────
        if lit_len == 15:
            while src_pos < src_len:
                extra = src[src_pos]
                src_pos += 1
                lit_len += extra
                if extra != 255:
                    break

        # ── 3. Copy literals verbatim ──────────────────────────────────
        dst[dst_pos:dst_pos + lit_len] = src[src_pos:src_pos + lit_len]
        src_pos += lit_len
        dst_pos += lit_len

        # End of block: last sequence has no match data
        if src_pos >= src_len:
            break

        # ── 4. Read 2-byte little-endian match offset ──────────────────
        offset = src[src_pos] | (src[src_pos + 1] << 8)
        src_pos += 2
        if offset == 0:
            raise ValueError("LZ4 decompression error: zero match offset (corrupt data)")

        # ── 5. Extend match length if nibble saturated at 15 ───────────
        match_len = match_extra + 4   # minimum match length is always 4
        if match_extra == 15:
            while src_pos < src_len:
                extra = src[src_pos]
                src_pos += 1
                match_len += extra
                if extra != 255:
                    break

        # ── 6. Copy back-reference (may overlap — must be byte-by-byte) ─
        match_pos = dst_pos - offset
        if match_pos < 0:
            raise ValueError(
                f"LZ4 decompression error: match offset {offset} "
                f"exceeds current output position {dst_pos}"
            )
        for _ in range(match_len):
            dst[dst_pos] = dst[match_pos]
            dst_pos   += 1
            match_pos += 1

    return bytes(dst[:dst_pos])


def decompress_chunk(compressed: bytes, uncompressed_len: int) -> bytes:
    """Decompress a chunk body using pure-Python LZ4 or ZSTD (requires 'zstandard' package).
    If compressed is empty the data is already raw (Compressed Length == 0 in chunk header).

    Format detection:
      - First 4 bytes == 28 b5 2f fd  →  ZSTD (needs 'zstandard' pip package)
      - Anything else                 →  LZ4 block (handled in pure Python, no dependencies)
    """
    if not compressed:
        return compressed

    if compressed[:4] == b"\x28\xb5\x2f\xfd":
        # ZSTD — only external dependency that remains
        try:
            import zstandard as zstd
            dctx = zstd.ZstdDecompressor()
            return dctx.decompress(compressed)
        except ImportError:
            raise RuntimeError(
                "This chunk uses ZSTD compression. "
                "Install the 'zstandard' package to support it: pip install zstandard"
            )
    else:
        # LZ4 block — pure Python, zero dependencies
        return _lz4_block_decompress(compressed, uncompressed_len)


# ─────────────────────────────────────────────
#  Data structures
# ─────────────────────────────────────────────

@dataclass
class FileHeader:
    """Holds the 32-byte file header fields."""
    version: int
    class_count: int
    instance_count: int


@dataclass
class RawChunk:
    """Holds the raw (decompressed) bytes and 4-character name of a chunk."""
    name: str
    data: bytes


@dataclass
class InstChunk:
    """Represents one INST chunk: a class definition with its referent list."""
    class_id: int
    class_name: str
    is_service: bool
    referents: list[int]


@dataclass
class PropChunk:
    """Represents one PROP chunk: a single property for one class."""
    class_id: int
    property_name: str
    type_id: int
    values: list[Any]


@dataclass
class PrntChunk:
    """Represents the PRNT chunk: parent–child relationships."""
    child_referents: list[int]
    parent_referents: list[int]


@dataclass
class ParsedFile:
    """Top-level result of parsing an rbxm/rbxl file."""
    header: FileHeader
    metadata: dict[str, str]
    shared_strings: list[bytes]
    instances: dict[int, InstChunk]          # class_id → InstChunk
    properties: list[PropChunk]
    parent_map: dict[int, int]               # referent → parent referent (-1 = root)


# ─────────────────────────────────────────────
#  File header parser
# ─────────────────────────────────────────────

def parse_header(data: bytes) -> tuple[FileHeader, int]:
    """Parse the 32-byte file header and validate magic bytes.
    Returns (FileHeader, offset_after_header)."""
    # The spec documents the magic as b"<roblox!" but some Roblox versions
    # use b"<roblox " (space) or other trailing byte variants.
    # We only validate the stable 7-byte prefix to stay broadly compatible.
    MAGIC_PREFIX = b"<roblox"
    SIG          = b"\x89\xff\x0d\x0a\x1a\x0a"
    if data[:7] != MAGIC_PREFIX:
        raise ValueError(f"Invalid magic number: {data[:8]!r} (expected prefix {MAGIC_PREFIX!r})")
    if data[8:14] != SIG:
        raise ValueError(f"Invalid signature: {data[8:14]!r}")
    version = struct.unpack_from("<H", data, 14)[0]
    class_count = struct.unpack_from("<i", data, 16)[0]
    instance_count = struct.unpack_from("<i", data, 20)[0]
    # bytes 24-31 are reserved
    hdr = FileHeader(version=version, class_count=class_count, instance_count=instance_count)
    _dbg(f"[Header] version={version} classes={class_count} instances={instance_count}")
    return hdr, 32


# ─────────────────────────────────────────────
#  Chunk stream reader
# ─────────────────────────────────────────────

def read_chunks(data: bytes, offset: int) -> list[RawChunk]:
    """Read all chunk headers and return decompressed RawChunk objects.
    Each chunk header is 16 bytes: name(4) + compressed_len(u32) + uncompressed_len(u32) + reserved(4)."""
    chunks: list[RawChunk] = []
    while offset < len(data):
        name_bytes, offset = read_bytes(data, offset, 4)
        name = name_bytes.rstrip(b"\x00").decode("ascii")
        compressed_len, offset = read_u32_le(data, offset)
        uncompressed_len, offset = read_u32_le(data, offset)
        _reserved, offset = read_bytes(data, offset, 4)

        if compressed_len == 0:
            # Data is stored raw
            chunk_body, offset = read_bytes(data, offset, uncompressed_len)
        else:
            raw_compressed, offset = read_bytes(data, offset, compressed_len)
            chunk_body = decompress_chunk(raw_compressed, uncompressed_len)

        _dbg(f"[Chunk] name={name!r} compressed={compressed_len} uncompressed={uncompressed_len}")
        chunks.append(RawChunk(name=name, data=chunk_body))

        if name == "END":
            break
    return chunks


# ─────────────────────────────────────────────
#  Individual chunk parsers
# ─────────────────────────────────────────────

def parse_meta_chunk(data: bytes) -> dict[str, str]:
    """Parse a META chunk into a dict of string → string metadata entries."""
    offset = 0
    count, offset = read_u32_le(data, offset)
    meta: dict[str, str] = {}
    for _ in range(count):
        key, offset = read_string(data, offset)
        val, offset = read_string(data, offset)
        meta[key] = val
        _dbg(f"  [META] {key!r} = {val!r}")
    return meta


def parse_sstr_chunk(data: bytes) -> list[bytes]:
    """Parse an SSTR chunk into a list of raw shared string bytes.
    Each entry has a 16-byte MD5 hash (ignored) followed by a length-prefixed string."""
    offset = 0
    _version, offset = read_u32_le(data, offset)
    count, offset = read_u32_le(data, offset)
    strings: list[bytes] = []
    for _ in range(count):
        _md5, offset = read_bytes(data, offset, 16)          # MD5 hash — not used
        length, offset = read_u32_le(data, offset)
        raw, offset = read_bytes(data, offset, length)
        strings.append(raw)
        _dbg(f"  [SSTR] len={length}")
    return strings


def parse_inst_chunk(data: bytes) -> InstChunk:
    """Parse an INST chunk describing one Roblox class and the referents of its instances."""
    offset = 0
    class_id, offset = read_u32_le(data, offset)
    class_name, offset = read_string(data, offset)
    object_format, offset = read_u8(data, offset)
    instance_count, offset = read_u32_le(data, offset)

    # Referents are stored as an interleaved array of zigzag-transformed i32 values,
    # and must be read accumulatively.
    raw_referents = deinterleave_i32(data[offset:offset + instance_count * 4], instance_count)
    offset += instance_count * 4

    # Accumulate referents
    referents: list[int] = []
    acc = 0
    for r in raw_referents:
        acc += r
        referents.append(acc)

    is_service = (object_format == 1)
    # If service, skip the service markers (one 0x01 byte per instance)
    if is_service:
        offset += instance_count

    _dbg(f"  [INST] id={class_id} class={class_name!r} service={is_service} count={instance_count}")
    return InstChunk(class_id=class_id, class_name=class_name, is_service=is_service, referents=referents)


# ─────────────────────────────────────────────
#  PROP value readers — one per Type ID
# ─────────────────────────────────────────────

def read_prop_string(data: bytes, count: int, offset: int) -> tuple[list[str], int]:
    """Read an array of String values (Type ID 0x01). Each is length-prefixed."""
    values = []
    for _ in range(count):
        s, offset = read_string(data, offset)
        values.append(s)
    return values, offset


def read_prop_bool(data: bytes, count: int, offset: int) -> tuple[list[bool], int]:
    """Read an array of Bool values (Type ID 0x02). One byte each."""
    values = [bool(data[offset + i]) for i in range(count)]
    return values, offset + count


def read_prop_int32(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Int32 values (Type ID 0x03). Big-endian, zigzag, interleaved."""
    values = deinterleave_i32(data[offset:offset + count * 4], count)
    return values, offset + count * 4


def read_prop_float32(data: bytes, count: int, offset: int) -> tuple[list[float], int]:
    """Read an array of Float32 values (Type ID 0x04). Roblox float format, interleaved."""
    values = deinterleave_roblox_f32(data[offset:offset + count * 4], count)
    return values, offset + count * 4


def read_prop_float64(data: bytes, count: int, offset: int) -> tuple[list[float], int]:
    """Read an array of Float64 values (Type ID 0x05). Little-endian IEEE-754, no interleave."""
    values = [struct.unpack_from("<d", data, offset + i * 8)[0] for i in range(count)]
    return values, offset + count * 8


def read_prop_udim(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of UDim values (Type ID 0x06).
    Stored as interleaved Float32 scales followed by interleaved Int32 offsets."""
    scales = deinterleave_roblox_f32(data[offset:offset + count * 4], count)
    offset += count * 4
    offsets = deinterleave_i32(data[offset:offset + count * 4], count)
    offset += count * 4
    return [(scales[i], offsets[i]) for i in range(count)], offset


def read_prop_udim2(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of UDim2 values (Type ID 0x07).
    Stored as four separate interleaved arrays: X.Scale, Y.Scale, X.Offset, Y.Offset."""
    xs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    ys = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    xo = deinterleave_i32(data[offset:offset + count * 4], count);        offset += count * 4
    yo = deinterleave_i32(data[offset:offset + count * 4], count);        offset += count * 4
    return [((xs[i], xo[i]), (ys[i], yo[i])) for i in range(count)], offset


def read_prop_ray(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Ray values (Type ID 0x08).
    Each Ray is 6 little-endian f32s: Origin (X,Y,Z) then Direction (X,Y,Z)."""
    values = []
    for _ in range(count):
        ox, offset = read_f32_le(data, offset)
        oy, offset = read_f32_le(data, offset)
        oz, offset = read_f32_le(data, offset)
        dx, offset = read_f32_le(data, offset)
        dy, offset = read_f32_le(data, offset)
        dz, offset = read_f32_le(data, offset)
        values.append({"origin": (ox, oy, oz), "direction": (dx, dy, dz)})
    return values, offset


def read_prop_faces(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Faces values (Type ID 0x09). One byte per value, low 6 bits used."""
    values = list(data[offset:offset + count])
    return values, offset + count


def read_prop_axes(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Axes values (Type ID 0x0A). One byte per value, low 3 bits used."""
    values = list(data[offset:offset + count])
    return values, offset + count


def read_prop_brickcolor(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of BrickColor values (Type ID 0x0B). Interleaved big-endian u32."""
    values = deinterleave_u32_be(data[offset:offset + count * 4], count)
    return values, offset + count * 4


def read_prop_color3(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Color3 values (Type ID 0x0C).
    Stored as three separate interleaved Roblox Float32 arrays: R, G, B."""
    rs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    gs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    bs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    return [(rs[i], gs[i], bs[i]) for i in range(count)], offset


def read_prop_vector2(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Vector2 values (Type ID 0x0D).
    Stored as two separate interleaved Roblox Float32 arrays: X, Y."""
    xs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    ys = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    return [(xs[i], ys[i]) for i in range(count)], offset


def read_prop_vector3(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Vector3 values (Type ID 0x0E).
    Stored as three separate interleaved Roblox Float32 arrays: X, Y, Z."""
    xs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    ys = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    zs = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    return [(xs[i], ys[i], zs[i]) for i in range(count)], offset


# CFrame rotation ID → (Y, X, Z) rotation in degrees
CFRAME_SPECIAL_ROTATIONS: dict[int, tuple[float, float, float]] = {
    0x02: (0, 0, 0),       0x14: (0, 180, 0),
    0x03: (90, 0, 0),      0x15: (-90, -180, 0),
    0x05: (0, 180, 180),   0x17: (0, 0, 180),
    0x06: (-90, 0, 0),     0x18: (90, 180, 0),
    0x07: (0, 180, 90),    0x19: (0, 0, -90),
    0x09: (0, 90, 90),     0x1b: (0, -90, -90),
    0x0a: (0, 0, 90),      0x1c: (0, -180, -90),
    0x0c: (0, -90, 90),    0x1e: (0, 90, -90),
    0x0d: (-90, -90, 0),   0x1f: (90, 90, 0),
    0x0e: (0, -90, 0),     0x20: (0, 90, 0),
    0x10: (90, -90, 0),    0x22: (-90, 90, 0),
    0x11: (0, 90, 180),    0x23: (0, -90, 180),
}


def _read_cframe_rotations(data: bytes, count: int, offset: int) -> tuple[list[Any], int]:
    """Read the rotation parts for 'count' CFrame values.
    For each CFrame, reads the ID byte; if 0x00 reads 9 f32s for the full matrix,
    otherwise stores the special-case rotation angles from the lookup table."""
    rotations = []
    for _ in range(count):
        rot_id = data[offset]; offset += 1
        if rot_id == 0x00:
            mat = struct.unpack_from("<9f", data, offset); offset += 36
            rotations.append(("matrix", mat))
        else:
            rotations.append(("special", CFRAME_SPECIAL_ROTATIONS.get(rot_id, rot_id)))
    return rotations, offset


def read_prop_cframe(data: bytes, count: int, offset: int) -> tuple[list[dict], int]:
    """Read an array of CFrame values (Type ID 0x10).
    Rotation parts come first (one per value), then positions as an interleaved Vector3 array."""
    rotations, offset = _read_cframe_rotations(data, count, offset)
    positions, offset = read_prop_vector3(data, count, offset)
    values = [
        {"rotation": rotations[i], "position": positions[i]}
        for i in range(count)
    ]
    return values, offset


def read_prop_enum(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Enum values (Type ID 0x12). Big-endian u32, interleaved."""
    values = deinterleave_u32_be(data[offset:offset + count * 4], count)
    return values, offset + count * 4


def read_prop_referent(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Referent values (Type ID 0x13).
    Stored as interleaved zigzag i32 and must be read accumulatively."""
    raw = deinterleave_i32(data[offset:offset + count * 4], count)
    offset += count * 4
    values: list[int] = []
    acc = 0
    for r in raw:
        acc += r
        values.append(acc if acc != -1 else -1)
    return values, offset


def read_prop_vector3int16(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Vector3int16 values (Type ID 0x14). Three little-endian i16 each."""
    values = []
    for _ in range(count):
        x, offset = read_i32_le(data, offset)  # actually i16, but reading 2 bytes
        # Fix: use struct directly for i16
        x = struct.unpack_from("<h", data, offset - 4)[0]
        y = struct.unpack_from("<h", data, offset - 2)[0]
        offset -= 4  # rewind — redo properly
        x = struct.unpack_from("<h", data, offset)[0]; offset += 2
        y = struct.unpack_from("<h", data, offset)[0]; offset += 2
        z = struct.unpack_from("<h", data, offset)[0]; offset += 2
        values.append((x, y, z))
    return values, offset


def read_prop_number_sequence(data: bytes, count: int, offset: int) -> tuple[list[list], int]:
    """Read an array of NumberSequence values (Type ID 0x15).
    Each sequence starts with a u32 keypoint count, then keypoints of (time, value, envelope)."""
    sequences = []
    for _ in range(count):
        kp_count, offset = read_u32_le(data, offset)
        keypoints = []
        for _ in range(kp_count):
            t, offset = read_f32_le(data, offset)
            v, offset = read_f32_le(data, offset)
            e, offset = read_f32_le(data, offset)
            keypoints.append({"time": t, "value": v, "envelope": e})
        sequences.append(keypoints)
    return sequences, offset


def read_prop_color_sequence(data: bytes, count: int, offset: int) -> tuple[list[list], int]:
    """Read an array of ColorSequence values (Type ID 0x16).
    Each sequence starts with a u32 keypoint count, then keypoints of (time, R, G, B, envelope)."""
    sequences = []
    for _ in range(count):
        kp_count, offset = read_u32_le(data, offset)
        keypoints = []
        for _ in range(kp_count):
            t, offset  = read_f32_le(data, offset)
            r, offset  = read_f32_le(data, offset)
            g, offset  = read_f32_le(data, offset)
            b, offset  = read_f32_le(data, offset)
            _e, offset = read_f32_le(data, offset)   # envelope — unused per spec
            keypoints.append({"time": t, "color": (r, g, b)})
        sequences.append(keypoints)
    return sequences, offset


def read_prop_number_range(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of NumberRange values (Type ID 0x17). Two little-endian f32 each (min, max)."""
    values = []
    for _ in range(count):
        mn, offset = read_f32_le(data, offset)
        mx, offset = read_f32_le(data, offset)
        values.append((mn, mx))
    return values, offset


def read_prop_rect(data: bytes, count: int, offset: int) -> tuple[list[dict], int]:
    """Read an array of Rect values (Type ID 0x18).
    Stored as four interleaved Roblox Float32 arrays: Min.X, Min.Y, Max.X, Max.Y."""
    minx = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    miny = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    maxx = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    maxy = deinterleave_roblox_f32(data[offset:offset + count * 4], count); offset += count * 4
    return [{"min": (minx[i], miny[i]), "max": (maxx[i], maxy[i])} for i in range(count)], offset


def read_prop_physical_properties(data: bytes, count: int, offset: int) -> tuple[list[Any], int]:
    """Read an array of PhysicalProperties values (Type ID 0x19).
    Each starts with a bitfield byte: bit0=custom, bit1=has_acoustic_absorption.
    If custom, a CustomPhysicalProperties struct follows."""
    values = []
    for _ in range(count):
        bitfield = data[offset]; offset += 1
        is_custom = bool(bitfield & 0b01)
        has_acoustic = bool(bitfield & 0b10)
        if is_custom:
            density,           offset = read_f32_le(data, offset)
            friction,          offset = read_f32_le(data, offset)
            elasticity,        offset = read_f32_le(data, offset)
            friction_weight,   offset = read_f32_le(data, offset)
            elasticity_weight, offset = read_f32_le(data, offset)
            acoustic = 1.0
            if has_acoustic:
                acoustic, offset = read_f32_le(data, offset)
            values.append({
                "custom": True,
                "density": density, "friction": friction,
                "elasticity": elasticity, "friction_weight": friction_weight,
                "elasticity_weight": elasticity_weight,
                "acoustic_absorption": acoustic,
            })
        else:
            values.append({"custom": False})
    return values, offset


def read_prop_color3uint8(data: bytes, count: int, offset: int) -> tuple[list[tuple], int]:
    """Read an array of Color3uint8 values (Type ID 0x1A).
    Stored as three consecutive (non-interleaved) u8 arrays: R[], G[], B[]."""
    rs = data[offset:offset + count];           offset += count
    gs = data[offset:offset + count];           offset += count
    bs = data[offset:offset + count];           offset += count
    return [(rs[i], gs[i], bs[i]) for i in range(count)], offset


def read_prop_int64(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of Int64 values (Type ID 0x1B). Big-endian, zigzag, interleaved."""
    values = deinterleave_i64(data[offset:offset + count * 8], count)
    return values, offset + count * 8


def read_prop_shared_string(data: bytes, count: int, offset: int) -> tuple[list[int], int]:
    """Read an array of SharedString indices (Type ID 0x1C).
    Stored as interleaved big-endian u32 indices into the SSTR array."""
    values = deinterleave_u32_be(data[offset:offset + count * 4], count)
    return values, offset + count * 4


def read_prop_bytecode(data: bytes, count: int, offset: int) -> tuple[list[bytes], int]:
    """Read an array of Bytecode values (Type ID 0x1D). Stored identically to String (length-prefixed bytes)."""
    values = []
    for _ in range(count):
        length, offset = read_u32_le(data, offset)
        raw, offset = read_bytes(data, offset, length)
        values.append(raw)
    return values, offset

def read_prop_rawbytes(data: bytes, count: int, offset: int) -> tuple[list[bytes], int]:
    """Read an array of String-typed props as raw bytes (no UTF-8 decode).
    Used for properties like ValuesAndTimes that store binary data in a String field."""
    values = []
    for _ in range(count):
        length, offset = read_u32_le(data, offset)
        raw, offset = read_bytes(data, offset, length)
        values.append(raw)
    return values, offset


def read_prop_optional_cframe(data: bytes, count: int, offset: int) -> tuple[list[Any], int]:
    """Read an array of OptionalCoordinateFrame values (Type ID 0x1E).
    The type ID 0x10 (CFrame) immediately follows the outer type ID, then Bool presence flags come last."""
    # Skip the inner CFrame type ID byte
    _inner_type, offset = read_u8(data, offset)
    # Read CFrame rotation parts
    rotations, offset = _read_cframe_rotations(data, count, offset)
    # Read CFrame positions
    positions, offset = read_prop_vector3(data, count, offset)
    # Read Bool presence array (preceded by Bool type ID 0x02)
    _bool_type, offset = read_u8(data, offset)
    presence = [bool(data[offset + i]) for i in range(count)]
    offset += count
    values = []
    for i in range(count):
        if presence[i]:
            values.append({"rotation": rotations[i], "position": positions[i]})
        else:
            values.append(None)
    return values, offset


def read_prop_unique_id(data: bytes, count: int, offset: int) -> tuple[list[dict], int]:
    """Read an array of UniqueId values (Type ID 0x1F).
    Each is: Index(u32) + Time(u32) + Random(i64), byte-interleaved across the whole array."""
    # Each UniqueId is 16 bytes (4+4+8)
    words = deinterleave(data[offset:offset + count * 16], count, 16)
    offset += count * 16
    values = []
    for w in words:
        index  = struct.unpack_from("<I", w, 0)[0]
        time   = struct.unpack_from("<I", w, 4)[0]
        random = struct.unpack_from("<q", w, 8)[0]
        values.append({"index": index, "time": time, "random": random})
    return values, offset


def read_prop_font(data: bytes, count: int, offset: int) -> tuple[list[dict], int]:
    """Read an array of Font values (Type ID 0x20).
    Each font is: Family(String) + Weight(u16 LE) + Style(u8) + CachedFaceId(String)."""
    values = []
    for _ in range(count):
        family,       offset = read_string(data, offset)
        weight        = struct.unpack_from("<H", data, offset)[0]; offset += 2
        style         = data[offset]; offset += 1
        cached_face,  offset = read_string(data, offset)
        values.append({"family": family, "weight": weight, "style": style, "cached_face_id": cached_face})
    return values, offset


def read_prop_content(data: bytes, count: int, offset: int) -> tuple[list[Any], int]:
    """Read an array of Content values (Type ID 0x22).
    Layout: SourceTypes (Enum array) + UriCount + Uris + ObjectCount + ObjectRefs +
            ExternalObjectCount + ExternalObjectRefs."""
    source_types, offset = read_prop_enum(data, count, offset)

    uri_count, offset = read_u32_le(data, offset)
    uris: list[str] = []
    for _ in range(uri_count):
        s, offset = read_string(data, offset)
        uris.append(s)

    obj_count, offset = read_u32_le(data, offset)
    obj_refs, offset  = read_prop_referent(data, obj_count, offset)

    ext_count, offset = read_u32_le(data, offset)
    ext_refs, offset  = read_prop_referent(data, ext_count, offset)

    # Reconstruct per-instance Content values from source_types
    uri_iter = iter(uris)
    obj_iter = iter(obj_refs)
    values = []
    for stype in source_types:
        if stype == 0:
            values.append({"type": "None"})
        elif stype == 1:
            values.append({"type": "Uri", "uri": next(uri_iter, None)})
        elif stype == 2:
            values.append({"type": "Object", "ref": next(obj_iter, None)})
        else:
            values.append({"type": "Unknown", "raw": stype})
    return values, offset


# ─────────────────────────────────────────────
#  Dispatch table: type_id → reader function
# ─────────────────────────────────────────────

PROP_READERS = {
    0x01: read_prop_string,
    0x02: read_prop_bool,
    0x03: read_prop_int32,
    0x04: read_prop_float32,
    0x05: read_prop_float64,
    0x06: read_prop_udim,
    0x07: read_prop_udim2,
    0x08: read_prop_ray,
    0x09: read_prop_faces,
    0x0a: read_prop_axes,
    0x0b: read_prop_brickcolor,
    0x0c: read_prop_color3,
    0x0d: read_prop_vector2,
    0x0e: read_prop_vector3,
    0x10: read_prop_cframe,
    0x12: read_prop_enum,
    0x13: read_prop_referent,
    0x14: read_prop_vector3int16,
    0x15: read_prop_number_sequence,
    0x16: read_prop_color_sequence,
    0x17: read_prop_number_range,
    0x18: read_prop_rect,
    0x19: read_prop_physical_properties,
    0x1a: read_prop_color3uint8,
    0x1b: read_prop_int64,
    0x1c: read_prop_shared_string,
    0x1d: read_prop_bytecode,
    0x1e: read_prop_optional_cframe,
    0x1f: read_prop_unique_id,
    0x20: read_prop_font,
    0x22: read_prop_content,
}

TYPE_NAMES = {
    0x01: "String",         0x02: "Bool",           0x03: "Int32",
    0x04: "Float32",        0x05: "Float64",         0x06: "UDim",
    0x07: "UDim2",          0x08: "Ray",             0x09: "Faces",
    0x0a: "Axes",           0x0b: "BrickColor",      0x0c: "Color3",
    0x0d: "Vector2",        0x0e: "Vector3",         0x10: "CFrame",
    0x12: "Enum",           0x13: "Referent",        0x14: "Vector3int16",
    0x15: "NumberSequence", 0x16: "ColorSequence",   0x17: "NumberRange",
    0x18: "Rect",           0x19: "PhysicalProperties",
    0x1a: "Color3uint8",    0x1b: "Int64",           0x1c: "SharedString",
    0x1d: "Bytecode",       0x1e: "OptionalCoordinateFrame",
    0x1f: "UniqueId",       0x20: "Font",            0x22: "Content",
}


def parse_prop_chunk(data: bytes, instance_counts: dict[int, int]) -> PropChunk:
    """Parse a PROP chunk for one property on one class.
    Dispatches to the appropriate type reader based on the Type ID byte."""
    offset = 0
    class_id, offset = read_u32_le(data, offset)
    prop_name, offset = read_string(data, offset)
    type_id, offset = read_u8(data, offset)

    count = instance_counts.get(class_id, 0)
    type_name = TYPE_NAMES.get(type_id, f"Unknown(0x{type_id:02x})")
    _dbg(f"  [PROP] class={class_id} prop={prop_name!r} type={type_name} count={count}")

    # Properties that use String type but contain raw binary data.
    # Decoding them as UTF-8 (the normal String path) corrupts the bytes.
    BINARY_STRING_PROPS = {"ValuesAndTimes"}

    if type_id == 0x01 and prop_name in BINARY_STRING_PROPS:
        reader = read_prop_rawbytes
    else:
        reader = PROP_READERS.get(type_id)

    if reader is None:
        _dbg(f"    WARNING: No reader for type 0x{type_id:02x}, skipping.")
        values: list[Any] = []
    else:
        try:
            values, _ = reader(data, count, offset)
        except Exception as exc:
            _dbg(f"    ERROR reading prop {prop_name!r}: {exc}")
            values = []

    return PropChunk(class_id=class_id, property_name=prop_name, type_id=type_id, values=values)


def parse_prnt_chunk(data: bytes) -> PrntChunk:
    """Parse the PRNT chunk to extract child->parent referent pairs.

    Both child and parent referent arrays are delta-encoded (accumulated) zigzag i32s.
    The null parent sentinel is -1 AFTER accumulation -- it must NOT be checked on the
    raw delta value, which would incorrectly break accumulation for subsequent entries.

    Root instances (no parent in the hierarchy) have an accumulated parent value of -1.
    """
    offset = 0
    _version, offset = read_u8(data, offset)
    count, offset = read_u32_le(data, offset)

    raw_children = deinterleave_i32(data[offset:offset + count * 4], count); offset += count * 4
    raw_parents  = deinterleave_i32(data[offset:offset + count * 4], count); offset += count * 4

    # Always accumulate both arrays unconditionally.
    # The null sentinel -1 is the *accumulated* result, not a magic delta value.
    # Checking the delta directly (the previous bug) caused parent refs to desync
    # for any instance that came after a root-level sibling.
    children: list[int] = []
    parents:  list[int] = []
    cacc = 0
    pacc = 0
    for c, p in zip(raw_children, raw_parents):
        cacc += c
        children.append(cacc)
        pacc += p
        parents.append(pacc)   # -1 here means null parent (root instance)

    _dbg(f"  [PRNT] {count} relationships  roots={parents.count(-1)}")
    return PrntChunk(child_referents=children, parent_referents=parents)


# ─────────────────────────────────────────────
#  High-level Instance object
# ─────────────────────────────────────────────

class Instance:
    """A single Roblox instance with friendly attribute and method access.

    Attributes
    ----------
    referent    : int               unique integer ID inside the file
    class_name  : str               Roblox class, e.g. "Part", "Model", "Script"
    properties  : dict[str, Any]    all properties keyed by their Roblox name
    parent      : Instance | None   parent instance (None if root)
    children    : list[Instance]    direct children
    """

    def __init__(self, referent: int, class_name: str) -> None:
        """Initialise an Instance with its referent ID and class name."""
        self.referent:   int                  = referent
        self.class_name: str                  = class_name
        self.properties: dict[str, Any]       = {}
        self.parent:     "Optional[Instance]" = None
        self.children:   "list[Instance]"     = []

    # ── convenience properties ──────────────────────────────────────────

    @property
    def name(self) -> str:
        """The value of the 'Name' property, or an empty string if not present."""
        return self.properties.get("Name", "")

    # ── read methods ────────────────────────────────────────────────────

    def get(self, property_name: str, default: Any = None) -> Any:
        """Return the value of a property by name, or default if not found.

        Usage::
            size  = inst.get("Size")
            color = inst.get("BrickColor", 0)
        """
        return self.properties.get(property_name, default)

    def GetName(self) -> str:
        """Return the instance's Name property (Roblox-style method name)."""
        return self.name

    def GetClass(self) -> str:
        """Return the instance's ClassName (Roblox-style method name)."""
        return self.class_name

    def GetChildren(self) -> "list[Instance]":
        """Return a list of direct child instances."""
        return list(self.children)

    def GetDescendants(self) -> "list[Instance]":
        """Return all descendants in depth-first order."""
        result: list = []
        def _walk(inst: "Instance") -> None:
            for child in inst.children:
                result.append(child)
                _walk(child)
        _walk(self)
        return result

    def GetParent(self) -> "Optional[Instance]":
        """Return the parent instance, or None if this is a root instance."""
        return self.parent

    def FindFirstChild(self, name: str) -> "Optional[Instance]":
        """Return the first direct child whose Name matches, or None."""
        for child in self.children:
            if child.name == name:
                return child
        return None

    def FindFirstChildOfClass(self, class_name: str) -> "Optional[Instance]":
        """Return the first direct child whose ClassName matches, or None."""
        for child in self.children:
            if child.class_name == class_name:
                return child
        return None

    def IsA(self, class_name: str) -> bool:
        """Return True if this instance's ClassName matches class_name."""
        return self.class_name == class_name

    def __repr__(self) -> str:
        return f'<Instance [{self.referent}] {self.class_name} "{self.name}">'

    def __getitem__(self, property_name: str) -> Any:
        """Allow dict-style property access: inst['Size']"""
        return self.properties[property_name]


# ─────────────────────────────────────────────
#  High-level RobloxModel object
# ─────────────────────────────────────────────

class RobloxModel:
    """The parsed Roblox model/place, containing all instances in a usable form.

    Attributes
    ----------
    roots         : list[Instance]    top-level instances (no parent)
    all_instances : list[Instance]    every instance in the file, flat list
    metadata      : dict[str, str]    key/value pairs from the META chunk
    """

    def __init__(
        self,
        roots: "list[Instance]",
        all_instances: "list[Instance]",
        metadata: dict,
    ) -> None:
        """Initialise the model — use parse() rather than constructing directly."""
        self.roots:         list = roots
        self.all_instances: list = all_instances
        self.metadata:      dict = metadata

    @property
    def instances(self) -> "list[Instance]":
        """Alias for all_instances — lets you write: for inst in model.instances"""
        return self.all_instances

    def GetDescendants(self) -> "list[Instance]":
        """Return every instance in the file as a flat list."""
        return list(self.all_instances)

    def FindFirstChild(self, name: str) -> "Optional[Instance]":
        """Find the first root-level instance with the given Name."""
        for inst in self.roots:
            if inst.name == name:
                return inst
        return None

    def FindFirstChildOfClass(self, class_name: str) -> "Optional[Instance]":
        """Find the first root-level instance with the given ClassName."""
        for inst in self.roots:
            if inst.class_name == class_name:
                return inst
        return None

    def FindAll(self, class_name: str) -> "list[Instance]":
        """Return all instances anywhere in the file whose ClassName matches."""
        return [i for i in self.all_instances if i.class_name == class_name]

    def FindAllByName(self, name: str) -> "list[Instance]":
        """Return all instances anywhere in the file whose Name matches."""
        return [i for i in self.all_instances if i.name == name]

    def __iter__(self):
        """Iterate over all instances: for inst in model"""
        return iter(self.all_instances)

    def __len__(self) -> int:
        return len(self.all_instances)

    def __repr__(self) -> str:
        return f'<RobloxModel {len(self.all_instances)} instance(s), {len(self.roots)} root(s)>'


# ─────────────────────────────────────────────
#  Builder: ParsedFile → RobloxModel
# ─────────────────────────────────────────────

def _build_model(parsed: ParsedFile) -> RobloxModel:
    """Convert the raw ParsedFile (chunks/referents) into a friendly RobloxModel.

    Steps:
      1. Create one Instance object per referent.
      2. Fill each instance's properties dict from all PropChunks.
      3. Wire up parent/child relationships using parent_map.
      4. Collect root instances (parent referent == -1).
    """
    # ── 1. Create Instance objects ──────────────────────────────────────
    ref_to_inst: dict = {}
    for inst_chunk in parsed.instances.values():
        for ref in inst_chunk.referents:
            ref_to_inst[ref] = Instance(referent=ref, class_name=inst_chunk.class_name)

    # ── 2. Fill properties ──────────────────────────────────────────────
    for prop in parsed.properties:
        inst_chunk = parsed.instances.get(prop.class_id)
        if inst_chunk is None:
            continue
        for ref, val in zip(inst_chunk.referents, prop.values):
            instance = ref_to_inst.get(ref)
            if instance is not None:
                instance.properties[prop.property_name] = val

    # ── 3. Wire hierarchy ───────────────────────────────────────────────
    roots: list = []
    for child_ref, parent_ref in parsed.parent_map.items():
        child_inst = ref_to_inst.get(child_ref)
        if child_inst is None:
            continue
        if parent_ref == -1:
            roots.append(child_inst)
        else:
            parent_inst = ref_to_inst.get(parent_ref)
            if parent_inst is not None:
                child_inst.parent = parent_inst
                parent_inst.children.append(child_inst)

    return RobloxModel(
        roots=roots,
        all_instances=list(ref_to_inst.values()),
        metadata=parsed.metadata,
    )



# ═════════════════════════════════════════════
#  XML FORMAT PARSER
#  Handles .rbxmx / .rbxlx and any .rbxm/.rbxl
#  that is actually XML (starts with <roblox)
# ═════════════════════════════════════════════

import xml.etree.ElementTree as _ET
import html as _html


def _xml_text(el) -> str:
    """Return stripped inner text of an XML element, or empty string if None."""
    return (el.text or "").strip()


def _xml_parse_color3(text: str) -> tuple:
    """Parse a Color3 value stored as a packed uint32 integer in XML.
    Roblox stores Color3 in XML as a single integer: 0xFFRRGGBB or 0x00RRGGBB.
    Returns (r, g, b) as floats 0.0–1.0."""
    val = int(text.strip())
    r = ((val >> 16) & 0xFF) / 255.0
    g = ((val >>  8) & 0xFF) / 255.0
    b = ((val      ) & 0xFF) / 255.0
    return (r, g, b)


def _xml_parse_vector3(el) -> tuple:
    """Parse a <Vector3> element with <X>, <Y>, <Z> children into a (x, y, z) float tuple."""
    x = float(_xml_text(el.find("X")) or "0")
    y = float(_xml_text(el.find("Y")) or "0")
    z = float(_xml_text(el.find("Z")) or "0")
    return (x, y, z)


def _xml_parse_cframe(el) -> dict:
    """Parse a <CoordinateFrame> element into the same dict format as the binary CFrame reader.
    Contains position (X,Y,Z) and a full rotation matrix (R00..R22)."""
    def f(tag):
        child = el.find(tag)
        return float(_xml_text(child)) if child is not None else 0.0
    position = (f("X"), f("Y"), f("Z"))
    matrix = (
        f("R00"), f("R01"), f("R02"),
        f("R10"), f("R11"), f("R12"),
        f("R20"), f("R21"), f("R22"),
    )
    return {"position": position, "rotation": ("matrix", matrix)}


def _xml_parse_content(el) -> dict:
    """Parse a <Content> element.
    May contain <url>...</url> for a URI value, or <null/> for no value."""
    url_el = el.find("url")
    if url_el is not None and url_el.text:
        return {"type": "Uri", "uri": url_el.text.strip()}
    return {"type": "None"}


def _xml_parse_property(prop_el) -> tuple:
    """Parse a single property XML element into (property_name, value).

    Supported XML property types and their mappings to Python values:

    XML tag          Python value
    ─────────────────────────────────────────────────────────────
    string           str
    ProtectedString  str  (HTML entities decoded)
    bool             bool
    int              int
    float            float
    double           float
    token            int  (enum value)
    BrickColor       int
    Color3           (r, g, b) floats 0-1
    Color3uint8      (r, g, b) ints 0-255
    Vector2          (x, y)
    Vector3          (x, y, z)
    CoordinateFrame  {"position": (x,y,z), "rotation": ("matrix", (9 floats))}
    UDim             (scale, offset)
    UDim2            ((xs, xo), (ys, yo))
    Ray              {"origin": (x,y,z), "direction": (x,y,z)}
    Rect             {"min": (x,y), "max": (x,y)}
    NumberRange      (min, max)
    Ref              str referent ID e.g. "RBX6", or None for null
    Content          {"type": "Uri"/"None", "uri": ...}
    """
    tag  = prop_el.tag
    name = prop_el.get("name", "")
    text = _xml_text(prop_el)

    # ── Scalar types ───────────────────────────────────────────────────
    if tag in ("string",):
        return name, text

    if tag == "ProtectedString":
        # HTML entities like &apos; &#9; &gt; are present — unescape them
        raw = prop_el.text or ""
        return name, _html.unescape(raw)

    if tag == "bool":
        return name, (text.lower() == "true")

    if tag in ("int", "BrickColor"):
        return name, int(text)

    if tag in ("float", "double"):
        return name, float(text)

    if tag in ("token",):
        return name, int(text)

    # ── Color ──────────────────────────────────────────────────────────
    if tag == "Color3":
        return name, _xml_parse_color3(text)

    if tag == "Color3uint8":
        # Stored same way as Color3 in XML (packed int), values 0-255
        val = int(text.strip())
        r = (val >> 16) & 0xFF
        g = (val >>  8) & 0xFF
        b =  val        & 0xFF
        return name, (r, g, b)

    # ── Vectors ────────────────────────────────────────────────────────
    if tag == "Vector2":
        x = float(_xml_text(prop_el.find("X")) or "0")
        y = float(_xml_text(prop_el.find("Y")) or "0")
        return name, (x, y)

    if tag == "Vector3":
        return name, _xml_parse_vector3(prop_el)

    # ── CFrame / CoordinateFrame ───────────────────────────────────────
    if tag == "CoordinateFrame":
        return name, _xml_parse_cframe(prop_el)

    # ── UDim ──────────────────────────────────────────────────────────
    if tag == "UDim":
        scale  = float(_xml_text(prop_el.find("S")) or "0")
        offset = int(  _xml_text(prop_el.find("O")) or "0")
        return name, (scale, offset)

    if tag == "UDim2":
        xs = float(_xml_text(prop_el.find("XS")) or "0")
        xo = int(  _xml_text(prop_el.find("XO")) or "0")
        ys = float(_xml_text(prop_el.find("YS")) or "0")
        yo = int(  _xml_text(prop_el.find("YO")) or "0")
        return name, ((xs, xo), (ys, yo))

    # ── Ray ───────────────────────────────────────────────────────────
    if tag == "Ray":
        orig = prop_el.find("origin")
        dirn = prop_el.find("direction")
        origin    = _xml_parse_vector3(orig) if orig is not None else (0, 0, 0)
        direction = _xml_parse_vector3(dirn) if dirn is not None else (0, 0, 0)
        return name, {"origin": origin, "direction": direction}

    # ── Rect ──────────────────────────────────────────────────────────
    if tag == "Rect2D":
        mn = prop_el.find("min")
        mx = prop_el.find("max")
        min_v = (_xml_parse_vector3(mn)[:2] if mn is not None else (0, 0))
        max_v = (_xml_parse_vector3(mx)[:2] if mx is not None else (0, 0))
        return name, {"min": min_v, "max": max_v}

    # ── NumberRange ───────────────────────────────────────────────────
    if tag == "NumberRange":
        parts = text.split()
        mn = float(parts[0]) if len(parts) > 0 else 0.0
        mx = float(parts[1]) if len(parts) > 1 else 0.0
        return name, (mn, mx)

    # ── NumberSequence ────────────────────────────────────────────────
    if tag == "NumberSequence":
        # Format: "t v e  t v e  ..."  space-separated triples
        parts   = text.split()
        kps     = []
        for i in range(0, len(parts) - 2, 3):
            kps.append({"time": float(parts[i]), "value": float(parts[i+1]), "envelope": float(parts[i+2])})
        return name, kps

    # ── ColorSequence ─────────────────────────────────────────────────
    if tag == "ColorSequence":
        # Format: "t r g b e  t r g b e  ..." space-separated quintuples
        parts = text.split()
        kps   = []
        for i in range(0, len(parts) - 3, 5):
            kps.append({"time": float(parts[i]), "color": (float(parts[i+1]), float(parts[i+2]), float(parts[i+3]))})
        return name, kps

    # ── Ref ───────────────────────────────────────────────────────────
    if tag == "Ref":
        return name, (None if text in ("null", "nil", "") else text)

    # ── Content ───────────────────────────────────────────────────────
    if tag == "Content":
        return name, _xml_parse_content(prop_el)

    # ── PhysicalProperties ────────────────────────────────────────────
    if tag == "PhysicalProperties":
        custom_el = prop_el.find("CustomPhysics")
        if custom_el is not None and _xml_text(custom_el).lower() == "true":
            def _f(t): 
                c = prop_el.find(t)
                return float(_xml_text(c)) if c is not None else 0.0
            return name, {
                "custom": True,
                "density":           _f("Density"),
                "friction":          _f("Friction"),
                "elasticity":        _f("Elasticity"),
                "friction_weight":   _f("FrictionWeight"),
                "elasticity_weight": _f("ElasticityWeight"),
                "acoustic_absorption": _f("AcousticAbsorption"),
            }
        return name, {"custom": False}

    # ── Font ──────────────────────────────────────────────────────────
    if tag == "Font":
        def _fc(t):
            c = prop_el.find(t)
            return _xml_text(c) if c is not None else ""
        return name, {
            "family":        _fc("Family"),
            "weight":        int(_fc("Weight") or "400"),
            "style":         _fc("Style"),
            "cached_face_id": _fc("CachedFaceId"),
        }

    # ── Fallback: return raw text for unknown types ────────────────────
    _dbg(f"    [XML] Unknown property type <{tag} name={name!r}> — storing raw text")
    return name, text


def _xml_parse_item(item_el, parent_inst, all_instances: list, ref_map: dict) -> None:
    """Recursively parse an <Item> XML element and all its nested <Item> children.

    Creates an Instance object, fills its properties, links it to its parent,
    and recurses into children. Hierarchy is implicit in XML nesting — there is
    no separate PRNT chunk like in the binary format.
    """
    class_name = item_el.get("class", "Unknown")
    referent   = item_el.get("referent", "")

    inst = Instance(referent=referent, class_name=class_name)
    inst.parent = parent_inst

    if parent_inst is not None:
        parent_inst.children.append(inst)

    all_instances.append(inst)
    if referent:
        ref_map[referent] = inst

    # Parse <Properties> block
    props_el = item_el.find("Properties")
    if props_el is not None:
        for prop_el in props_el:
            try:
                prop_name, value = _xml_parse_property(prop_el)
                inst.properties[prop_name] = value
            except Exception as exc:
                _dbg(f"    [XML] Error parsing property <{prop_el.tag} name={prop_el.get('name')}>: {exc}")

    # Recurse into nested <Item> children
    for child_el in item_el.findall("Item"):
        _xml_parse_item(child_el, inst, all_instances, ref_map)


def _resolve_xml_refs(all_instances: list, ref_map: dict) -> None:
    """Replace string Ref property values with actual Instance objects.

    In XML, Ref properties are stored as strings like "RBX6". After all
    instances are built we can replace those strings with the real Instance
    objects they point to, matching what the binary parser produces.
    """
    for inst in all_instances:
        for key, val in inst.properties.items():
            if isinstance(val, str) and val in ref_map:
                inst.properties[key] = ref_map[val]


def parse_xml(file_path: str) -> "RobloxModel":
    """Parse a Roblox XML model file (.rbxmx / .rbxlx, or XML-format .rbxm/.rbxl).

    The XML format encodes hierarchy through nesting — each <Item> element
    may contain child <Item> elements. Properties use typed XML tags
    (e.g. <Vector3>, <CoordinateFrame>, <bool>) instead of binary encoding.

    Returns the same RobloxModel object as parse(), so all Instance methods
    (GetName, GetChildren, FindFirstChild, etc.) work identically.
    """
    _dbg(f"=== rbxm_parser XML: {file_path} ===")

    with open(file_path, "r", encoding="utf-8") as f:
        xml_text = f.read()

    try:
        root_el = _ET.fromstring(xml_text)
    except _ET.ParseError as e:
        raise ValueError(f"Failed to parse XML: {e}")

    all_instances: list = []
    ref_map:       dict = {}
    roots:         list = []

    # Top-level <Item> elements are root instances
    for item_el in root_el.findall("Item"):
        inst = Instance(referent=item_el.get("referent", ""), class_name=item_el.get("class", "Unknown"))
        inst.parent = None
        all_instances.append(inst)
        if inst.referent:
            ref_map[inst.referent] = inst
        roots.append(inst)

        # Parse properties
        props_el = item_el.find("Properties")
        if props_el is not None:
            for prop_el in props_el:
                try:
                    prop_name, value = _xml_parse_property(prop_el)
                    inst.properties[prop_name] = value
                except Exception as exc:
                    _dbg(f"  [XML] Error on <{prop_el.tag} name={prop_el.get('name')}>: {exc}")

        # Recurse into children
        for child_el in item_el.findall("Item"):
            _xml_parse_item(child_el, inst, all_instances, ref_map)

    # Wire Ref properties to actual Instance objects
    _resolve_xml_refs(all_instances, ref_map)

    _dbg(f"XML parsed: {len(all_instances)} instances, {len(roots)} roots")

    if DEBUG:
        _dbg("\n=== XML Instance Tree ===")
        def _xml_dump(inst, depth=0):
            _dbg("  " * depth + repr(inst))
            for c in inst.children:
                _xml_dump(c, depth + 1)
        for r in roots:
            _xml_dump(r)

    _flush_debug(file_path)
    return RobloxModel(roots=roots, all_instances=all_instances, metadata={})


# ─────────────────────────────────────────────
#  Top-level parser (returns RobloxModel)
# ─────────────────────────────────────────────

def _is_xml_file(raw: bytes) -> bool:
    """Detect whether raw file bytes are XML format.
    XML files start with <roblox (with optional BOM or whitespace).
    Binary files start with <roblox! or <roblox<space> followed by binary data."""
    # Strip UTF-8 BOM if present
    sniff = raw[:200].lstrip(b"\xef\xbb\xbf").lstrip()
    return sniff.startswith(b"<roblox") and b"xmlns" in sniff[:200]


def parse(file_path: str) -> RobloxModel:
    """Parse a Roblox model/place file — auto-detects binary or XML format.

    Supports:
      .rbxm  / .rbxl   — binary format (default) or XML format
      .rbxmx / .rbxlx  — always XML format

    Returns a RobloxModel with Instance objects ready to use.
    If DEBUG is True, writes a detailed log to rbxm_out.txt next to the source file.
    """
    with open(file_path, "rb") as f:
        raw = f.read()

    if _is_xml_file(raw):
        _dbg(f"[parse] Detected XML format: {file_path}")
        return parse_xml(file_path)

    _dbg(f"[parse] Detected binary format: {file_path}")

    _dbg(f"=== rbxm_parser: {file_path} ({len(raw)} bytes) ===")

    header, offset = parse_header(raw)
    raw_chunks = read_chunks(raw, offset)

    metadata: dict = {}
    shared_strings: list = []
    instances: dict = {}
    properties: list = []
    prnt: Optional[PrntChunk] = None

    for chunk in raw_chunks:
        if chunk.name == "META":
            metadata = parse_meta_chunk(chunk.data)
        elif chunk.name == "SSTR":
            shared_strings = parse_sstr_chunk(chunk.data)
        elif chunk.name == "INST":
            inst = parse_inst_chunk(chunk.data)
            instances[inst.class_id] = inst
        elif chunk.name == "PROP":
            instance_counts = {cid: len(i.referents) for cid, i in instances.items()}
            prop = parse_prop_chunk(chunk.data, instance_counts)
            properties.append(prop)
        elif chunk.name == "PRNT":
            prnt = parse_prnt_chunk(chunk.data)
        elif chunk.name == "END":
            _dbg("[END] Reached end chunk.")

    parent_map: dict = {}
    if prnt:
        for child, parent in zip(prnt.child_referents, prnt.parent_referents):
            parent_map[child] = parent

    raw_parsed = ParsedFile(
        header=header,
        metadata=metadata,
        shared_strings=shared_strings,
        instances=instances,
        properties=properties,
        parent_map=parent_map,
    )

    _dbg(f"Classes: {len(instances)}  Properties: {len(properties)}")

    if DEBUG:
        _dbg("\n=== Instance Tree ===")
        _dump_tree(raw_parsed)

    model = _build_model(raw_parsed)

    _dbg(f"Built RobloxModel: {len(model.all_instances)} instances, {len(model.roots)} roots")
    _flush_debug(file_path)
    return model


# ─────────────────────────────────────────────
#  Debug helper — prints a human-readable tree
# ─────────────────────────────────────────────

def _dump_tree(parsed: ParsedFile) -> None:
    """Recursively dump the instance hierarchy into the debug buffer for human inspection."""
    ref_to_class: dict = {}
    for inst in parsed.instances.values():
        for ref in inst.referents:
            ref_to_class[ref] = inst.class_name

    name_map: dict = {}
    for prop in parsed.properties:
        if prop.property_name == "Name":
            inst = parsed.instances.get(prop.class_id)
            if inst:
                for ref, val in zip(inst.referents, prop.values):
                    name_map[ref] = val

    children: dict = {}
    for child, parent in parsed.parent_map.items():
        children.setdefault(parent, []).append(child)

    def _recurse(ref: int, depth: int) -> None:
        cls  = ref_to_class.get(ref, "?")
        name = name_map.get(ref, "")
        _dbg("  " * depth + f'[{ref}] {cls}  "{name}"')
        for child_ref in sorted(children.get(ref, [])):
            _recurse(child_ref, depth + 1)

    for r in sorted(children.get(-1, [])):
        _recurse(r, 0)


# ─────────────────────────────────────────────
#  CLI entry-point
# ─────────────────────────────────────────────

def main() -> None:
    """Command-line entry point. Usage: python rbxm_parser.py <file.rbxm>"""
    if len(sys.argv) < 2:
        dprint("Usage: python rbxm_parser.py <file.rbxm|file.rbxl>")
        sys.exit(1)

    path = sys.argv[1]
    model = parse(path)

    dprint(repr(model))
    dprint(f"Metadata : {model.metadata}")
    dprint()
    for inst in model.all_instances:
        parent_name = inst.parent.name if inst.parent else "(root)"
        dprint(f"  {inst!r}  parent={parent_name!r}  props={list(inst.properties.keys())}")




'''model = parse(r"")

ks = model.FindFirstChildOfClass("CurveAnimation")

for inst in ks.GetChildren():
    dprint(inst.name, inst.class_name)
    if inst.class_name == "AnimationRigData":
        dprint(inst.properties)'''






'''if inst.class_name == "Folder":
    dprint(inst.name, inst.class_name)
    children = inst.GetChildren()
    for child in children:
        dprint(f"  {child.name}  {child.class_name}")
        for grandchild in child.GetChildren():
            dprint(f"    {grandchild.name}  {grandchild.class_name}")
    break'''


if __name__ == "__main__":
    main()





"""
# ── iterate all instances ───────────────────────────────
for inst in model.instances:
    dprint(inst)                        # <Instance [1] Part "BasePlate">
    dprint(inst.name)                   # "BasePlate"
    dprint(inst.class_name)             # "Part"
    dprint(inst.properties)             # {"Name": "BasePlate", "Size": (4,1,4), ...}

# ── Roblox-style methods ────────────────────────────────
inst.GetName()                         # "BasePlate"
inst.GetClass()                        # "Part"
inst.GetParent()                       # <Instance [0] Model "MyModel">
inst.GetChildren()                     # [<Instance ...>, ...]
inst.GetDescendants()                  # all children recursively
inst.FindFirstChild("Mesh")            # by name
inst.FindFirstChildOfClass("Script")   # by class
inst.IsA("Part")                       # True / False

# ── property access ─────────────────────────────────────
inst.get("Size")                       # (4.0, 1.0, 4.0)
inst.get("BrickColor", 0)              # with fallback default
inst["CFrame"]                         # dict-style, raises KeyError if missing

# ── model-level search ──────────────────────────────────
model.FindAll("Part")                  # all Parts in the file
model.FindAllByName("Handle")          # all instances named "Handle"
model.FindFirstChildOfClass("Model")   # first root-level Model
"""





