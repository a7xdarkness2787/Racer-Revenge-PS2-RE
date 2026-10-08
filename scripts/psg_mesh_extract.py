#!/usr/bin/env python3
"""Parse and reconstruct ordinary Racer Revenge PS2 PSG mesh payloads.

The tool expects an extracted .psg supplied by the user. It never downloads or
contains retail game data. CableShadow resources use a special topology and are
reported but not exported as ordinary strips unless --allow-special is given.
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


class PsgError(ValueError):
    pass


def fixed_string(data: bytes, label: str) -> str:
    try:
        end = data.index(0)
    except ValueError as exc:
        raise PsgError(f"{label}: missing NUL terminator") from exc
    if any(data[end + 1 :]):
        raise PsgError(f"{label}: non-zero padding")
    return data[:end].decode("ascii")


def fixed_tables(blob: bytes):
    if len(blob) < 12 or blob[:4] != b"psg\0":
        raise PsgError("not a PSG file")
    version, object_count = struct.unpack_from("<II", blob, 4)
    if version != 3:
        raise PsgError(f"unsupported PSG version {version}")

    objects = []
    pos = 12
    for i in range(object_count):
        if pos + 0xE0 > len(blob):
            raise PsgError("object table exceeds file")
        rec = blob[pos : pos + 0xE0]
        parent = struct.unpack_from("<I", rec, 0xDC)[0]
        objects.append({
            "name": fixed_string(rec[:0x80], f"object {i}"),
            "matrix": list(struct.unpack_from("<16f", rec, 0x80)),
            "center": list(struct.unpack_from("<3f", rec, 0xC0)),
            "half_extents": list(struct.unpack_from("<3f", rec, 0xCC)),
            "radius_like": struct.unpack_from("<f", rec, 0xD8)[0],
            "parent": None if parent == 0xFFFFFFFF else parent,
        })
        pos += 0xE0

    if pos + 4 > len(blob):
        raise PsgError("missing material count")
    material_count = struct.unpack_from("<I", blob, pos)[0]
    pos += 4
    materials = []
    for i in range(material_count):
        if pos + 0x40 > len(blob):
            raise PsgError("material table exceeds file")
        materials.append(fixed_string(blob[pos:pos + 0x40], f"material {i}"))
        pos += 0x40
    return objects, materials, pos


def unpack_bytes(cmd: int, num: int) -> int:
    base = cmd & 0x7F
    components = ((base >> 2) & 3) + 1
    kind = base & 3
    count = 256 if num == 0 else num
    if kind == 0:
        bits = components * 32
    elif kind == 1:
        bits = components * 16
    elif kind == 2:
        bits = components * 8
    elif components == 4:
        bits = 16
    else:
        raise PsgError(f"invalid UNPACK {base:#x}")
    return (count * bits + 7) // 8


def vif_commands(packet: bytes):
    pos = 0
    out = []
    no_data = {0,1,2,3,4,5,6,7,0x10,0x11,0x13,0x14,0x15,0x17}
    while pos < len(packet):
        if pos + 4 > len(packet):
            raise PsgError("truncated VIF command")
        word = struct.unpack_from("<I", packet, pos)[0]
        imm = word & 0xFFFF
        num = (word >> 16) & 0xFF
        cmd = (word >> 24) & 0xFF
        base = cmd & 0x7F
        start = pos
        pos += 4
        if 0x60 <= base <= 0x7F:
            size = unpack_bytes(cmd, num)
        elif base == 0x20:
            size = 4
        elif base in (0x30, 0x31):
            size = 16
        elif base == 0x4A:
            size = (256 if num == 0 else num) * 8
        elif base in (0x50, 0x51):
            size = imm * 16
        elif base in no_data:
            size = 0
        else:
            raise PsgError(f"unknown VIF command {base:#x} at +{start:#x}")
        if pos + size > len(packet):
            raise PsgError(f"VIF data overruns packet at +{start:#x}")
        data = packet[pos:pos + size]
        pos += (size + 3) & ~3
        if pos > len(packet):
            raise PsgError("VIF padding overruns packet")
        out.append({"base": base, "num": num, "imm": imm, "data": data})
    return out


def vif_batches(packet: bytes):
    current = []
    for cmd in vif_commands(packet):
        if cmd["base"] == 0 and not current:
            continue
        if cmd["base"] != 0:
            current.append(cmd)
        if cmd["base"] == 0x17:
            yield current
            current = []
    if current:
        raise PsgError("unterminated VIF geometry batch")


def decode_packet(packet: bytes, objects, scales, origin, material, lod, block):
    position_scale, normal_scale, uv_u, uv_v = scales
    vertices, normals, uvs, colors, faces, warnings = [], [], [], [], [], []
    batches = strips = 0

    for batch_id, batch in enumerate(vif_batches(packet)):
        batches += 1
        if len(batch) not in (5, 6) or batch[0]["base"] != 0x6C or batch[-1]["base"] != 0x17:
            raise PsgError("unexpected geometry batch grammar")
        header = struct.unpack_from("<4I", batch[0]["data"], 0)
        count = header[0] & 0x7FFF
        if batch[0]["num"] != 1 or batch[0]["imm"] != 0x8000:
            raise PsgError("unexpected geometry header UNPACK")
        if header[1:] != (0x30024000, 0x00000412, 0):
            raise PsgError(f"unexpected geometry header {header!r}")

        p, n, uv = batch[1], batch[2], batch[3]
        if any(cmd["num"] != count for cmd in (p,n,uv)) or n["base"] != 0x6A or uv["base"] != 0x65:
            raise PsgError("attribute stream mismatch")
        color = batch[4] if len(batch) == 6 else None
        if color and (color["base"] != 0x6E or color["num"] != count):
            raise PsgError("color-like stream mismatch")

        base_vertex = len(vertices)
        tags = []
        for i in range(count):
            if p["base"] == 0x6D:
                x,y,z,w = struct.unpack_from("<4h", p["data"], i * 8)
            elif p["base"] == 0x6C:
                x,y,z,w = struct.unpack_from("<4i", p["data"], i * 16)
            else:
                raise PsgError(f"unexpected position UNPACK {p['base']:#x}")
            if w == 0 or abs(w) % 16:
                raise PsgError(f"invalid position W tag {w}")
            object_index = abs(w) // 16 - 1
            if not 0 <= object_index < len(objects):
                raise PsgError(f"object index {object_index} out of range")
            vertices.append({
                "position": [origin[0]+x*position_scale, origin[1]+y*position_scale, origin[2]+z*position_scale],
                "object_index": object_index,
                "w": w,
                "material": material,
            })
            tags.append(w)
            nx,ny,nz = struct.unpack_from("<3b", n["data"], i * 3)
            normals.append([nx*normal_scale, ny*normal_scale, nz*normal_scale])
            u,v = struct.unpack_from("<2h", uv["data"], i * 4)
            uvs.append([u*uv_u, v*uv_v])
            colors.append(list(struct.unpack_from("<4b", color["data"], i*4)) if color else None)

        run_start = None
        active_object = None
        for i,w in enumerate(tags):
            if i + 1 < len(tags) and w < 0 and tags[i+1] < 0 and abs(w) == abs(tags[i+1]):
                run_start = i
                active_object = abs(w)//16 - 1
                strips += 1
            if w <= 0:
                continue
            obj = abs(w)//16 - 1
            if run_start is None or i < run_start+2 or obj != active_object or abs(tags[i-1]) != abs(w) or abs(tags[i-2]) != abs(w):
                warnings.append({"batch": batch_id, "vertex": i, "w": w})
                continue
            tri = i - (run_start + 2)
            a,b,c = base_vertex+i-2, base_vertex+i-1, base_vertex+i
            if tri & 1:
                a,b = b,a
            faces.append({"indices":[a,b,c], "object_index":obj, "material":material, "lod":lod, "block":block})

    return {"vertices":vertices,"normals":normals,"uvs":uvs,"colors":colors,"faces":faces,
            "batch_count":batches,"strip_starts":strips,"topology_warnings":warnings}


def parse(blob: bytes):
    objects, materials, pos = fixed_tables(blob)
    if pos + 0x24 > len(blob):
        raise PsgError("missing render header")
    position_scale, normal_scale, uv_u, uv_v = struct.unpack_from("<4f", blob, pos)
    origin = struct.unpack_from("<3f", blob, pos+0x10)
    origin_present, lod_count = struct.unpack_from("<II", blob, pos+0x1C)
    if origin_present not in (0,1) or lod_count == 0:
        raise PsgError("invalid render header")
    pos += 0x24
    material_base = 0
    lods = []

    for lod_index in range(lod_count):
        if pos + 8 > len(blob):
            raise PsgError("truncated LOD header")
        threshold, block_count = struct.unpack_from("<fI", blob, pos)
        pos += 8
        blocks = []
        for block_index in range(block_count):
            if pos + 0x14 > len(blob):
                raise PsgError("truncated material block")
            slot, flags, metric, packed_counts, packet_size = struct.unpack_from("<IIfII", blob, pos)
            pos += 0x14
            if slot != block_index:
                raise PsgError("non-sequential material slot")
            if packet_size == 0 or packet_size & 0xF or pos + packet_size > len(blob):
                raise PsgError("invalid VIF packet size")
            table_index = material_base + slot
            if table_index >= len(materials):
                raise PsgError("material slot exceeds table")
            packet = decode_packet(blob[pos:pos+packet_size], objects,
                                   (position_scale,normal_scale,uv_u,uv_v), origin,
                                   materials[table_index], lod_index, block_index)
            pos += packet_size
            declared_vertices = packed_counts & 0xFFFF
            if declared_vertices != len(packet["vertices"]):
                raise PsgError("declared vertex count mismatch")
            blocks.append({
                "material_slot":slot,"material_table_index":table_index,"material":materials[table_index],
                "flags":flags,"metric":metric,"declared_strip_count":packed_counts>>16,
                "declared_vertex_count":declared_vertices,"packet_size":packet_size,**packet,
            })
        material_base += block_count
        lods.append({"threshold":threshold,"block_count":block_count,"blocks":blocks})

    if material_base != len(materials):
        raise PsgError("LOD blocks do not consume material table")

    remap = None
    tail = blob[pos:]
    if tail:
        if len(tail) < 12 or len(tail) % 4:
            raise PsgError("unrecognized PSG tail")
        kind, aligned = struct.unpack_from("<II", tail, 0)
        count = struct.unpack_from("<I", tail, len(tail)-4)[0]
        mapping = tail[8:-4]
        expected = (count + 3) & ~3
        if kind != 1 or aligned != expected or len(mapping) != aligned or count != len(objects):
            raise PsgError("unrecognized object-remap tail")
        if list(mapping[:count]) != list(range(count)) or any(mapping[count:]):
            raise PsgError("unexpected object-remap mapping")
        remap = {"kind":kind,"aligned_bytes":aligned,"indices":list(mapping[:count]),"object_count":count}

    return {"objects":objects,"materials":materials,"position_scale":position_scale,
            "normal_scale":normal_scale,"uv_scale":[uv_u,uv_v],"origin":list(origin),
            "origin_present":origin_present,"lods":lods,"object_remap":remap}


def bounds(vertices):
    if not vertices:
        return None,None
    lo=[min(v["position"][a] for v in vertices) for a in range(3)]
    hi=[max(v["position"][a] for v in vertices) for a in range(3)]
    return ([(lo[a]+hi[a])/2 for a in range(3)],[(hi[a]-lo[a])/2 for a in range(3)])


def summary(result):
    lods=[]
    for li,lod in enumerate(result["lods"]):
        blocks=[]
        for block in lod["blocks"]:
            center,half=bounds(block["vertices"])
            blocks.append({"material":block["material"],"flags":f"0x{block['flags']:x}",
                           "metric":block["metric"],"declared_strips":block["declared_strip_count"],
                           "observed_strip_starts":block["strip_starts"],"vertices":len(block["vertices"]),
                           "triangles":len(block["faces"]),"batches":block["batch_count"],
                           "packet_size":block["packet_size"],"bounds_center":center,
                           "bounds_half_extents":half,"topology_warnings":len(block["topology_warnings"])})
        lods.append({"index":li,"threshold":lod["threshold"],"block_count":lod["block_count"],"blocks":blocks})
    return {"object_count":len(result["objects"]),"material_count":len(result["materials"]),
            "position_scale":result["position_scale"],"normal_scale":result["normal_scale"],
            "uv_scale":result["uv_scale"],"origin":result["origin"],"origin_present":result["origin_present"],
            "lod_count":len(result["lods"]),"lods":lods,"object_remap":result["object_remap"]}


def write_obj(result, output: Path, lod_index: int, allow_special: bool):
    if not 0 <= lod_index < len(result["lods"]):
        raise PsgError("LOD out of range")
    lod=result["lods"][lod_index]
    warning_count=sum(len(b["topology_warnings"]) for b in lod["blocks"])
    if warning_count and not allow_special:
        raise PsgError(f"LOD has {warning_count} topology warnings; special primitive path not decoded")
    lines=["# Independently reconstructed from a user-supplied PSG."]
    bases=[]
    total=0
    for block in lod["blocks"]:
        bases.append(total)
        for v in block["vertices"]:
            x,y,z=v["position"]; lines.append(f"v {x:.9g} {y:.9g} {z:.9g}")
        for u,v in block["uvs"]: lines.append(f"vt {u:.9g} {v:.9g}")
        for nx,ny,nz in block["normals"]: lines.append(f"vn {nx:.9g} {ny:.9g} {nz:.9g}")
        total += len(block["vertices"])
    group=material=None
    for bi,block in enumerate(lod["blocks"]):
        base=bases[bi]
        for face in block["faces"]:
            name=result["objects"][face["object_index"]]["name"] or f"object_{face['object_index']}"
            mtl=block["material"] or f"material_{bi}"
            if name != group:
                lines.append("g " + name.replace(" ","_")); group=name
            if mtl != material:
                lines.append("usemtl " + mtl.replace(" ","_")); material=mtl
            a,b,c=[base+i+1 for i in face["indices"]]
            lines.append(f"f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}")
    output.write_text("\n".join(lines)+"\n",encoding="utf-8")


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("psg",type=Path)
    ap.add_argument("--json",action="store_true")
    ap.add_argument("--obj",type=Path)
    ap.add_argument("--lod",type=int,default=0)
    ap.add_argument("--allow-special",action="store_true")
    args=ap.parse_args()
    result=parse(args.psg.read_bytes())
    if args.obj:
        write_obj(result,args.obj,args.lod,args.allow_special)
    row=summary(result)
    if args.json:
        print(json.dumps(row,indent=2))
    else:
        print(f"objects={row['object_count']} materials={row['material_count']} lods={row['lod_count']} position_scale={row['position_scale']:.9g} origin={row['origin']}")
        for lod in row["lods"]:
            verts=sum(b["vertices"] for b in lod["blocks"]); tris=sum(b["triangles"] for b in lod["blocks"])
            warns=sum(b["topology_warnings"] for b in lod["blocks"])
            print(f"  lod {lod['index']}: threshold={lod['threshold']:.9g} blocks={lod['block_count']} vertices={verts} triangles={tris} warnings={warns}")
        if args.obj: print(f"wrote {args.obj}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, UnicodeDecodeError, struct.error, PsgError, ValueError) as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
