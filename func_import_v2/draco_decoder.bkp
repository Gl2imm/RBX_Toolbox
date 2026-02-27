import struct
from io import BytesIO

# Constants
METADATA_FLAG_MASK = 32768

# encoderType
POINT_CLOUD = 0
TRIANGULAR_MESH = 1

# encoderMethod
MESH_SEQUENTIAL_ENCODING = 0
MESH_EDGEBREAKER_ENCODING = 1

# connectivityMethod
SEQUENTIAL_COMPRESSED_INDICES = 0
SEQUENTIAL_UNCOMPRESSED_INDICES = 1

# encoderType (Attributes)
SEQUENTIAL_ATTRIBUTE_ENCODER_GENERIC = 0
SEQUENTIAL_ATTRIBUTE_ENCODER_INTEGER = 1
SEQUENTIAL_ATTRIBUTE_ENCODER_QUANTIZATION = 2
SEQUENTIAL_ATTRIBUTE_ENCODER_NORMALS = 3

# predictionMethod
PREDICTION_NONE = -2
PREDICTION_DIFFERENCE = 0
MESH_PREDICTION_PARALLELOGRAM = 1
MESH_PREDICTION_CONSTRAINED_MULTI_PARALLELOGRAM = 4
MESH_PREDICTION_TEX_COORDS_PORTABLE = 5
MESH_PREDICTION_GEOMETRIC_NORMAL = 6

# predictionTransformType
PREDICTION_TRANSFORM_NONE = -1
PREDICTION_TRANSFORM_DELTA = 0
PREDICTION_TRANSFORM_WRAP = 1
PREDICTION_TRANSFORM_NORMAL_OCTAHEDRON_CANONICALIZED = 3

# Data Types
DT_INT8 = 1
DT_UINT8 = 2
DT_INT16 = 3
DT_UINT16 = 4
DT_INT32 = 5
DT_UINT32 = 6
DT_INT64 = 7
DT_UINT64 = 8
DT_FLOAT32 = 9
DT_FLOAT64 = 10
DT_BOOL = 11

DRACO_DATA_TYPE_SIZES = {
    0: 0,
    1: 1, 2: 1, 3: 2, 4: 2,
    5: 4, 6: 4, 7: 8, 8: 8,
    9: 4, 10: 8, 11: 1
}

DRACO_ATTR_TYPES = [
    "POSITION", "NORMAL", "COLOR", "TEX_COORD", "GENERIC"
]

class DracoByteReader:
    def __init__(self, data):
        self.buffer = BytesIO(data) if isinstance(data, bytes) else data
        self.view = self.buffer.getbuffer()

    def get_index(self):
        return self.buffer.tell()
    
    def set_index(self, idx):
        self.buffer.seek(idx)

    def jump(self, n):
        self.buffer.seek(self.buffer.tell() + n)

    def uint8(self):
        return struct.unpack("<B", self.buffer.read(1))[0]
    
    def int8(self):
        return struct.unpack("<b", self.buffer.read(1))[0]

    def uint16le(self):
        return struct.unpack("<H", self.buffer.read(2))[0]
    
    def uint32le(self):
        return struct.unpack("<I", self.buffer.read(4))[0]
    
    def int32le(self):
        return struct.unpack("<i", self.buffer.read(4))[0]

    def uint64le(self):
        return struct.unpack("<Q", self.buffer.read(8))[0]

    def floatle(self):
        return struct.unpack("<f", self.buffer.read(4))[0]
    
    def doublele(self):
        return struct.unpack("<d", self.buffer.read(8))[0]

    def string(self, length):
        return self.buffer.read(length).decode('utf-8')

class RansDecoder:
    def __init__(self):
        self.probability_table = []
        self.lookup_table = []
        self.buffer = None
        self.start_index = 0
        self.offset = 0
        self.base = 0
        self.precision = 0
        self.state = 0
        self.prob_zero = 0

    def decode_tables(self, stream, expected_cum_prob):
        num_symbols = DracoBitstream.leb128(stream)
        
        self.probability_table = [None] * num_symbols # Expand as needed? No, sparse/dynamic in JS.
        # Actually in JS it sets index i + j. Let's use a dict or large list? 
        # Since it's iterating, a list is fine but we need to handle gaps if any?
        # JS: probabilityTable[i+j] = ...
        # It seems indexes are contiguous roughly.
        
        # Let's use a dictionary map for sparse probability table to be safe
        self.probability_table = {}
        self.lookup_table = [] # This needs to be packed? JS: lookupTable[j] = i (symbol)
        
        cum_prob = 0
        act_prob = 0
        
        i = 0
        while i < num_symbols:
            data = stream.uint8()
            token = data & 3
            
            if token == 3:
                offset = data >> 2
                for j in range(offset + 1):
                    self.probability_table[i + j] = {'prob': 0, 'cum_prob': cum_prob}
                i += offset + 1
            else:
                prob = data >> 2
                for j in range(token):
                    eb = stream.uint8()
                    prob |= (eb << (8 * (j + 1) - 2))
                
                self.probability_table[i] = {'prob': prob, 'cum_prob': cum_prob}
                cum_prob += prob
                
                for j in range(act_prob, cum_prob):
                    # Python list handling for sparse/dynamic
                    # lookup_table size must grow
                    while len(self.lookup_table) <= j:
                         self.lookup_table.append(0)
                    self.lookup_table[j] = i
                    
                act_prob = cum_prob
                i += 1
                
        if cum_prob != expected_cum_prob:
            raise ValueError(f"Rans decoding error: cum_prob {cum_prob} != expected {expected_cum_prob}")

    def start(self, buffer_view, start_index, offset, base, precision):
        self.buffer = buffer_view
        self.start_index = start_index
        
        self.base = base
        self.precision = precision
        
        # In JS: this.buffer[this.startIndex + offset - 1]
        # We need to access bytes. buffer_view should be bytes or memoryview
        
        x = (self.buffer[self.start_index + offset - 1]) >> 6
        
        if x == 0:
            self.offset = offset - 1
            self.state = self.buffer[self.start_index + offset - 1] & 0x3F
        elif x == 1:
            self.offset = offset - 2
            self.state = (
                (self.buffer[self.start_index + offset - 1] << 8) |
                self.buffer[self.start_index + offset - 2]
            ) & 0x3FFF
        elif x == 2:
            self.offset = offset - 3
            self.state = (
                (self.buffer[self.start_index + offset - 1] << 16) |
                (self.buffer[self.start_index + offset - 2] << 8) |
                self.buffer[self.start_index + offset - 3]
            ) & 0x3FFFFF
        elif x == 3:
            self.offset = offset - 4
            self.state = (
                (self.buffer[self.start_index + offset - 1] << 24) |
                (self.buffer[self.start_index + offset - 2] << 16) |
                (self.buffer[self.start_index + offset - 3] << 8) |
                self.buffer[self.start_index + offset - 4]
            ) & 0x3FFFFFFF
            
        self.state += base

    def read_symbol(self):
        while self.state < self.base and self.offset > 0:
            self.offset -= 1
            self.state = (self.state << 8) | self.buffer[self.start_index + self.offset]
            
        quo = self.state // self.precision
        rem = self.state % self.precision
        
        symbol = self.lookup_table[rem]
        entry = self.probability_table[symbol]
        prob = entry['prob']
        cum_prob = entry['cum_prob']
        
        self.state = quo * prob + rem - cum_prob
        return symbol

    def init_symbols(self, stream, bit_length):
        precision_bits = (3 * bit_length) // 2
        if precision_bits > 20: precision_bits = 20
        if precision_bits < 12: precision_bits = 12
        
        precision = 1 << precision_bits
        base = precision * 4
        
        self.decode_tables(stream, precision)
        
        data_size = DracoBitstream.leb128(stream)
        
        # buffer for start is generally the full buffer of the stream?
        # In JS: stream.buffer is likely the full ArrayBuffer or TypedArray
        # We need to pass the underlying buffer accessible by index
        self.start(stream.view, stream.get_index(), data_size, base, precision)
        stream.jump(data_size)

    def init_bits(self, stream):
        self.prob_zero = stream.uint8()
        data_size = DracoBitstream.leb128(stream)
        self.start(stream.view, stream.get_index(), data_size, 4096, 256)
        stream.jump(data_size)

    def read_bit(self):
        while self.state < self.base and self.offset > 0:
            self.offset -= 1
            self.state = (self.state << 8) | self.buffer[self.start_index + self.offset]
            
        quot = self.state // self.precision
        rem = self.state % self.precision
        
        p = self.precision - self.prob_zero
        val = rem < p
        
        if val:
            self.state = quot * p + rem
        else:
            self.state = self.state - quot * p - p
            
        return 1 if val else 0


class DracoBitstream:
    @staticmethod
    def leb128(stream):
        result = 0
        shift = 0
        while True:
            value = stream.uint8()
            result |= (value & 0x7F) << shift
            shift += 7
            if not (value & 0x80):
                break
        return result

    @staticmethod
    def parse(data_bytes):
        stream = DracoByteReader(data_bytes)
        parser = DracoParser()
        
        # DecodeHeader
        header = DracoBitstream.parse_header(stream)
        parser.header = header
        
        print(f"DRACO {header['majorVersion']}.{header['minorVersion']} | encoderType: {header['encoderType']}, method: {header['encoderMethod']}, flags: {header['flags']}")
        
        if header['encoderType'] != TRIANGULAR_MESH:
            raise NotImplementedError("draco encoderType not implemented")
            
        if header['flags'] & METADATA_FLAG_MASK:
             raise NotImplementedError("draco flags not implemented")
             
        # DecodeConnectivityData
        DracoBitstream.decode_connectivity_data(stream, parser, header['encoderMethod'])
        
        # DecodeAttributeData
        DracoBitstream.decode_attribute_data(stream, parser, header['encoderMethod'])
        
        # GenerateSequence
        DracoBitstream.generate_sequence(parser, header['encoderMethod'])
        
        # DecodeAttributes
        DracoBitstream.decode_attributes(stream, parser)
        
        # Return attributes from last decoder (usually position/norm/etc are sequential)
        # JS: parser.attributes = parser.decoders.at(-1).attributes
        # In Python list[-1]
        parser.attributes = parser.decoders[-1]['attributes']
        
        # Convert to dictionary output format expected by mesh_reader
        result = {}
        
        for attr in parser.attributes:
            # uniqueId: 0=Pos, 1=Norm, 2=UV, 3=?, 4=Color involved? 
            # We map based on standard Roblox uniqueId
            # But wait, generic attributes might rely on order too.
            # uniqueId in JS code comes from stream.
            
            uid = attr['uniqueId']
            output_data = attr.get('output', [])
            
            if uid == 0:
                result["vertices"] = output_data
            elif uid == 1:
                result["normals"] = output_data
            elif uid == 2:
                result["uvs"] = output_data
            elif uid == 3:
                 pass # Tangents? Not standard usage in my previous MeshParser check but maybe?
            elif uid == 4:
                result["vertexColors"] = output_data
            
        # Faces
        result["faces"] = parser.faces
        
        return result

    @staticmethod
    def parse_header(stream):
        header_str = stream.string(5)
        if header_str != "DRACO":
            raise ValueError("invalid draco bitstream")
            
        major = stream.uint8()
        minor = stream.uint8()
        enc_type = stream.uint8()
        enc_method = stream.uint8()
        flags = stream.uint16le()
        
        return {
            'majorVersion': major,
            'minorVersion': minor,
            'encoderType': enc_type,
            'encoderMethod': enc_method,
            'flags': flags
        }
    
    @staticmethod
    def decode_connectivity_data(stream, parser, encoder_method):
        if encoder_method == MESH_SEQUENTIAL_ENCODING:
            parser.num_faces = DracoBitstream.leb128(stream)
            parser.num_points = DracoBitstream.leb128(stream)
            connectivity_method = stream.uint8()
            parser.connectivity_method = connectivity_method
            
            parser.faces = [0] * (parser.num_faces * 3)
            
            if connectivity_method == SEQUENTIAL_COMPRESSED_INDICES:
                 raise NotImplementedError("draco compressed indices not implemented")
            elif connectivity_method == SEQUENTIAL_UNCOMPRESSED_INDICES:
                if parser.num_points < 256:
                    for i in range(parser.num_faces):
                        parser.faces[i*3+0] = stream.uint8()
                        parser.faces[i*3+1] = stream.uint8()
                        parser.faces[i*3+2] = stream.uint8()
                elif parser.num_points < (1 << 16):
                    for i in range(parser.num_faces):
                        parser.faces[i*3+0] = stream.uint16le()
                        parser.faces[i*3+1] = stream.uint16le()
                        parser.faces[i*3+2] = stream.uint16le()
                elif parser.num_points < (1 << 21):
                    for i in range(parser.num_faces):
                        parser.faces[i*3+0] = DracoBitstream.leb128(stream)
                        parser.faces[i*3+1] = DracoBitstream.leb128(stream)
                        parser.faces[i*3+2] = DracoBitstream.leb128(stream)
                else:
                    for i in range(parser.num_faces):
                        parser.faces[i*3+0] = stream.uint32le()
                        parser.faces[i*3+1] = stream.uint32le()
                        parser.faces[i*3+2] = stream.uint32le()
        else:
             raise NotImplementedError("draco encoderMethod not implemented")

    @staticmethod
    def decode_attribute_data(stream, parser, encoder_method):
        num_decoders = stream.uint8()
        parser.decoders = []
        for i in range(num_decoders):
            parser.decoders.append({
                'attributes': None,
                'pointIds': None,
                'index': i,
                'decoderType': None,
                'dataId': None,
                'traversalMethod': None
            })
            
        if encoder_method == MESH_EDGEBREAKER_ENCODING:
             for decoder in parser.decoders:
                 decoder['dataId'] = stream.uint8()
                 decoder['decoderType'] = stream.uint8()
                 decoder['traversalMethod'] = stream.uint8()
                 
        for decoder in parser.decoders:
            num_attributes = DracoBitstream.leb128(stream)
            decoder['attributes'] = []
            
            for j in range(num_attributes):
                att_type = stream.uint8()
                data_type = stream.uint8()
                num_comps = stream.uint8()
                normalized = stream.uint8()
                unique_id = DracoBitstream.leb128(stream)
                
                decoder['attributes'].append({
                    'attributeType': att_type,
                    'dataType': data_type,
                    'numComponents': num_comps,
                    'normalized': normalized,
                    'uniqueId': unique_id,
                    'decoderType': None
                })
                
            for attr in decoder['attributes']:
                attr['decoderType'] = stream.uint8()

    @staticmethod
    def generate_sequence(parser, encoder_method):
        if encoder_method == MESH_SEQUENTIAL_ENCODING:
            for decoder in parser.decoders:
                decoder['pointIds'] = list(range(parser.num_points))
        else:
            raise NotImplementedError("draco edgebreaker not implemented")

    @staticmethod
    def decode_attributes(stream, parser):
        parser.rans = RansDecoder()
        parser.bits_value = 0
        parser.bits_length = 0
        
        for decoder in parser.decoders:
            for attr in decoder['attributes']:
                decoder_type = attr['decoderType']
                if decoder_type == SEQUENTIAL_ATTRIBUTE_ENCODER_GENERIC:
                    DracoBitstream.decode_attribute_generic(stream, parser, decoder, attr)
                else:
                    DracoBitstream.decode_attribute_compressed(stream, parser, decoder, attr, decoder_type)
            
            # Prediction/Transform passes
            for attr in decoder['attributes']:
                decoder_type = attr['decoderType']
                if decoder_type == SEQUENTIAL_ATTRIBUTE_ENCODER_QUANTIZATION:
                    DracoBitstream.decode_and_transform_quantized(stream, parser, decoder, attr)
                elif decoder_type == SEQUENTIAL_ATTRIBUTE_ENCODER_NORMALS:
                     DracoBitstream.decode_and_transform_normals(stream, parser, decoder, attr)
                else:
                     DracoBitstream.transform_attribute_generic(parser, decoder, attr)

    @staticmethod
    def decode_attribute_generic(stream, parser, decoder, attr):
         point_ids = decoder['pointIds']
         num_entries = len(point_ids)
         num_comps = attr['numComponents']
         num_values = num_entries * num_comps
         
         output = [0] * num_values
         dt_size = DRACO_DATA_TYPE_SIZES.get(attr['dataType'], 0)
         
         if dt_size == 1:
             for k in range(num_values): output[k] = stream.uint8()
         elif dt_size == 2:
             for k in range(num_values): output[k] = stream.uint16le()
         elif dt_size == 4:
             for k in range(num_values): output[k] = stream.uint32le()
         elif dt_size == 8:
             for k in range(num_values): output[k] = stream.uint64le()
             
         attr['output'] = output

    @staticmethod
    def decode_attribute_compressed(stream, parser, decoder, attr, decoder_type):
        prediction_scheme = stream.uint8()
        attr['predictionScheme'] = prediction_scheme
        
        if prediction_scheme != PREDICTION_NONE:
            attr['predictionTransformType'] = stream.int8()
            
        compressed = stream.uint8()
        
        num_entries = len(decoder['pointIds'])
        num_comps = attr['numComponents']
        
        if decoder_type == SEQUENTIAL_ATTRIBUTE_ENCODER_NORMALS and prediction_scheme == PREDICTION_DIFFERENCE:
            num_comps = 2 # Normals specialized compression
            
        num_values = num_entries * num_comps
        output = [0] * num_values
        attr['output'] = output
        
        if compressed > 0:
            DracoBitstream.decode_symbols(stream, parser, num_values, num_comps, output)
        else:
            # Uncompressed fallback inside compressed block (?)
            size = stream.uint8()
            if size == 1:
                for k in range(num_values): output[k] = stream.uint8()
            elif size == 2:
                for k in range(num_values): output[k] = stream.uint16le()
            elif size == 4:
                for k in range(num_values): output[k] = stream.uint32le()
            elif size == 8:
                for k in range(num_values): output[k] = stream.uint64le()
                
        # Zigzag decode equivalent (signed conversion)
        # JS: value & 1 ? -(value >>> 1) - 1 : value >>> 1
        if num_values > 0 and attr.get('predictionTransformType') != PREDICTION_TRANSFORM_NORMAL_OCTAHEDRON_CANONICALIZED:
            for i in range(len(output)):
                val = output[i]
                # Simulate JS unsigned shift right for logic consistency if val was loaded as unsigned
                # But here 'val' is from decode_symbols which returns positive integers usually (symbols)
                if val & 1:
                    output[i] = -((val >> 1)) - 1
                else:
                    output[i] = val >> 1
                    
        if prediction_scheme != PREDICTION_NONE:
            DracoBitstream.decode_prediction_data(stream, parser, decoder, attr, num_values, num_comps, prediction_scheme, attr.get('predictionTransformType'))
            
            if num_values > 0:
                DracoBitstream.compute_original_values(parser, decoder, attr, num_values, num_comps, prediction_scheme, attr.get('predictionTransformType'), output)

    @staticmethod
    def decode_symbols(stream, parser, num_values, num_comps, output):
        TAGGED_SYMBOLS = 0
        RAW_SYMBOLS = 1
        
        scheme = stream.uint8()
        
        if scheme == TAGGED_SYMBOLS:
            parser.rans.init_symbols(stream, 5)
            for i in range(0, num_values, num_comps):
                num_bits = parser.rans.read_symbol()
                for j in range(num_comps):
                    output[i + j] = DracoBitstream.read_bits(stream, parser, num_bits)
            
            DracoBitstream.flush_bits(parser)
            
        elif scheme == RAW_SYMBOLS:
            max_bit_length = stream.uint8()
            parser.rans.init_symbols(stream, max_bit_length)
            for i in range(num_values):
                output[i] = parser.rans.read_symbol()

    @staticmethod
    def read_bits(stream, parser, n):
        while parser.bits_length < n:
            byte = stream.uint8()
            for i in range(8):
                parser.bits_value = (parser.bits_value << 1) | ((byte >> i) & 1)
            parser.bits_length += 8
            
        value = 0
        for bit in range(n):
            parser.bits_length -= 1
            value |= ((parser.bits_value >> parser.bits_length) & 1) << bit
        return value

    @staticmethod
    def flush_bits(parser):
        parser.bits_value = 0
        parser.bits_length = 0

    @staticmethod
    def decode_prediction_data(stream, parser, decoder, attr, num_values, num_comps, pred_scheme, pred_trans_type):
        if pred_scheme == PREDICTION_DIFFERENCE:
            pass # No extra data
        else:
            # We implemented only minimal subset based on JS file analysis
             pass

        if pred_trans_type == PREDICTION_TRANSFORM_WRAP:
            attr['wrapMin'] = stream.int32le()
            attr['wrapMax'] = stream.int32le()
        elif pred_trans_type == PREDICTION_TRANSFORM_NORMAL_OCTAHEDRON_CANONICALIZED:
            attr['octaMaxQ'] = stream.int32le()
            stream.int32le() # unused

    @staticmethod
    def compute_original_values(parser, decoder, attr, num_values, num_comps, pred_scheme, pred_trans_type, output):
        # We need a Python equivalent of the JS computeOriginalValues closure/function
        
        # Define helper functions inside
        def mod_max(x, center_value, max_quantized_value):
            if x > center_value: return x - max_quantized_value
            if x < -center_value: return x + max_quantized_value
            return x

        # Prediction Transform handling
        if pred_trans_type == PREDICTION_TRANSFORM_WRAP:
             wrap_min = attr['wrapMin']
             wrap_max = attr['wrapMax']
             max_dif = 1 + wrap_max - wrap_min
             
             # In-place Difference decoding with Wrap
             # D(i) = D(i) + D(i-1)
             
             # But first, we need to handle the specific WRAP logic + Diff logic combination?
             # The JS code defines `computeOriginalValue` function and THEN loops.
             
             def compute_val_wrap(predicted, pred_idx, corr, corr_idx, out_arr, out_idx):
                 for i in range(num_comps):
                     # predicted[pred_idx + i] is 'predicted' value, usually prev value
                     val = max(wrap_min, min(wrap_max, predicted[pred_idx + i])) + corr[corr_idx + i]
                     if val > wrap_max: val -= max_dif
                     elif val < wrap_min: val += max_dif
                     out_arr[out_idx + i] = val

             if pred_scheme == PREDICTION_DIFFERENCE:
                  # First val is original
                  # Then subsequent are diffs
                  zero = [0]*num_comps
                  # decode first
                  # Note: "output" array currently holds the "correction" (decoded symbols)
                  # We use it as both source (corr) and dest (output)
                  # So we must be careful.
                  
                  # JS: computeOriginalValue(zeroValues, 0,  output, 0,  output, 0)
                  compute_val_wrap(zero, 0, output, 0, output, 0)
                  
                  for i in range(num_comps, num_values, num_comps):
                      compute_val_wrap(output, i - num_comps, output, i, output, i)
                      
        elif pred_trans_type == PREDICTION_TRANSFORM_NORMAL_OCTAHEDRON_CANONICALIZED:
             # This is complex, used for Normals
             max_quantized = (1 << attr['octaMaxQ']) - 1
             center_value = (max_quantized - 1) // 2
             
             def invert_diamond(s, t):
                 sign_s = 1 if s >= 0 else -1
                 sign_t = 1 if t >= 0 else -1 # JS logic slightly more complex check?
                 # JS: if(s>=0 && t>=0) {1,1} else if (s<=0 && t<=0) {-1,-1} else {s>0?1:-1, t>0?1:-1}
                 if s >= 0 and t >= 0:
                     sign_s, sign_t = 1, 1
                 elif s <= 0 and t <= 0:
                     sign_s, sign_t = -1, -1
                 else:
                     sign_s = 1 if s > 0 else -1
                     sign_t = 1 if t > 0 else -1
                     
                 corner_s = sign_s * center_value
                 corner_t = sign_t * center_value
                 
                 us = t + t - corner_t
                 ut = s + s - corner_s
                 
                 if sign_s * sign_t >= 0:
                     us = -us
                     ut = -ut
                     
                 return (us + corner_s) // 2, (ut + corner_t) // 2 # Integer division? JS used /2.
             
             def get_rot_count(pred_x, pred_y):
                 if pred_x == 0:
                     if pred_y == 0: return 0
                     elif pred_y > 0: return 3
                     else: return 1
                 elif pred_x > 0:
                     return 2 if pred_y >= 0 else 1
                 else:
                     return 0 if pred_y <= 0 else 3
                     
             def rotate_point(p, count):
                 if count == 1: return [p[1], -p[0]]
                 if count == 2: return [-p[0], -p[1]]
                 if count == 3: return [-p[1], p[0]]
                 return p
                 
             def add_as_unsigned(a, b):
                 # JS does (a >>> 0) + (b >>> 0) essentially
                 ua = a + 4294967296 if a < 0 else a
                 ub = b + 4294967296 if b < 0 else b
                 return ua + ub
                 
             def compute_val_oct(predicted, pred_idx, corr, corr_idx, out_arr, out_idx):
                 pred = [predicted[pred_idx+0]-center_value, predicted[pred_idx+1]-center_value]
                 correction = [corr[corr_idx+0], corr[corr_idx+1]]
                 
                 is_in_diamond = (abs(pred[0]) + abs(pred[1])) <= center_value
                 if not is_in_diamond:
                     pred = invert_diamond(pred[0], pred[1])
                     
                 is_bl = (pred[0] == 0 and pred[1] == 0) or (pred[0] < 0 and pred[1] <= 0)
                 rot_cnt = get_rot_count(pred[0], pred[1])
                 
                 if not is_bl:
                     pred = rotate_point(pred, rot_cnt)
                     
                 # Modular addition
                 orig = [
                     mod_max(add_as_unsigned(pred[0], correction[0]), center_value, max_quantized),
                     mod_max(add_as_unsigned(pred[1], correction[1]), center_value, max_quantized)
                 ]
                 
                 if not is_bl:
                     orig = rotate_point(orig, (4 - rot_cnt) % 4)
                     
                 if not is_in_diamond:
                     orig = invert_diamond(orig[0], orig[1])
                     
                 out_arr[out_idx+0] = orig[0] + center_value
                 out_arr[out_idx+1] = orig[1] + center_value

             if pred_scheme == PREDICTION_DIFFERENCE:
                  zero = [0]*num_comps
                  compute_val_oct(zero, 0, output, 0, output, 0)
                  for i in range(num_comps, num_values, num_comps):
                      compute_val_oct(output, i - num_comps, output, i, output, i)
        
        else:
            # Default Difference
             if pred_scheme == PREDICTION_DIFFERENCE:
                 # Simple addition
                 # D(i) = D(i) + D(i-1)
                 # output already has D(i) (correction)
                 # D(0) is correct
                 for i in range(num_comps, num_values, num_comps):
                      for j in range(num_comps):
                          output[i+j] = output[i+j] + output[i-num_comps+j]


    @staticmethod
    def decode_and_transform_quantized(stream, parser, decoder, attr):
        num_comps = attr['numComponents']
        num_values = len(decoder['pointIds']) * num_comps
        output = attr['output']
        
        min_values = []
        for i in range(num_comps):
            min_values.append(stream.floatle())
            
        range_val = stream.floatle()
        quant_bits = stream.uint8()
        
        max_quantized = (1 << quant_bits) - 1
        delta = range_val / max_quantized if max_quantized > 0 else 0
        
        for i in range(0, num_values, num_comps):
            for j in range(num_comps):
                output[i+j] = min_values[j] + output[i+j] * delta

    @staticmethod
    def decode_and_transform_normals(stream, parser, decoder, attr):
         num_values = len(decoder['pointIds']) * 2
         inp = attr['output']
         output = [] # Replaces output with 3 component normals
         attr['output'] = output
         
         quant_bits = stream.uint8()
         max_val = (1 << quant_bits) - 2
         dequant = 2.0 / max_val
         
         for i in range(0, num_values, 2):
             s = inp[i]
             t = inp[i+1]
             
             y = s * dequant - 1
             z = t * dequant - 1
             x = 1.0 - abs(y) - abs(z)
             
             x_offset = -x if x < 0 else 0 # Clamped? JS logic: x_offset = -x; x_offset < 0 ? 0 : x_offset
             
             # JS: y += y < 0 ? x_offset : -x_offset
             y += x_offset if y < 0 else -x_offset
             z += x_offset if z < 0 else -x_offset
             
             norm_sq = x*x + y*y + z*z
             if norm_sq < 1e-6:
                 output.extend([0.0, 0.0, 0.0])
             else:
                 import math
                 d = 1.0 / math.sqrt(norm_sq)
                 output.extend([x*d, y*d, z*d])

    @staticmethod
    def transform_attribute_generic(parser, decoder, attr):
        # Convert raw int output to floats if needed
        # JS uses ByteReader.Converter.setUint32 ... getFloat32
        # We can just unpack/pack
        out = attr['output']
        dt = attr['dataType']
        
        if dt == DT_FLOAT32:
             # out contains uint32s, convert to float
             for i in range(len(out)):
                 out[i] = struct.unpack('f', struct.pack('I', out[i] & 0xFFFFFFFF))[0]
        elif dt == DT_FLOAT64:
             for i in range(len(out)):
                 out[i] = struct.unpack('d', struct.pack('Q', out[i] & 0xFFFFFFFFFFFFFFFF))[0]
        elif dt == DT_BOOL:
             for i in range(len(out)):
                 out[i] = (out[i] != 0)


class DracoParser:
    def __init__(self):
        self.header = None
        self.num_faces = 0
        self.num_points = 0
        self.connectivity_method = 0
        self.faces = []
        self.decoders = []
        self.attributes = []
        self.rans = None
        self.bits_value = 0
        self.bits_length = 0
