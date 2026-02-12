import struct
from io import BytesIO

def assert_condition(cond, msg):
    if not cond:
        raise ValueError(msg)

class ByteReader:
    def __init__(self, data: bytes):
        self.buffer = BytesIO(data)

    def get_index(self):
        return self.buffer.tell()

    def set_index(self, idx):
        self.buffer.seek(idx)

    def get_length(self):
        return len(self.buffer.getbuffer())

    def jump(self, n):
        self.buffer.seek(self.buffer.tell() + n)

    def byte(self):
        return struct.unpack("<B", self.buffer.read(1))[0]

    def uint16le(self):
        return struct.unpack("<H", self.buffer.read(2))[0]

    def uint32le(self):
        return struct.unpack("<I", self.buffer.read(4))[0]

    def floatle(self):
        return struct.unpack("<f", self.buffer.read(4))[0]

    def string(self, length):
        return self.buffer.read(length).decode("utf-8", errors="ignore")

    def subarray(self, start, end):
        return self.buffer.getbuffer()[start:end]

def buffer_to_string(buf):
    if isinstance(buf, memoryview):
        buf = buf.tobytes()  # convert memoryview → bytes
    return buf.decode("utf-8", errors="ignore")

class RBXMeshParser:
    @staticmethod
    def parse(buffer: bytes):
        reader = ByteReader(buffer)
        assert_condition(reader.string(8) == "version ", "Invalid mesh file")

        version = reader.string(4)
        if version in ("1.00", "1.01"):
            return RBXMeshParser.parse_text(buffer_to_string(buffer))
        elif version in ("2.00", "3.00", "3.01", "4.00", "4.01", "5.00"):
            return RBXMeshParser.parse_bin(buffer, version)
        else:
            raise ValueError(f"Unsupported mesh version '{version}'")

    @staticmethod
    def parse_text(s: str):
        lines = s.splitlines()
        assert_condition(len(lines) == 3, "Invalid mesh version 1 file (Wrong amount of lines)")

        version = lines[0]
        face_count = int(lines[1])
        data = lines[2]

        vectors = data.replace(" ", "").replace("\n", "").strip()[1:-1].split("][")
        assert_condition(len(vectors) == face_count * 9, "Length mismatch")

        scale_multiplier = 0.5 if version == "version 1.00" else 1.0
        vertex_count = face_count * 3

        vertices, normals, uvs, faces = [], [], [], []

        for i in range(vertex_count):
            n = i * 3
            vertex = list(map(float, vectors[n].split(",")))
            normal = list(map(float, vectors[n + 1].split(",")))
            uv = list(map(float, vectors[n + 2].split(",")))

            vertices.extend([vertex[0] * scale_multiplier,
                             vertex[1] * scale_multiplier,
                             vertex[2] * scale_multiplier])

            normals.extend(normal)
            uvs.extend(uv)
            faces.append(i)

        return {"version": version.split(" ")[1], "vertices": vertices, "normals": normals, "uvs": uvs, "faces": faces, "lods": [0, face_count]}

    @staticmethod
    def parse_bin(buffer: bytes, version: str):
        reader = ByteReader(buffer)
        assert_condition(reader.string(12) == f"version {version}", "Bad header")

        newline = reader.byte()
        if newline == 0x0D:
            assert_condition(reader.byte() == 0x0A, "Bad newline")
        else:
            assert_condition(newline == 0x0A, "Bad newline")

        begin = reader.get_index()

        # defaults
        header_size = 0
        vertex_size = 0
        face_size = 12
        lod_size = 4
        name_table_size = 0
        facs_data_size = 0
        lod_count = 0
        vertex_count = 0
        face_count = 0
        bone_count = 0
        subset_count = 0

        if version == "2.00":
            header_size = reader.uint16le()
            assert_condition(header_size >= 12, f"Invalid header size {header_size}")
            vertex_size = reader.byte()
            face_size = reader.byte()
            vertex_count = reader.uint32le()
            face_count = reader.uint32le()

        elif version.startswith("3."):
            header_size = reader.uint16le()
            assert_condition(header_size >= 16, f"Invalid header size {header_size}")
            vertex_size = reader.byte()
            face_size = reader.byte()
            lod_size = reader.uint16le()
            lod_count = reader.uint16le()
            vertex_count = reader.uint32le()
            face_count = reader.uint32le()

        elif version.startswith("4."):
            header_size = reader.uint16le()
            assert_condition(header_size >= 24, f"Invalid header size {header_size}")
            reader.jump(2)
            vertex_count = reader.uint32le()
            face_count = reader.uint32le()
            lod_count = reader.uint16le()
            bone_count = reader.uint16le()
            name_table_size = reader.uint32le()
            subset_count = reader.uint16le()
            reader.jump(2)
            vertex_size = 40

        elif version.startswith("5."):
            header_size = reader.uint16le()
            assert_condition(header_size >= 32, f"Invalid header size {header_size}")
            reader.jump(2)
            vertex_count = reader.uint32le()
            face_count = reader.uint32le()
            lod_count = reader.uint16le()
            bone_count = reader.uint16le()
            name_table_size = reader.uint32le()
            subset_count = reader.uint16le()
            reader.jump(2)
            reader.jump(4)
            facs_data_size = reader.uint32le()
            vertex_size = 40

        reader.set_index(begin + header_size)

        assert_condition(vertex_size >= 36, f"Invalid vertex size {vertex_size}")
        assert_condition(face_size >= 12, f"Invalid face size {face_size}")
        assert_condition(lod_size >= 4, f"Invalid lod size {lod_size}")

        file_end = (reader.get_index() +
            (vertex_count * vertex_size) +
            (bone_count * 8 * vertex_count if bone_count > 0 else 0) +
            (face_count * face_size) +
            (lod_count * lod_size) +
            (bone_count * 60) +
            name_table_size +
            (subset_count * 72) +
            facs_data_size)

        #assert_condition(file_end == reader.get_length(),
                         #f"Invalid file size (expected {reader.get_length()}, got {file_end})")

        faces = [0] * (face_count * 3)
        vertices = [0.0] * (vertex_count * 3)
        normals = [0.0] * (vertex_count * 3)
        uvs = [0.0] * (vertex_count * 2)
        tangents = [0.0] * (vertex_count * 4)
        vertex_colors = [0] * (vertex_count * 4) if vertex_size >= 40 else None
        lods = []

        mesh = {
            "version" : version,
            "vertexColors": vertex_colors,
            "vertices": vertices,
            "tangents": tangents,
            "normals": normals,
            "faces": faces,
            "lods": lods,
            "uvs": uvs  
        }

        # Vertex[vertexCount]
        for i in range(vertex_count):
            vertices[i*3+0] = reader.floatle()
            vertices[i*3+1] = reader.floatle()
            vertices[i*3+2] = reader.floatle()

            normals[i*3+0] = reader.floatle()
            normals[i*3+1] = reader.floatle()
            normals[i*3+2] = reader.floatle()

            uvs[i*2+0] = reader.floatle()
            uvs[i*2+1] = 1 - reader.floatle()

            tangents[i*4+0] = reader.byte() / 127 - 1
            tangents[i*4+1] = reader.byte() / 127 - 1
            tangents[i*4+2] = reader.byte() / 127 - 1
            tangents[i*4+3] = reader.byte() / 127 - 1

            if vertex_colors is not None:
                vertex_colors[i*4+0] = reader.byte()
                vertex_colors[i*4+1] = reader.byte()
                vertex_colors[i*4+2] = reader.byte()
                vertex_colors[i*4+3] = reader.byte()
                reader.jump(vertex_size - 40)
            else:
                reader.jump(vertex_size - 36)

        # Envelope
        if bone_count > 0:
            mesh["skinIndices"] = [0] * (vertex_count * 4)
            mesh["skinWeights"] = [0.0] * (vertex_count * 4)
            for i in range(vertex_count):
                for j in range(4):
                    mesh["skinIndices"][i*4+j] = reader.byte()
                for j in range(4):
                    mesh["skinWeights"][i*4+j] = reader.byte() / 255

        # Faces
        for i in range(face_count):
            faces[i*3+0] = reader.uint32le()
            faces[i*3+1] = reader.uint32le()
            faces[i*3+2] = reader.uint32le()
            reader.jump(face_size - 12)

        # LODs
        if lod_count <= 2:
            lods.extend([0, face_count])
            reader.jump(lod_count * lod_size)
        else:
            for i in range(lod_count):
                lods.append(reader.uint32le())
                reader.jump(lod_size - 4)

        # Bones
        if bone_count > 0:
            name_table_start = reader.get_index() + bone_count * 60
            mesh["bones"] = [None] * bone_count
            for i in range(bone_count):
                bone = {}
                name_start = name_table_start + reader.uint32le()
                name_end = buffer_to_string(reader.subarray(name_start, reader.get_length())).find("\x00")
                if name_end == -1:
                    bone["name"] = buffer_to_string(reader.subarray(name_start, reader.get_length()))
                else:
                    bone["name"] = buffer_to_string(reader.subarray(name_start, name_start + name_end))

                parent_index = reader.uint16le()
                lod_parent_index = reader.uint16le()
                bone["parent"] = mesh["bones"][parent_index] if parent_index < i else None
                bone["lodParent"] = mesh["bones"][lod_parent_index] if lod_parent_index < i else None

                bone["culling"] = reader.floatle()
                bone["cframe"] = [0.0]*12
                for j in range(9):
                    bone["cframe"][j+3] = reader.floatle()
                for j in range(3):
                    bone["cframe"][j] = reader.floatle()

                mesh["bones"][i] = bone

        if name_table_size > 0:
            reader.jump(name_table_size)

        if subset_count > 0:
            bone_indices = [0]*26
            for _ in range(subset_count):
                reader.uint32le()
                reader.uint32le()
                verts_begin = reader.uint32le()
                verts_length = reader.uint32le()
                reader.uint32le()
                for i in range(26):
                    bone_indices[i] = reader.uint16le()
                verts_end = verts_begin + verts_length
                for i in range(verts_begin, verts_end):
                    for j in range(4):
                        mesh["skinIndices"][i*4+j] = bone_indices[mesh["skinIndices"][i*4+j]]

        if facs_data_size > 0:
            reader.jump(facs_data_size)

        return mesh






def write_obj_from_mesh_json(mesh, out_path, lod_index=0, object_name="mesh"):
    flip_v=False
    ver = mesh["version"] 
    V = mesh["vertices"]                  # flat [x,y,z,...]
    N = mesh.get("normals")               # flat [nx,ny,nz,...]  (optional)
    UV = mesh.get("uvs")                  # flat [u,v,...]       (optional)
    F  = mesh["faces"]                    # flat [i0,i1,i2, i3,i4,i5, ...] (0-based)
    LOD = mesh.get("lods") or [0, len(F)//3]  # fallback: single range if no LODs present
    if float(ver) == 1.00:
        flip_v=True


    # choose one LOD's face range
    if lod_index < 0 or lod_index >= len(LOD):
        raise IndexError("lod_index out of range for provided 'lods'")

    start_face = LOD[lod_index]
    end_face   = (LOD[lod_index + 1] if lod_index + 1 < len(LOD) else len(F)//3)

    # slice the faces (each face = 3 indices)
    face_indices = F[start_face*3 : end_face*3]

    nv = len(V) // 3
    nn = (len(N)//3) if N else 0
    nt = (len(UV)//2) if UV else 0

    # Sanity: Roblox indices are 0-based; OBJ wants 1-based.
    def idx1(i): return i + 1

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Generated from Roblox mesh JSON (v{mesh.get('version','?')})\n")
        f.write(f"# Hello from RBX_Toolbox ;)\n")
        f.write(f"o {object_name}\n")

        # positions
        for i in range(0, len(V), 3):
            f.write(f"v {V[i]:.6f} {V[i+1]:.6f} {V[i+2]:.6f}\n")

        # uvs (optional)
        if UV:
            for i in range(0, len(UV), 2):
                u, v = UV[i], UV[i+1]
                if flip_v:  # not needed for v4+, only v1.00 quirk per spec
                    v = 1.0 - v
                f.write(f"vt {u:.6f} {v:.6f}\n")

        # normals (optional)
        if N:
            for i in range(0, len(N), 3):
                f.write(f"vn {N[i]:.6f} {N[i+1]:.6f} {N[i+2]:.6f}\n")

        # faces
        use_uvs = UV is not None and nt == nv
        use_nrm = N  is not None and nn == nv

        # Write f lines as vi[/ti][/ni] with matched indices.
        # In Roblox v2+ the index usually addresses a single "wedge" vertex
        # so pos/uv/normal share the same index — if your arrays align, this keeps them in sync.
        for i in range(0, len(face_indices), 3):
            a, b, c = face_indices[i], face_indices[i+1], face_indices[i+2]

            if use_uvs and use_nrm:
                f.write(f"f {idx1(a)}/{idx1(a)}/{idx1(a)} {idx1(b)}/{idx1(b)}/{idx1(b)} {idx1(c)}/{idx1(c)}/{idx1(c)}\n")
            elif use_uvs and not use_nrm:
                f.write(f"f {idx1(a)}/{idx1(a)} {idx1(b)}/{idx1(b)} {idx1(c)}/{idx1(c)}\n")
            elif use_nrm and not use_uvs:
                f.write(f"f {idx1(a)}//{idx1(a)} {idx1(b)}//{idx1(b)} {idx1(c)}//{idx1(c)}\n")
            else:
                f.write(f"f {idx1(a)} {idx1(b)} {idx1(c)}\n")




'''mesh_file = r""
#mesh_file = r""
otput_obj = r""
with open(mesh_file, "rb") as f:
    data = f.read()'''

#mesh = RBXMeshParser.parse(data)
#import json
#print(json.dumps(mesh, indent=2))
#with open(r"C:\Users\tommy.ds\Downloads\mesh.json", "w") as f:
    #json.dump(mesh, f, indent=2)


#write_obj_from_mesh_json(mesh, otput_obj, lod_index=0, object_name="mesh")

