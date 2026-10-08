# Development Log

Concise chronological index of meaningful reverse-engineering developments. Detailed evidence belongs in `records/`, `analysis/`, stable subsystem documents, and Git history.

## 2026-10-07 — Canonical retail target established
North American retail disc identity, filesystem conversion identity and `SLUS_202.68` baseline were recorded.

## 2026-10-07 — RES container format structurally recovered
**Status:** VERIFIED / OBSERVED executable linkage

All 103 retail RES files passed one bounded version-3 parser: 34,128 logical resource entries and 44,861 compressed chunks. The `LoadResourceFile` candidate at `0x0012cea0..0x0012dca0` independently exposes version and 0x6000-block behavior.

## 2026-10-07 — Pod physics and TunnelTrack graph mapped
**Status:** VERIFIED file structure / OBSERVED executable field mapping

All 23 pod PHY resources parse; the pod configuration consumer at `0x002146c0` supplies runtime field offsets. All 26 SPL resources parse, exposing 4,999 nodes and 5,108 explicit edges.

## 2026-10-07 — Collision format recovered across complete corpus
**Status:** VERIFIED structure / OBSERVED executable conversion

All 2,505 COL resources pass the parser. Full-corpus testing corrected the BVH volume interpretation by proving the 0.005 minimum half-extent rule across 222,577 nodes.

## 2026-10-07 — PSG hierarchy and material tables recovered
**Status:** VERIFIED fixed tables

All 9,917 embedded PSG files pass the fixed-table parser: 17,942 hierarchy descriptors and 22,175 material-name records.

## 2026-10-07 — Repository research structure formalized
The standalone research tree was organized around the same evidence-first model as the companion Episode I Racer retail RE project.

## 2026-10-07 — First PSG VIF payload block verified
**Status:** VERIFIED sample structure / OBSERVED executable linkage

A canonical 881-PSG sample from POD01, TA and TB establishes a 0x40-byte first payload descriptor followed by a descriptor-sized VIF packet. Descriptor `+0x3c` gives the packet byte size.

All 881 first packets begin with `0x6c018000` and are fully walkable using standard VIF command/data lengths. The sampled command stream contains UNPACK V4-32, V4-16, V3-8, V2-16 and V4-8 plus MSCNT and padding.

Executable code at `0x00246a58..0x00246a9c` emits the same `0x6c018000` VIF constant, tying the serialized PSG bytes to the PSXSurfaceGeometry rendering path.

Evidence:
- `analysis/2026-10-07-psg-vif-payload.md`
- `formats/PSG.md`
- `executable/psx_surface_geometry.md`
- `scripts/psg_vif_inspect.py`
- `raw/2026-10-07-psg-vif-summary.txt`
