"""
model_reader.py - Pure Python RBXM/RBXL binary and XML parser.
Converted from ModelParser.js (.agent/ModelParser.js).

Usage:
    with open("model.rbxm", "rb") as f:
        data = f.read()
    result = RBXModelParser.parse(data)
    # result['result'] is a list of top-level RBXInstance objects
    # result['meta'] is a dict of metadata
"""



import struct
import xml.etree.ElementTree as ET
from io import BytesIO
import base64
import re


# ─────────────────────────────────────────────
# Pure Python LZ4 Block Decompressor
# ─────────────────────────────────────────────
def _lz4_block_decompress(data, uncompressed_size):
    """Decompress LZ4 block format. No external dependency needed."""
    src = data
    src_len = len(src)
    dst = bytearray(uncompressed_size)
    si = 0  # source index
    di = 0  # destination index

    while si < src_len:
        # Read token
        token = src[si]
        si += 1

        # Literal length
        lit_len = (token >> 4) & 0x0F
        if lit_len == 15:
            while True:
                extra = src[si]
                si += 1
                lit_len += extra
                if extra != 255:
                    break

        # Copy literals
        dst[di:di + lit_len] = src[si:si + lit_len]
        si += lit_len
        di += lit_len

        # Check if we've reached the end (last sequence has no match)
        if si >= src_len:
            break

        # Read match offset (2 bytes, little-endian)
        offset = src[si] | (src[si + 1] << 8)
        si += 2
        if offset == 0:
            raise ValueError("LZ4: invalid offset 0")

        # Match length
        match_len = (token & 0x0F) + 4  # minimum match = 4
        if (token & 0x0F) == 15:
            while True:
                extra = src[si]
                si += 1
                match_len += extra
                if extra != 255:
                    break

        # Copy match (byte-by-byte to handle overlapping)
        match_pos = di - offset
        for _ in range(match_len):
            dst[di] = dst[match_pos]
            di += 1
            match_pos += 1

    return bytes(dst[:di])


### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


# ─────────────────────────────────────────────
# Data Type Names (index = type byte in PROP)
# ─────────────────────────────────────────────
RBX_DATA_TYPES = [
    "Unknown", "string", "bool", "int", "float", "double",
    "UDim", "UDim2", "Ray", "Faces", "Axes", "BrickColor",
    "Color3", "Vector2", "Vector3", "Vector2int16", "CFrame",
    "Quaternion", "Enum", "Instance", "Vector3int16",
    "NumberSequence", "ColorSequence", "NumberRange", "Rect2D",
    "PhysicalProperties", "Color3uint8", "int64", "SharedString",
    "UnknownScriptFormat", "Optional", "UniqueId", "Font",
    "SecurityCapabilities", "Content",
]

# CFrame orientation lookup
CFRAME_FACES = [
    [1, 0, 0], [0, 1, 0], [0, 0, 1],
    [-1, 0, 0], [0, -1, 0], [0, 0, -1],
]


# ─────────────────────────────────────────────
# ByteReader
# ─────────────────────────────────────────────
class ByteReader:
    """Binary reader with Roblox-specific interleaved integer/float helpers."""

    def __init__(self, data):
        if isinstance(data, (bytes, bytearray)):
            self._data = data
            self._view = memoryview(bytearray(data))
        elif isinstance(data, memoryview):
            self._data = bytes(data)
            self._view = data
        else:
            raise TypeError(f"ByteReader expects bytes, got {type(data)}")
        self.index = 0

    # ── position helpers ──
    def get_index(self):
        return self.index

    def set_index(self, idx):
        self.index = idx

    def get_remaining(self):
        return len(self._data) - self.index

    def get_length(self):
        return len(self._data)

    def jump(self, n):
        self.index += n

    # ── primitive reads ──
    def uint8(self):
        val = self._data[self.index]
        self.index += 1
        return val

    def uint16le(self):
        val = struct.unpack_from('<H', self._data, self.index)[0]
        self.index += 2
        return val

    def uint32le(self):
        val = struct.unpack_from('<I', self._data, self.index)[0]
        self.index += 4
        return val

    def int32le(self):
        val = struct.unpack_from('<i', self._data, self.index)[0]
        self.index += 4
        return val

    def floatle(self):
        val = struct.unpack_from('<f', self._data, self.index)[0]
        self.index += 4
        return val

    def doublele(self):
        val = struct.unpack_from('<d', self._data, self.index)[0]
        self.index += 8
        return val

    def string(self, length):
        s = self._data[self.index:self.index + length]
        self.index += length
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            return s.decode('latin-1')

    def array(self, length):
        a = self._data[self.index:self.index + length]
        self.index += length
        return a

    def match(self, expected):
        """Check if next bytes match the expected string. Advances index."""
        b = expected.encode('latin-1') if isinstance(expected, str) else expected
        actual = self._data[self.index:self.index + len(b)]
        self.index += len(b)
        return actual == b

    def peek_uint32le(self):
        return struct.unpack_from('<I', self._data, self.index)[0]

    # ── Roblox interleaved encodings ──
    def rbx_interleaved_uint32(self, count):
        """Read count interleaved big-endian uint32s (4 × count bytes)."""
        values = [0] * count
        raw = self._data[self.index:self.index + count * 4]
        self.index += count * 4
        for i in range(count):
            values[i] = (
                (raw[i] << 24) |
                (raw[i + count] << 16) |
                (raw[i + count * 2] << 8) |
                raw[i + count * 3]
            )
        return values

    def rbx_interleaved_int32(self, count):
        """Read count interleaved rotated int32s."""
        uints = self.rbx_interleaved_uint32(count)
        values = [0] * count
        for i in range(count):
            u = uints[i]
            # un-rotate: if low bit set → negative
            if u & 1:
                values[i] = -(u >> 1) - 1
            else:
                values[i] = u >> 1
        return values

    def rbx_interleaved_float(self, count):
        """Read count interleaved rotated floats."""
        uints = self.rbx_interleaved_uint32(count)
        values = [0.0] * count
        for i in range(count):
            u = uints[i]
            # un-rotate
            u = (u >> 1) | ((u & 1) << 31)
            values[i] = struct.unpack('<f', struct.pack('<I', u))[0]
        return values

    def rbx_interleaved_uint16(self, count):
        """Read count interleaved uint16s (2 × count bytes)."""
        values = [0] * count
        raw = self._data[self.index:self.index + count * 2]
        self.index += count * 2
        for i in range(count):
            values[i] = (raw[i] << 8) | raw[i + count]
        return values

    def rbx_interleaved_int64(self, count):
        """Read count interleaved rotated int64s (8 × count bytes)."""
        values = [0] * count
        raw = self._data[self.index:self.index + count * 8]
        self.index += count * 8
        for i in range(count):
            u = 0
            for j in range(8):
                u = (u << 8) | raw[i + count * j]
            # un-rotate
            if u & 1:
                values[i] = -(u >> 1) - 1
            else:
                values[i] = u >> 1
        return values

    def lz4_decompress(self, compressed_size, decompressed_size):
        """Decompress LZ4 data (pure Python, no external dependency)."""
        compressed = self._data[self.index:self.index + compressed_size]
        self.index += compressed_size
        return _lz4_block_decompress(compressed, decompressed_size)


# ─────────────────────────────────────────────
# RBXInstance - represents a Roblox Instance
# ─────────────────────────────────────────────
class RBXInstance:
    """Represents a Roblox Instance node in the model tree."""

    def __init__(self, class_name):
        self.Children = []
        self.Properties = {}
        self.set_property("ClassName", class_name, "string")

    def set_property(self, name, value, prop_type):
        if prop_type is not None:
            self.Properties[name] = {"type": prop_type, "value": value}
        else:
            self.Properties.pop(name, None)

    def get_property(self, name, case_insensitive=False):
        prop = self.Properties.get(name)
        if prop is None and case_insensitive:
            name_lower = name.lower()
            for k, v in self.Properties.items():
                if k.lower() == name_lower:
                    return v["value"]
            return None
        return prop["value"] if prop else None

    def find_first_child(self, name, recursive=False):
        for child in self.Children:
            if child.get_property("Name") == name:
                return child
        if recursive:
            queue = [self.Children[:]]
            while queue:
                children = queue.pop(0)
                for child in children:
                    if child.get_property("Name") == name:
                        return child
                    if child.Children:
                        queue.append(child.Children)
        return None

    def find_first_child_of_class(self, class_name, recursive=False):
        for child in self.Children:
            if child.get_property("ClassName") == class_name:
                return child
        if recursive:
            queue = [self.Children[:]]
            while queue:
                children = queue.pop(0)
                for child in children:
                    if child.get_property("ClassName") == class_name:
                        return child
                    if child.Children:
                        queue.append(child.Children)
        return None

    def __repr__(self):
        name = self.get_property("Name") or ""
        cls = self.get_property("ClassName") or "?"
        return f"RBXInstance({cls}, '{name}', {len(self.Children)} children)"


# ─────────────────────────────────────────────
# RBXBinaryParser
# ─────────────────────────────────────────────
class RBXBinaryParser:
    """Parses binary RBXM/RBXL files."""

    @staticmethod
    def parse(buffer):
        reader = ByteReader(buffer)

        # Validate header
        header_str = reader.string(7)
        assert header_str == "<roblox", f"[RBXBinaryParser] Not a valid RBXM file (got '{header_str}')"
        # Skip remaining header bytes: \x21\x89\xFF\x0D\x0A\x1A\x0A\x00\x00
        reader.jump(9)

        type_count = reader.uint32le()
        instance_count = reader.uint32le()
        reader.jump(8)  # reserved

        parser_state = {
            'instances': [None] * instance_count,
            'types': [None] * type_count,
            'shared_strings': [],
            'result': [],
            'meta': {},
        }

        # First pass: collect chunk info for decompression
        chunks = []

        while True:
            chunk_type = reader.string(4)
            com_length = reader.uint32le()
            decom_length = reader.uint32le()
            reader.jump(4)  # reserved

            chunks.append({
                'chunk_type': chunk_type,
                'com_length': com_length,
                'decom_length': decom_length,
                'data_start_index': reader.get_index(),
            })

            if com_length > 0:
                assert reader.get_remaining() >= com_length, "[RBXBinaryParser] unexpected eof"
                reader.jump(com_length)
            else:
                assert reader.get_remaining() >= decom_length, "[RBXBinaryParser] unexpected eof"
                reader.jump(decom_length)

            if chunk_type == "END\x00":
                break

        # Second pass: decompress and parse each chunk
        for chunk_info in chunks:
            chunk_type = chunk_info['chunk_type']
            com_length = chunk_info['com_length']
            decom_length = chunk_info['decom_length']
            reader.set_index(chunk_info['data_start_index'])

            if com_length == 0:
                data = reader.array(decom_length)
            else:
                # Try LZ4 decompression (also handles Zstd magic check — 
                # for pure Python we only support LZ4 here)
                peek = reader.peek_uint32le()
                if peek == 0xFD2FB528:
                    # Zstd — requires zstandard package
                    try:
                        import zstandard as zstd
                        compressed = reader.array(com_length)
                        dctx = zstd.ZstdDecompressor()
                        data = dctx.decompress(compressed, max_output_size=decom_length)
                    except ImportError:
                        dprint("[RBXBinaryParser] Zstd chunk found but 'zstandard' package not installed, skipping")
                        reader.jump(com_length)
                        continue
                else:
                    data = reader.lz4_decompress(com_length, decom_length)

            chunk_reader = ByteReader(data)

            if chunk_type == "INST":
                RBXBinaryParser._parse_INST(parser_state, chunk_reader)
            elif chunk_type == "PROP":
                RBXBinaryParser._parse_PROP(parser_state, chunk_reader)
            elif chunk_type == "PRNT":
                RBXBinaryParser._parse_PRNT(parser_state, chunk_reader)
            elif chunk_type == "SSTR":
                RBXBinaryParser._parse_SSTR(parser_state, chunk_reader)
            elif chunk_type == "META":
                RBXBinaryParser._parse_META(parser_state, chunk_reader)
            elif chunk_type == "END\x00":
                pass
            else:
                dprint(f"[RBXBinaryParser] Unknown chunk '{chunk_type}'")

        return parser_state

    @staticmethod
    def _parse_META(state, chunk):
        count = chunk.uint32le()
        for _ in range(count):
            key = chunk.string(chunk.uint32le())
            value = chunk.string(chunk.uint32le())
            state['meta'][key] = value

    @staticmethod
    def _parse_SSTR(state, chunk):
        version = chunk.uint32le()
        if version == 0:
            count = chunk.uint32le()
            for i in range(count):
                md5 = chunk.array(16)
                length = chunk.uint32le()
                value = chunk.string(length)
                state['shared_strings'].append({'md5': md5, 'value': value})
        else:
            dprint(f"[RBXBinaryParser] Unknown SSTR version {version}")

    @staticmethod
    def _parse_INST(state, chunk):
        type_id = chunk.uint32le()
        class_name = chunk.string(chunk.uint32le())
        is_service = chunk.uint8()
        count = chunk.uint32le()

        type_info = {
            'class_name': class_name,
            'instances': [],
        }
        state['types'][type_id] = type_info

        instance_ids = chunk.rbx_interleaved_int32(count)
        instance_id = 0

        for i in range(count):
            inst = RBXInstance(class_name)
            type_info['instances'].append(inst)
            instance_id += instance_ids[i]
            state['instances'][instance_id] = inst

        # Handle service trailing bytes
        if is_service:
            remaining = chunk.get_remaining()
            if is_service == 1 and remaining == count:
                chunk.jump(count)
            elif remaining > 0:
                dprint(f"[RBXBinaryParser] INST chunk {class_name}({count}) isService={is_service} has unexpected trailing data")

    @staticmethod
    def _parse_PROP(state, chunk):
        type_info = state['types'][chunk.uint32le()]
        prop_name = chunk.string(chunk.uint32le())

        if chunk.get_remaining() <= 0:
            dprint(f"[RBXBinaryParser] PROP chunk is empty")
            return

        count = len(type_info['instances'])
        values, value_type = RBXBinaryParser._parse_property_values(state, chunk, count)

        for i in range(count):
            inst = type_info['instances'][i]
            value = values[i]
            if value is not None:
                inst.set_property(prop_name, value, value_type)

    @staticmethod
    def _parse_property_values(state, chunk, count):
        """Parse property values based on the type byte. Returns (values_list, value_type_name)."""
        type_index = chunk.uint8()
        type_name = RBX_DATA_TYPES[type_index] if type_index < len(RBX_DATA_TYPES) else "Unknown"
        value_type = type_name
        values = [None] * count

        if type_name == "string":
            for i in range(count):
                values[i] = chunk.string(chunk.uint32le())

        elif type_name == "bool":
            for i in range(count):
                values[i] = chunk.uint8() != 0

        elif type_name == "int":
            values = chunk.rbx_interleaved_int32(count)

        elif type_name == "float":
            values = chunk.rbx_interleaved_float(count)

        elif type_name == "double":
            for i in range(count):
                values[i] = chunk.doublele()

        elif type_name == "UDim":
            scale = chunk.rbx_interleaved_float(count)
            offset = chunk.rbx_interleaved_int32(count)
            for i in range(count):
                values[i] = [scale[i], offset[i]]

        elif type_name == "UDim2":
            scale_x = chunk.rbx_interleaved_float(count)
            scale_y = chunk.rbx_interleaved_float(count)
            offset_x = chunk.rbx_interleaved_int32(count)
            offset_y = chunk.rbx_interleaved_int32(count)
            for i in range(count):
                values[i] = [[scale_x[i], offset_x[i]], [scale_y[i], offset_y[i]]]

        elif type_name == "Ray":
            for i in range(count):
                values[i] = [
                    [chunk.floatle(), chunk.floatle(), chunk.floatle()],
                    [chunk.floatle(), chunk.floatle(), chunk.floatle()],
                ]

        elif type_name == "Faces":
            for i in range(count):
                data = chunk.uint8()
                values[i] = {
                    'Right': bool(data & 1), 'Top': bool(data & 2),
                    'Back': bool(data & 4), 'Left': bool(data & 8),
                    'Bottom': bool(data & 16), 'Front': bool(data & 32),
                }

        elif type_name == "Axes":
            for i in range(count):
                data = chunk.uint8()
                values[i] = {'X': bool(data & 1), 'Y': bool(data & 2), 'Z': bool(data & 4)}

        elif type_name == "BrickColor":
            values = chunk.rbx_interleaved_uint32(count)

        elif type_name == "Color3":
            r = chunk.rbx_interleaved_float(count)
            g = chunk.rbx_interleaved_float(count)
            b = chunk.rbx_interleaved_float(count)
            for i in range(count):
                values[i] = [r[i], g[i], b[i]]

        elif type_name == "Vector2":
            vx = chunk.rbx_interleaved_float(count)
            vy = chunk.rbx_interleaved_float(count)
            for i in range(count):
                values[i] = [vx[i], vy[i]]

        elif type_name == "Vector3":
            vx = chunk.rbx_interleaved_float(count)
            vy = chunk.rbx_interleaved_float(count)
            vz = chunk.rbx_interleaved_float(count)
            for i in range(count):
                values[i] = [vx[i], vy[i], vz[i]]

        elif type_name == "Vector2int16":
            vx = chunk.rbx_interleaved_uint16(count)
            vy = chunk.rbx_interleaved_uint16(count)
            for i in range(count):
                values[i] = [_int16be(vx[i]), _int16be(vy[i])]

        elif type_name == "Vector3int16":
            vx = chunk.rbx_interleaved_uint16(count)
            vy = chunk.rbx_interleaved_uint16(count)
            vz = chunk.rbx_interleaved_uint16(count)
            for i in range(count):
                values[i] = [_int16be(vx[i]), _int16be(vy[i]), _int16be(vz[i])]

        elif type_name == "CFrame":
            # Pass 1: rotation
            for vi in range(count):
                value = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
                cf_type = chunk.uint8()
                if cf_type != 0:
                    right = CFRAME_FACES[(cf_type - 1) // 6]
                    up = CFRAME_FACES[(cf_type - 1) % 6]
                    back = [
                        right[1] * up[2] - up[1] * right[2],
                        right[2] * up[0] - up[2] * right[0],
                        right[0] * up[1] - up[0] * right[1],
                    ]
                    for k in range(3):
                        value[3 + k * 3] = right[k]
                        value[4 + k * 3] = up[k]
                        value[5 + k * 3] = back[k]
                else:
                    for k in range(3, 12):
                        value[k] = chunk.floatle()
                values[vi] = value

            # Pass 2: position (interleaved)
            vx = chunk.rbx_interleaved_float(count)
            vy = chunk.rbx_interleaved_float(count)
            vz = chunk.rbx_interleaved_float(count)
            for i in range(count):
                values[i][0] = vx[i]
                values[i][1] = vy[i]
                values[i][2] = vz[i]

        elif type_name == "Enum":
            values = chunk.rbx_interleaved_uint32(count)

        elif type_name == "Instance":
            ref_ids = chunk.rbx_interleaved_int32(count)
            ref_id = 0
            for i in range(count):
                ref_id += ref_ids[i]
                values[i] = state['instances'][ref_id] if 0 <= ref_id < len(state['instances']) else None

        elif type_name == "NumberSequence":
            for i in range(count):
                length = chunk.uint32le()
                sequence = []
                for _ in range(length):
                    sequence.append({
                        'Time': chunk.floatle(),
                        'Value': chunk.floatle(),
                        'Envelope': chunk.floatle(),
                    })
                values[i] = sequence

        elif type_name == "ColorSequence":
            for i in range(count):
                length = chunk.uint32le()
                sequence = []
                for _ in range(length):
                    sequence.append({
                        'Time': chunk.floatle(),
                        'Value': [chunk.floatle(), chunk.floatle(), chunk.floatle()],
                    })
                    chunk.floatle()  # unused envelope
                values[i] = sequence

        elif type_name == "NumberRange":
            for i in range(count):
                values[i] = [chunk.floatle(), chunk.floatle()]

        elif type_name == "Rect2D":
            x0 = chunk.rbx_interleaved_float(count)
            y0 = chunk.rbx_interleaved_float(count)
            x1 = chunk.rbx_interleaved_float(count)
            y1 = chunk.rbx_interleaved_float(count)
            for i in range(count):
                values[i] = [[x0[i], y0[i]], [x1[i], y1[i]]]

        elif type_name == "PhysicalProperties":
            for i in range(count):
                byte = chunk.uint8()
                if byte == 0 or byte == 2:
                    values[i] = False
                elif byte == 1 or byte == 3:
                    values[i] = {
                        'Density': chunk.floatle(),
                        'Friction': chunk.floatle(),
                        'Elasticity': chunk.floatle(),
                        'FrictionWeight': chunk.floatle(),
                        'ElasticityWeight': chunk.floatle(),
                    }
                    if byte & 2:
                        values[i]['AcousticAbsorption'] = chunk.floatle()
                    else:
                        values[i]['AcousticAbsorption'] = 1.0
                else:
                    dprint(f"[RBXBinaryParser] Unknown PhysicalProperties format {byte}")
                    values[i] = False

        elif type_name == "Color3uint8":
            rgbs = chunk.array(count * 3)
            for i in range(count):
                values[i] = [rgbs[i] / 255.0, rgbs[i + count] / 255.0, rgbs[i + count * 2] / 255.0]
            value_type = "Color3"

        elif type_name == "Font":
            for i in range(count):
                values[i] = {
                    'Family': chunk.string(chunk.uint32le()),
                    'Weight': chunk.uint16le(),
                    'Style': chunk.uint8(),
                    'CachedFaceId': chunk.string(chunk.uint32le()),
                }

        elif type_name == "int64":
            values = chunk.rbx_interleaved_int64(count)

        elif type_name == "SecurityCapabilities":
            raw = chunk.rbx_interleaved_int64(count)
            for i in range(count):
                values[i] = raw[i]  # keep as integer

        elif type_name == "SharedString":
            indices = chunk.rbx_interleaved_uint32(count)
            for i in range(count):
                idx = indices[i]
                if idx < len(state['shared_strings']):
                    values[i] = state['shared_strings'][idx]['value']
                else:
                    values[i] = ""
            value_type = "string"

        elif type_name == "Optional":
            values, value_type = RBXBinaryParser._parse_property_values(state, chunk, count)
            mask, _ = RBXBinaryParser._parse_property_values(state, chunk, count)
            for i in range(count):
                if not mask[i]:
                    values[i] = None

        elif type_name == "UniqueId":
            raw = chunk.array(count * 16)
            for i in range(count):
                result_hex = ""
                for j in range(16):
                    b = raw[j * count + i]
                    result_hex += f"{b:02x}"
                values[i] = result_hex

        elif type_name == "Content":
            source_types = chunk.rbx_interleaved_int32(count)
            num_uris = chunk.uint32le()
            uris = []
            for _ in range(num_uris):
                uris.append(chunk.string(chunk.uint32le()))

            num_objects = chunk.uint32le()
            objects = chunk.rbx_interleaved_int32(num_objects)

            num_objects_external = chunk.uint32le()
            objects_external = chunk.rbx_interleaved_int32(num_objects_external)

            uri_counter = 0
            object_counter = 0
            for i in range(count):
                source_type = source_types[i]
                if source_type == 1:
                    values[i] = {'SourceType': source_type, 'Uri': uris[uri_counter] if uri_counter < len(uris) else ""}
                    uri_counter += 1
                elif source_type == 2:
                    if object_counter < len(objects):
                        object_counter += objects[object_counter]
                    values[i] = {'SourceType': source_type, 'Object': object_counter}
                    object_counter += 1
                else:
                    values[i] = {'SourceType': source_type}

        else:
            dprint(f"[RBXBinaryParser] Unimplemented dataType {type_index} '{type_name}'")
            for i in range(count):
                values[i] = f"<{type_name}>"

        return values, value_type

    @staticmethod
    def _parse_PRNT(state, chunk):
        chunk.uint8()  # version
        count = chunk.uint32le()

        child_ids = chunk.rbx_interleaved_int32(count)
        parent_ids = chunk.rbx_interleaved_int32(count)

        child_id = 0
        parent_id = 0
        for i in range(count):
            child_id += child_ids[i]
            parent_id += parent_ids[i]

            child = state['instances'][child_id]
            if parent_id >= 0 and parent_id < len(state['instances']) and state['instances'][parent_id] is not None:
                parent = state['instances'][parent_id]
                child.set_property("Parent", parent, "Instance")
                parent.Children.append(child)
            else:
                state['result'].append(child)


# ─────────────────────────────────────────────
# RBXXmlParser
# ─────────────────────────────────────────────
class RBXXmlParser:
    """Parses XML-format RBXM/RBXL files."""

    @staticmethod
    def parse(buffer):
        if isinstance(buffer, bytes):
            text = buffer.decode('utf-8', errors='replace')
        else:
            text = buffer

        root = ET.fromstring(text)

        state = {
            'shared_strings': {},
            'ref_wait': [],
            'refs': {},
            'result': [],
            'meta': {},
        }

        for child in root:
            tag = child.tag
            if tag == "Item":
                state['result'].append(RBXXmlParser._parse_item(state, child))
            elif tag == "SharedStrings":
                RBXXmlParser._parse_shared_strings(state, child)
            elif tag == "Meta":
                name = child.attrib.get("name", "")
                state['meta'][name] = child.text or ""
            elif tag == "External":
                pass  # ignored
            else:
                dprint(f"[RBXXmlParser] Unknown node '{tag}'")

        return state

    @staticmethod
    def _parse_shared_strings(state, node):
        for child in node:
            if child.tag != "SharedString":
                continue
            md5 = child.attrib.get("md5", "")
            try:
                value = base64.b64decode((child.text or "").strip()).decode('utf-8', errors='replace')
            except Exception as e:
                dprint(f"[RBXXmlParser] Error decoding SharedString: {e}")
                value = ""
            state['shared_strings'][md5] = {'md5': md5, 'value': value}

    @staticmethod
    def _parse_item(state, node):
        class_name = node.attrib.get("class", "Unknown")
        inst = RBXInstance(class_name)
        referent = node.attrib.get("referent")

        if referent:
            state['refs'][referent] = inst
            # Resolve waiting references
            resolved = []
            for wait in state['ref_wait']:
                if wait['ref'] == referent:
                    wait['inst'].set_property(wait['name'], inst, "Instance")
                    resolved.append(wait)
            for r in resolved:
                state['ref_wait'].remove(r)

        for child_node in node:
            if child_node.tag == "Item":
                child = RBXXmlParser._parse_item(state, child_node)
                child.set_property("Parent", inst, "Instance")
                inst.Children.append(child)
            elif child_node.tag == "Properties":
                RBXXmlParser._parse_properties(state, inst, child_node)

        return inst

    @staticmethod
    def _get_child_value(node, child_tag, default=""):
        """Get text content of a child element by tag name."""
        child = node.find(child_tag)
        if child is not None and child.text is not None:
            return child.text
        return default

    @staticmethod
    def _parse_properties(state, inst, props_node):
        for prop_node in props_node:
            tag = prop_node.tag
            name = prop_node.attrib.get("name", "")
            value = prop_node.text or ""

            if tag in ("string", "ProtectedString", "BinaryString"):
                inst.set_property(name, value, "string")

            elif tag == "Content":
                url_el = prop_node.find("url")
                if url_el is None:
                    url_el = prop_node.find("uri")
                content_val = (url_el.text if url_el is not None and url_el.text else "")
                inst.set_property(name, content_val, "string")

            elif tag == "double":
                inst.set_property(name, float(value) if value else 0.0, "double")

            elif tag == "float":
                inst.set_property(name, float(value) if value else 0.0, "float")

            elif tag == "int":
                inst.set_property(name, int(value) if value else 0, "int")

            elif tag == "int64":
                inst.set_property(name, int(value) if value else 0, "int64")

            elif tag == "bool":
                inst.set_property(name, value == "true", "bool")

            elif tag == "token":
                inst.set_property(name, int(value) if value else 0, "Enum")

            elif tag == "Color3":
                r = float(RBXXmlParser._get_child_value(prop_node, "R", "0"))
                g = float(RBXXmlParser._get_child_value(prop_node, "G", "0"))
                b = float(RBXXmlParser._get_child_value(prop_node, "B", "0"))
                inst.set_property(name, [r, g, b], "Color3")

            elif tag == "Color3uint8":
                v = int(value) if value else 0
                inst.set_property(name, [
                    ((v >> 16) & 0xFF) / 255.0,
                    ((v >> 8) & 0xFF) / 255.0,
                    (v & 0xFF) / 255.0,
                ], "Color3")

            elif tag in ("CoordinateFrame", "OptionalCoordinateFrame"):
                target = prop_node
                if tag == "OptionalCoordinateFrame":
                    cf_el = prop_node.find("CFrame")
                    if cf_el is None:
                        continue
                    target = cf_el
                gv = lambda t, d="0": float(RBXXmlParser._get_child_value(target, t, d))
                inst.set_property(name, [
                    gv("X"), gv("Y"), gv("Z"),
                    gv("R00"), gv("R01"), gv("R02"),
                    gv("R10"), gv("R11"), gv("R12"),
                    gv("R20"), gv("R21"), gv("R22"),
                ], "CFrame")

            elif tag == "Vector2":
                x = float(RBXXmlParser._get_child_value(prop_node, "X", "0"))
                y = float(RBXXmlParser._get_child_value(prop_node, "Y", "0"))
                inst.set_property(name, [x, y], "Vector2")

            elif tag == "Vector2int16":
                x = float(RBXXmlParser._get_child_value(prop_node, "X", "0"))
                y = float(RBXXmlParser._get_child_value(prop_node, "Y", "0"))
                inst.set_property(name, [x, y], "Vector2int16")

            elif tag == "Vector3":
                x = float(RBXXmlParser._get_child_value(prop_node, "X", "0"))
                y = float(RBXXmlParser._get_child_value(prop_node, "Y", "0"))
                z = float(RBXXmlParser._get_child_value(prop_node, "Z", "0"))
                inst.set_property(name, [x, y, z], "Vector3")

            elif tag == "Vector3int16":
                x = float(RBXXmlParser._get_child_value(prop_node, "X", "0"))
                y = float(RBXXmlParser._get_child_value(prop_node, "Y", "0"))
                z = float(RBXXmlParser._get_child_value(prop_node, "Z", "0"))
                inst.set_property(name, [x, y, z], "Vector3int16")

            elif tag == "UDim":
                s = float(RBXXmlParser._get_child_value(prop_node, "S", "0"))
                o = float(RBXXmlParser._get_child_value(prop_node, "O", "0"))
                inst.set_property(name, [s, o], "UDim")

            elif tag == "UDim2":
                xs = float(RBXXmlParser._get_child_value(prop_node, "XS", "0"))
                xo = float(RBXXmlParser._get_child_value(prop_node, "XO", "0"))
                ys = float(RBXXmlParser._get_child_value(prop_node, "YS", "0"))
                yo = float(RBXXmlParser._get_child_value(prop_node, "YO", "0"))
                inst.set_property(name, [[xs, xo], [ys, yo]], "UDim2")

            elif tag == "Rect2D":
                min_el = prop_node.find("min")
                max_el = prop_node.find("max")
                def _rect_val(parent, child_tag, default="0"):
                    if parent is not None:
                        el = parent.find(child_tag)
                        if el is not None and el.text:
                            return float(el.text)
                    return float(default)
                inst.set_property(name, [
                    [_rect_val(min_el, "X"), _rect_val(min_el, "Y")],
                    [_rect_val(max_el, "X"), _rect_val(max_el, "Y")],
                ], "Rect2D")

            elif tag == "PhysicalProperties":
                custom = RBXXmlParser._get_child_value(prop_node, "CustomPhysics", "false")
                if custom == "true":
                    inst.set_property(name, {
                        'Density': float(RBXXmlParser._get_child_value(prop_node, "Density", "1")),
                        'Friction': float(RBXXmlParser._get_child_value(prop_node, "Friction", "0")),
                        'Elasticity': float(RBXXmlParser._get_child_value(prop_node, "Elasticity", "0")),
                        'FrictionWeight': float(RBXXmlParser._get_child_value(prop_node, "FrictionWeight", "1")),
                        'ElasticityWeight': float(RBXXmlParser._get_child_value(prop_node, "ElasticityWeight", "1")),
                    }, "PhysicalProperties")
                else:
                    inst.set_property(name, False, "PhysicalProperties")

            elif tag == "Font":
                inst.set_property(name, {
                    'Family': RBXXmlParser._get_child_value(prop_node, "Family", ""),
                    'Weight': int(RBXXmlParser._get_child_value(prop_node, "Weight", "500")),
                    'Style': int(RBXXmlParser._get_child_value(prop_node, "Style", "0")),
                    'CachedFaceId': RBXXmlParser._get_child_value(prop_node, "CachedFaceId", ""),
                }, "Font")

            elif tag == "Ref":
                if value in state['refs']:
                    inst.set_property(name, state['refs'][value], "Instance")
                else:
                    state['ref_wait'].append({'inst': inst, 'name': name, 'ref': value})

            elif tag == "SharedString":
                if value in state['shared_strings']:
                    inst.set_property(name, state['shared_strings'][value]['value'], "string")

            elif tag == "SecurityCapabilities":
                inst.set_property(name, int(value) if value else 0, "SecurityCapabilities")

            elif tag == "UniqueId":
                inst.set_property(name, value, "UniqueId")

            else:
                dprint(f"[RBXXmlParser] Unknown dataType '{tag}' for {inst.get_property('ClassName')}.{name}")


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────
def _int16be(x):
    """Convert interleaved uint16 to signed int16 (big endian rotation)."""
    val = ((x << 8 | x >> 8) & 0x7FFF) - ((x << 8) & 0x8000)
    return val


# ─────────────────────────────────────────────
# RBXModelParser - auto-detects binary vs XML
# ─────────────────────────────────────────────
class RBXModelParser:
    """
    Main entry point. Auto-detects binary (RBXM) vs XML format.
    
    Usage:
        with open("model.rbxm", "rb") as f:
            data = f.read()
        result = RBXModelParser.parse(data)
        
    Returns a dict with:
        result['result']  - list of top-level RBXInstance objects
        result['meta']    - dict of metadata
    """

    @staticmethod
    def parse(buffer):
        if isinstance(buffer, str):
            buffer = buffer.encode('utf-8')

        # Check header: "<roblox" followed by 0x21 (binary) or other (XML)
        if len(buffer) < 8:
            raise ValueError("Buffer too small to be a valid RBXM file")

        header = buffer[:7]
        if header != b"<roblox":
            raise ValueError(f"Not a valid RBXM file (header: {header})")

        if buffer[7] == 0x21:
            # Binary format
            return RBXBinaryParser.parse(buffer)
        else:
            # XML format
            return RBXXmlParser.parse(buffer)



with open(r"D:\Mine\GDrive\Blender\Roblox\0. Addon\RBX_Toolbox\RBX_Import\tmp_rbxm\2936967301.rbxm", "rb") as f:
    data = f.read()
result = RBXModelParser.parse(data)
#print(result)
'''print(result['result'][0].get_property('ClassName'))
print(result['result'][0].get_property('Name'))
print(result['result'][0].get_property('Parent'))
print(result['result'][0].get_property('Properties'))
print(result['result'][0].get_property('Children'))
print(result['result'][0].get_property('ClassId'))'''
#print(result['meta'])


def print_tree(instances, indent=0):
    for inst in instances:
        cls = inst.get_property("ClassName")
        name = inst.get_property("Name") or ""
        prefix = "  " * indent
        print(f"{prefix}{cls}: {name}")
        # Print all properties (uncomment for full detail)
        for pname, prop in inst.Properties.items():
            if pname not in ("ClassName", "Name", "Parent"):
                if pname == "HSRData":
                    pass
                else:
                    print(f"{prefix}  .{pname} = {prop['value']}")
        print_tree(inst.Children, indent + 1)
    
print_tree(result['result'])