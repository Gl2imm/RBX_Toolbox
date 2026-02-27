"""
Draco Bitstream Decoder
=======================
A pure-Python decoder for Google Draco compressed meshes, implementing the
sequential encoding path described in Draco Bitstream Specification v2.2.

Supports:
  - Sequential mesh encoding (triangular meshes)
  - rANS entropy coding (symbol + bit modes)
  - Tagged and Raw symbol decoding schemes
  - Prediction: DIFFERENCE with WRAP / OCTAHEDRON_CANONICALIZED / DELTA transforms
  - Attribute types: GENERIC, INTEGER, QUANTIZATION, NORMALS
  - Data type reinterpretation (uint32→float32, uint64→float64, bool)

This module exposes a single public function:
    decode_draco(raw_bytes) → dict
        Returns {"vertices": [...], "normals": [...], "uvs": [...],
                 "vertexColors": [...], "faces": [...]}
"""

import struct
import math
from io import BytesIO


# ======================================================================
# Constants from Draco Bitstream Specification §27.1
# ======================================================================

# Encoder types
_ENCODER_POINT_CLOUD = 0
_ENCODER_TRIANGULAR_MESH = 1

# Encoder methods
_METHOD_SEQUENTIAL = 0
_METHOD_EDGEBREAKER = 1

# Connectivity methods for sequential encoding
_CONNECTIVITY_COMPRESSED = 0
_CONNECTIVITY_UNCOMPRESSED = 1

# Sequential attribute encoder types
_ATTR_ENC_GENERIC = 0
_ATTR_ENC_INTEGER = 1
_ATTR_ENC_QUANTIZATION = 2
_ATTR_ENC_NORMALS = 3

# Prediction schemes
_PRED_NONE = -2
_PRED_DIFFERENCE = 0

# Prediction transform types
_TRANSFORM_WRAP = 1
_TRANSFORM_NORMAL_OCTAHEDRON = 3

# Symbol decoding schemes
_SCHEME_TAGGED = 0
_SCHEME_RAW = 1

# Metadata flag
_FLAG_METADATA = 32768

# Draco data type byte sizes, indexed by type enum (0=invalid,1=i8..11=bool)
_DATA_TYPE_SIZES = [0, 1, 1, 2, 2, 4, 4, 8, 8, 4, 8, 1]

# Data type enum values for reinterpretation
_DTYPE_FLOAT32 = 9
_DTYPE_FLOAT64 = 10
_DTYPE_BOOL = 11


# ======================================================================
# Byte-level stream reader
# ======================================================================

class _StreamReader:
    """Sequential byte reader over a bytes/memoryview buffer."""

    __slots__ = ("_buf", "_pos", "_view")

    def __init__(self, data):
        if isinstance(data, memoryview):
            self._buf = data
        else:
            self._buf = memoryview(data)
        self._view = self._buf
        self._pos = 0

    # -- position control --

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, val):
        self._pos = val

    def advance(self, n):
        self._pos += n

    # -- primitive readers (little-endian) --

    def read_u8(self):
        val = self._buf[self._pos]
        self._pos += 1
        return val

    def read_i8(self):
        val = struct.unpack_from("<b", self._buf, self._pos)[0]
        self._pos += 1
        return val

    def read_u16(self):
        val = struct.unpack_from("<H", self._buf, self._pos)[0]
        self._pos += 2
        return val

    def read_u32(self):
        val = struct.unpack_from("<I", self._buf, self._pos)[0]
        self._pos += 4
        return val

    def read_i32(self):
        val = struct.unpack_from("<i", self._buf, self._pos)[0]
        self._pos += 4
        return val

    def read_u64(self):
        val = struct.unpack_from("<Q", self._buf, self._pos)[0]
        self._pos += 8
        return val

    def read_f32(self):
        val = struct.unpack_from("<f", self._buf, self._pos)[0]
        self._pos += 4
        return val

    def read_ascii(self, length):
        end = self._pos + length
        s = bytes(self._buf[self._pos:end]).decode("ascii")
        self._pos = end
        return s


# ======================================================================
# LEB128 variable-length unsigned integer (§26.1)
# ======================================================================

def _read_leb128(stream):
    """Decode a LEB128 (varUI32 / varUI64) value from the stream."""
    result = 0
    shift = 0
    while True:
        byte = stream.read_u8()
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return result


# ======================================================================
# rANS entropy decoder (§22 – Asymmetric Numeral Systems)
# ======================================================================

class _RansState:
    """Asymmetric Numeral Systems decoder supporting symbol and bit modes."""

    __slots__ = (
        "_prob_table", "_lookup", "_buf", "_buf_start",
        "_cursor", "_base", "_precision", "_state", "_p_zero",
    )

    def __init__(self):
        self._prob_table = {}
        self._lookup = []
        self._buf = None
        self._buf_start = 0
        self._cursor = 0
        self._base = 0
        self._precision = 0
        self._state = 0
        self._p_zero = 0

    # -- table construction (§22.1 – BuildSymbolTables / rans_build_look_up_table) --

    def _build_tables(self, stream, expected_total):
        num_symbols = _read_leb128(stream)
        self._prob_table = {}
        self._lookup = []

        cumulative = 0
        filled = 0

        idx = 0
        while idx < num_symbols:
            raw = stream.read_u8()
            token = raw & 3

            if token == 3:
                # Run of zero-probability symbols
                run_length = (raw >> 2) + 1
                for k in range(run_length):
                    self._prob_table[idx + k] = (0, cumulative)
                idx += run_length
            else:
                # Decode probability value with 0..2 extra bytes
                prob = raw >> 2
                for extra in range(token):
                    eb = stream.read_u8()
                    prob |= eb << (8 * (extra + 1) - 2)

                self._prob_table[idx] = (prob, cumulative)
                cumulative += prob

                # Fill lookup table entries
                while len(self._lookup) < cumulative:
                    self._lookup.append(idx)
                filled = cumulative
                idx += 1

        if cumulative != expected_total:
            raise ValueError(
                f"rANS table error: cumulative {cumulative} != expected {expected_total}"
            )

    # -- state initialization (§22.3 – ans_read_init) --

    def _init_state(self, buf_view, start_offset, data_len, base, precision):
        self._buf = buf_view
        self._buf_start = start_offset
        self._base = base
        self._precision = precision

        # Read initial state from the last bytes of the rANS data
        tag = (self._buf[self._buf_start + data_len - 1] >> 6) & 3

        if tag == 0:
            self._cursor = data_len - 1
            self._state = self._buf[self._buf_start + data_len - 1] & 0x3F
        elif tag == 1:
            self._cursor = data_len - 2
            self._state = (
                (self._buf[self._buf_start + data_len - 1] << 8)
                | self._buf[self._buf_start + data_len - 2]
            ) & 0x3FFF
        elif tag == 2:
            self._cursor = data_len - 3
            self._state = (
                (self._buf[self._buf_start + data_len - 1] << 16)
                | (self._buf[self._buf_start + data_len - 2] << 8)
                | self._buf[self._buf_start + data_len - 3]
            ) & 0x3FFFFF
        else:  # tag == 3
            self._cursor = data_len - 4
            self._state = (
                (self._buf[self._buf_start + data_len - 1] << 24)
                | (self._buf[self._buf_start + data_len - 2] << 16)
                | (self._buf[self._buf_start + data_len - 3] << 8)
                | self._buf[self._buf_start + data_len - 4]
            ) & 0x3FFFFFFF

        self._state += base

    # -- renormalize: refill state from buffer --

    def _renorm(self):
        while self._state < self._base and self._cursor > 0:
            self._cursor -= 1
            self._state = (
                (self._state << 8) | self._buf[self._buf_start + self._cursor]
            )

    # -- symbol mode (§22.4 – rans_read) --

    def setup_symbol_mode(self, stream, bit_length):
        """Initialize rANS for multi-symbol decoding."""
        prec_bits = (3 * bit_length) // 2
        prec_bits = max(12, min(20, prec_bits))
        precision = 1 << prec_bits
        base = precision * 4

        self._build_tables(stream, precision)
        data_size = _read_leb128(stream)

        self._init_state(stream._view, stream.position, data_size, base, precision)
        stream.advance(data_size)

    def decode_symbol(self):
        """Read one symbol from the rANS stream."""
        self._renorm()

        quotient = self._state // self._precision
        remainder = self._state % self._precision

        symbol = self._lookup[remainder]
        prob, cum = self._prob_table[symbol]

        self._state = quotient * prob + remainder - cum
        return symbol

    # -- bit mode (§22.5 – rabs_read) --

    def setup_bit_mode(self, stream):
        """Initialize rANS for single-bit decoding."""
        self._p_zero = stream.read_u8()
        data_size = _read_leb128(stream)
        self._init_state(stream._view, stream.position, data_size, 4096, 256)
        stream.advance(data_size)

    def decode_bit(self):
        """Read a single bit from the rANS stream."""
        self._renorm()

        quotient = self._state // self._precision
        remainder = self._state % self._precision

        threshold = self._precision - self._p_zero
        is_one = remainder < threshold

        if is_one:
            self._state = quotient * threshold + remainder
        else:
            self._state = self._state - quotient * threshold - threshold

        return 1 if is_one else 0


# ======================================================================
# Draco bitstream parser state
# ======================================================================

class _DecoderState:
    """Holds all mutable state during Draco decoding."""

    __slots__ = (
        "header", "triangle_count", "vertex_count",
        "connectivity_type", "triangle_indices",
        "attr_decoders", "attributes",
        "rans", "pending_bits", "pending_count",
    )

    def __init__(self):
        self.header = None
        self.triangle_count = 0
        self.vertex_count = 0
        self.connectivity_type = 0
        self.triangle_indices = []
        self.attr_decoders = []
        self.attributes = []
        self.rans = _RansState()
        # Bit accumulator for tagged-symbol bit reading
        self.pending_bits = 0
        self.pending_count = 0


# ======================================================================
# Header parsing (§3)
# ======================================================================

def _parse_header(stream):
    magic = stream.read_ascii(5)
    if magic != "DRACO":
        raise ValueError("Not a valid Draco bitstream (missing DRACO header)")

    major = stream.read_u8()
    minor = stream.read_u8()
    enc_type = stream.read_u8()
    enc_method = stream.read_u8()
    flags = stream.read_u16()

    return {
        "major": major,
        "minor": minor,
        "enc_type": enc_type,
        "enc_method": enc_method,
        "flags": flags,
    }


# ======================================================================
# Connectivity decoding — sequential path (§4)
# ======================================================================

def _decode_connectivity(stream, state):
    """Parse sequential connectivity: face/point counts + index buffer."""
    if state.header["enc_method"] != _METHOD_SEQUENTIAL:
        raise NotImplementedError("Only sequential mesh encoding is supported")

    state.triangle_count = _read_leb128(stream)
    state.vertex_count = _read_leb128(stream)
    state.connectivity_type = stream.read_u8()

    index_count = state.triangle_count * 3
    indices = [0] * index_count

    if state.connectivity_type == _CONNECTIVITY_COMPRESSED:
        raise NotImplementedError("Compressed sequential indices not supported")

    elif state.connectivity_type == _CONNECTIVITY_UNCOMPRESSED:
        nv = state.vertex_count
        if nv < 256:
            for i in range(index_count):
                indices[i] = stream.read_u8()
        elif nv < (1 << 16):
            for i in range(index_count):
                indices[i] = stream.read_u16()
        elif nv < (1 << 21):
            for i in range(index_count):
                indices[i] = _read_leb128(stream)
        else:
            for i in range(index_count):
                indices[i] = stream.read_u32()
    else:
        raise ValueError(
            f"Unknown connectivity method: {state.connectivity_type}"
        )

    state.triangle_indices = indices


# ======================================================================
# Attribute descriptor parsing (§11.1 – ParseAttributeDecodersData)
# ======================================================================

def _parse_attribute_descriptors(stream, state):
    """Read attribute decoder groups and per-attribute metadata."""
    num_groups = stream.read_u8()
    state.attr_decoders = []

    for g in range(num_groups):
        state.attr_decoders.append({
            "index": g,
            "attrs": None,
            "point_ids": None,
        })

    # EdgeBreaker-specific fields (not used in sequential path, but must be
    # consumed if present)
    if state.header["enc_method"] == _METHOD_EDGEBREAKER:
        for dec in state.attr_decoders:
            dec["data_id"] = stream.read_u8()
            dec["dec_type"] = stream.read_u8()
            dec["traversal"] = stream.read_u8()

    for dec in state.attr_decoders:
        attr_count = _read_leb128(stream)
        attrs = []
        for _ in range(attr_count):
            a_type = stream.read_u8()
            d_type = stream.read_u8()
            n_comp = stream.read_u8()
            norm = stream.read_u8()
            uid = _read_leb128(stream)
            attrs.append({
                "attr_type": a_type,
                "data_type": d_type,
                "components": n_comp,
                "normalized": norm,
                "unique_id": uid,
                "seq_type": None,   # filled next
                "values": None,     # decoded output
            })
        # Per-attribute sequential encoder type
        for a in attrs:
            a["seq_type"] = stream.read_u8()
        dec["attrs"] = attrs


# ======================================================================
# Point-ID sequence generation (§11 – GenerateSequence)
# ======================================================================

def _generate_point_ids(state):
    """For sequential encoding, each point maps to itself."""
    if state.header["enc_method"] != _METHOD_SEQUENTIAL:
        raise NotImplementedError("Only sequential encoding is supported")
    for dec in state.attr_decoders:
        dec["point_ids"] = list(range(state.vertex_count))


# ======================================================================
# Bitwise reading helpers for tagged-symbol decoding (§22.8)
# ======================================================================

def _read_n_bits(stream, state, n):
    """Read *n* bits from the byte stream, LSB first."""
    while state.pending_count < n:
        byte = stream.read_u8()
        # Insert byte bits MSB-first into the accumulator
        for i in range(8):
            state.pending_bits = (state.pending_bits << 1) | ((byte >> i) & 1)
        state.pending_count += 8

    value = 0
    for bit in range(n):
        state.pending_count -= 1
        value |= ((state.pending_bits >> state.pending_count) & 1) << bit
    return value


def _flush_pending_bits(state):
    state.pending_bits = 0
    state.pending_count = 0


# ======================================================================
# Symbol decoding (§21 – DecodeSymbols)
# ======================================================================

def _decode_symbols(stream, state, total_values, components, output):
    """
    Decode *total_values* integer symbols into *output* using either
    tagged or raw rANS scheme.
    """
    scheme = stream.read_u8()

    if scheme == _SCHEME_TAGGED:
        state.rans.setup_symbol_mode(stream, 5)
        for i in range(0, total_values, components):
            num_bits = state.rans.decode_symbol()
            for j in range(components):
                output[i + j] = _read_n_bits(stream, state, num_bits)
        _flush_pending_bits(state)

    elif scheme == _SCHEME_RAW:
        max_bit_len = stream.read_u8()
        state.rans.setup_symbol_mode(stream, max_bit_len)
        for i in range(total_values):
            output[i] = state.rans.decode_symbol()

    else:
        raise ValueError(f"Unknown symbol decoding scheme: {scheme}")


# ======================================================================
# Zigzag signed-integer conversion (§12.4)
# ======================================================================

def _zigzag_to_signed(output):
    """
    Convert unsigned zigzag-encoded values to signed integers in-place.
    Mapping: 0→0, 1→-1, 2→1, 3→-2, ...
    """
    for i in range(len(output)):
        val = output[i]
        if val & 1:
            output[i] = -((val >> 1) & 0x7FFFFFFF) - 1
        else:
            output[i] = (val >> 1) & 0x7FFFFFFF


# ======================================================================
# Prediction data parsing (§16 – DecodePredictionData)
# ======================================================================

def _read_prediction_data(stream, attr, pred_scheme, transform_type):
    """Read any extra data required by the prediction scheme + transform."""
    # Most prediction schemes beyond DIFFERENCE need EdgeBreaker which we don't
    # support; DIFFERENCE has no extra scheme data.

    # Transform data (§16.1)
    if transform_type == _TRANSFORM_WRAP:
        attr["wrap_min"] = stream.read_i32()
        attr["wrap_max"] = stream.read_i32()
    elif transform_type == _TRANSFORM_NORMAL_OCTAHEDRON:
        attr["octa_max_q"] = stream.read_i32()
        stream.read_i32()  # unused center value


# ======================================================================
# Prediction original-value reconstruction (§19 – ComputeOriginalValues)
# ======================================================================

def _reconstruct_original_values(
    attr, total_values, components, pred_scheme, transform_type, output
):
    """
    Apply prediction scheme + inverse transform to recover original
    attribute values from the correction array stored in *output*.
    """
    if pred_scheme != _PRED_DIFFERENCE:
        raise NotImplementedError(
            f"Prediction scheme {pred_scheme} requires EdgeBreaker"
        )

    # Select the inverse-transform function based on transform type
    if transform_type == _TRANSFORM_WRAP:
        _reconstruct_wrap(attr, total_values, components, output)
    elif transform_type == _TRANSFORM_NORMAL_OCTAHEDRON:
        _reconstruct_octahedron(attr, total_values, components, output)
    else:
        # Default delta: D(i) = D(i) + D(i-1)
        _reconstruct_delta(total_values, components, output)


# -- Wrap transform (§19.5) --

def _reconstruct_wrap(attr, total_values, components, output):
    lo = attr["wrap_min"]
    hi = attr["wrap_max"]
    span = 1 + hi - lo

    def _apply(pred_arr, pi, corr_arr, ci, dest_arr, di):
        for c in range(components):
            clamped = max(lo, min(hi, pred_arr[pi + c]))
            val = clamped + corr_arr[ci + c]
            if val > hi:
                val -= span
            elif val < lo:
                val += span
            dest_arr[di + c] = val

    zeros = [0] * components
    _apply(zeros, 0, output, 0, output, 0)
    for i in range(components, total_values, components):
        _apply(output, i - components, output, i, output, i)


# -- Octahedral normal canonicalized transform (§19.1–19.4) --

def _reconstruct_octahedron(attr, total_values, components, output):
    max_quantized = (1 << attr["octa_max_q"]) - 1
    max_val = max_quantized - 1
    center = max_val / 2

    def _mod_max(x):
        if x > center:
            return x - max_quantized
        if x < -center:
            return x + max_quantized
        return x

    def _flip_diamond(s, t):
        """Reflect (s,t) across the diamond boundary (§19.2 InvertDiamond)."""
        if s >= 0 and t >= 0:
            ss, st = 1, 1
        elif s <= 0 and t <= 0:
            ss, st = -1, -1
        else:
            ss = 1 if s > 0 else -1
            st = 1 if t > 0 else -1

        cs = ss * center
        ct = st * center
        us = t + t - ct
        ut = s + s - cs

        if ss * st >= 0:
            us, ut = -us, -ut

        return (us + cs) / 2, (ut + ct) / 2

    def _rotation_count(px, py):
        if px == 0:
            if py == 0:
                return 0
            return 3 if py > 0 else 1
        if px > 0:
            return 2 if py >= 0 else 1
        return 0 if py <= 0 else 3

    def _rotate(pt, count):
        if count == 1:
            return [pt[1], -pt[0]]
        if count == 2:
            return [-pt[0], -pt[1]]
        if count == 3:
            return [-pt[1], pt[0]]
        return list(pt)

    def _unsigned_add(a, b):
        """Unsigned 32-bit addition matching JS >>> 0 semantics."""
        ua = a + 4294967296 if a < 0 else a
        ub = b + 4294967296 if b < 0 else b
        return ua + ub

    def _apply(pred_arr, pi, corr_arr, ci, dest_arr, di):
        pred = [
            pred_arr[pi] - center,
            pred_arr[pi + 1] - center,
        ]
        corr = [corr_arr[ci], corr_arr[ci + 1]]

        in_diamond = abs(pred[0]) + abs(pred[1]) <= center
        if not in_diamond:
            pred[0], pred[1] = _flip_diamond(pred[0], pred[1])

        in_bottom_left = (
            (pred[0] == 0 and pred[1] == 0)
            or (pred[0] < 0 and pred[1] <= 0)
        )
        rot = _rotation_count(pred[0], pred[1])

        if not in_bottom_left:
            pred = _rotate(pred, rot)

        orig = [
            _mod_max(_unsigned_add(pred[0], corr[0])),
            _mod_max(_unsigned_add(pred[1], corr[1])),
        ]

        if not in_bottom_left:
            orig = _rotate(orig, (4 - rot) % 4)

        if not in_diamond:
            orig[0], orig[1] = _flip_diamond(orig[0], orig[1])

        dest_arr[di] = orig[0] + center
        dest_arr[di + 1] = orig[1] + center

    zeros = [0] * components
    _apply(zeros, 0, output, 0, output, 0)
    for i in range(components, total_values, components):
        _apply(output, i - components, output, i, output, i)


# -- Default delta transform --

def _reconstruct_delta(total_values, components, output):
    """D(i) = D(i) + D(i-1) — simple cumulative addition."""
    for i in range(components, total_values, components):
        for c in range(components):
            output[i + c] += output[i - components + c]


# ======================================================================
# Attribute value decoders (§12 – DecodePortableAttribute)
# ======================================================================

def _decode_generic_attribute(stream, dec, attr):
    """Read raw uncompressed attribute values based on data type size."""
    point_count = len(dec["point_ids"])
    comp = attr["components"]
    total = point_count * comp

    vals = [0] * total
    elem_size = _DATA_TYPE_SIZES[attr["data_type"]] if attr["data_type"] < len(_DATA_TYPE_SIZES) else 0

    if elem_size == 1:
        for k in range(total):
            vals[k] = stream.read_u8()
    elif elem_size == 2:
        for k in range(total):
            vals[k] = stream.read_u16()
    elif elem_size == 4:
        for k in range(total):
            vals[k] = stream.read_u32()
    elif elem_size == 8:
        for k in range(total):
            vals[k] = stream.read_u64()

    attr["values"] = vals


def _decode_compressed_attribute(stream, state, dec, attr, seq_type):
    """
    Decode an integer-encoded attribute: read prediction scheme, decode
    symbols, apply zigzag and prediction transforms.
    """
    pred_scheme = stream.read_u8()
    attr["pred_scheme"] = pred_scheme

    transform_type = None
    if pred_scheme != _PRED_NONE:
        transform_type = stream.read_i8()
        attr["transform_type"] = transform_type

    is_compressed = stream.read_u8()

    point_count = len(dec["point_ids"])
    comp = attr["components"]

    # Normal encoder in DIFFERENCE mode uses 2 components (octahedral coords)
    if seq_type == _ATTR_ENC_NORMALS and pred_scheme == _PRED_DIFFERENCE:
        comp = 2

    total = point_count * comp
    vals = [0] * total
    attr["values"] = vals

    if is_compressed > 0:
        _decode_symbols(stream, state, total, comp, vals)
    else:
        # Uncompressed fallback within the compressed path
        elem_size = stream.read_u8()
        if elem_size == 1:
            for k in range(total):
                vals[k] = stream.read_u8()
        elif elem_size == 2:
            for k in range(total):
                vals[k] = stream.read_u16()
        elif elem_size == 4:
            for k in range(total):
                vals[k] = stream.read_u32()
        elif elem_size == 8:
            for k in range(total):
                vals[k] = stream.read_u64()

    # Zigzag decode to signed (skip for octahedral normal transform which
    # uses unsigned values directly)
    if total > 0 and transform_type != _TRANSFORM_NORMAL_OCTAHEDRON:
        _zigzag_to_signed(vals)

    # Prediction reconstruction
    if pred_scheme != _PRED_NONE:
        _read_prediction_data(stream, attr, pred_scheme, transform_type)
        if total > 0:
            _reconstruct_original_values(
                attr, total, comp, pred_scheme, transform_type, vals
            )


# ======================================================================
# Attribute post-processing / dequantization transforms (§14, §15)
# ======================================================================

def _dequantize_attribute(stream, dec, attr):
    """
    Quantization inverse: read min/range/bits, then
    value = min + quantized * (range / maxQuantized).
    """
    comp = attr["components"]
    total = len(dec["point_ids"]) * comp
    vals = attr["values"]

    min_vals = [stream.read_f32() for _ in range(comp)]
    value_range = stream.read_f32()
    quant_bits = stream.read_u8()

    max_q = (1 << quant_bits) - 1
    step = value_range / max_q if max_q > 0 else 0.0

    for i in range(0, total, comp):
        for c in range(comp):
            vals[i + c] = min_vals[c] + vals[i + c] * step


def _dequantize_normals(stream, dec, attr):
    """
    Octahedral normal dequantization: convert 2-component quantized
    octahedral coordinates back to 3-component unit normals.
    """
    total_2 = len(dec["point_ids"]) * 2
    inp = attr["values"]
    out = []

    quant_bits = stream.read_u8()
    max_val = (1 << quant_bits) - 2
    scale = 2.0 / max_val if max_val > 0 else 0.0

    for i in range(0, total_2, 2):
        # Map quantized coords to [-1, 1]
        ny = inp[i] * scale - 1.0
        nz = inp[i + 1] * scale - 1.0

        # Octahedron unfolding
        nx = 1.0 - abs(ny) - abs(nz)

        # Fold-over correction for the lower hemisphere
        fold = max(0.0, -nx)
        ny += fold if ny < 0 else -fold
        nz += fold if nz < 0 else -fold

        # Normalize to unit length
        length_sq = nx * nx + ny * ny + nz * nz
        if length_sq < 1e-12:
            out.extend([0.0, 0.0, 0.0])
        else:
            inv_len = 1.0 / math.sqrt(length_sq)
            out.extend([nx * inv_len, ny * inv_len, nz * inv_len])

    attr["values"] = out


def _reinterpret_generic(attr):
    """
    For generic/integer attributes: reinterpret raw uint32 bits as float32,
    uint64 as float64, or int as bool, matching the declared data type.
    """
    vals = attr["values"]
    dt = attr["data_type"]

    if dt == _DTYPE_FLOAT32:
        for i in range(len(vals)):
            vals[i] = struct.unpack("<f", struct.pack("<I", vals[i] & 0xFFFFFFFF))[0]
    elif dt == _DTYPE_FLOAT64:
        for i in range(len(vals)):
            vals[i] = struct.unpack(
                "<d", struct.pack("<Q", vals[i] & 0xFFFFFFFFFFFFFFFF)
            )[0]
    elif dt == _DTYPE_BOOL:
        for i in range(len(vals)):
            vals[i] = vals[i] != 0


# ======================================================================
# Main attribute decoding orchestrator (§12 – DecodeAttributes)
# ======================================================================

def _decode_all_attributes(stream, state):
    """
    Two-pass attribute decoding per the spec:
      Pass 1: decode portable attribute data (raw values / symbols)
      Pass 2: apply transforms to recover original values
    """
    state.rans = _RansState()
    state.pending_bits = 0
    state.pending_count = 0

    for dec in state.attr_decoders:
        # Pass 1 — DecodePortableAttributes
        for attr in dec["attrs"]:
            seq_type = attr["seq_type"]
            if seq_type == _ATTR_ENC_GENERIC:
                _decode_generic_attribute(stream, dec, attr)
            else:
                _decode_compressed_attribute(stream, state, dec, attr, seq_type)

        # Pass 2 — TransformAttributesToOriginalFormat
        for attr in dec["attrs"]:
            seq_type = attr["seq_type"]
            if seq_type == _ATTR_ENC_QUANTIZATION:
                _dequantize_attribute(stream, dec, attr)
            elif seq_type == _ATTR_ENC_NORMALS:
                _dequantize_normals(stream, dec, attr)
            else:
                _reinterpret_generic(attr)

    # Expose final attributes from the last decoder group
    if state.attr_decoders:
        state.attributes = state.attr_decoders[-1]["attrs"]


# ======================================================================
# Public API
# ======================================================================

def decode_draco(raw_bytes):
    """
    Decode a Draco-compressed mesh from raw bytes.

    Returns a dict with the keys used by mesh_reader.py:
        "vertices"     – flat list of floats  [x,y,z, x,y,z, ...]
        "normals"      – flat list of floats  [nx,ny,nz, ...]  or []
        "uvs"          – flat list of floats  [u,v, ...]        or []
        "vertexColors" – flat list of ints    [r,g,b,a, ...]   or None
        "faces"        – flat list of ints    [i0,i1,i2, ...]
    """
    stream = _StreamReader(raw_bytes)
    state = _DecoderState()

    # 1. Header
    state.header = _parse_header(stream)
    hdr = state.header
    print(
        f"  Draco {hdr['major']}.{hdr['minor']} | "
        f"type={hdr['enc_type']}, method={hdr['enc_method']}, "
        f"flags={hdr['flags']}"
    )

    if hdr["enc_type"] != _ENCODER_TRIANGULAR_MESH:
        raise NotImplementedError("Only triangular mesh encoding is supported")
    if hdr["flags"] & _FLAG_METADATA:
        raise NotImplementedError("Draco metadata decoding is not supported")

    # 2. Connectivity (face indices)
    _decode_connectivity(stream, state)

    # 3. Attribute descriptors
    _parse_attribute_descriptors(stream, state)

    # 4. Point-ID mapping
    _generate_point_ids(state)

    # 5. Attribute data
    _decode_all_attributes(stream, state)

    # 6. Assemble output keyed by unique_id
    #    Roblox convention: 0=position, 1=normal, 2=texcoord, 4=color
    result = {
        "vertices": [],
        "normals": [],
        "uvs": [],
        "vertexColors": None,
        "faces": state.triangle_indices,
    }

    for attr in state.attributes:
        uid = attr["unique_id"]
        data = attr.get("values", [])
        if uid == 0:
            result["vertices"] = data
        elif uid == 1:
            result["normals"] = data
        elif uid == 2:
            result["uvs"] = data
        elif uid == 4:
            result["vertexColors"] = data

    return result
