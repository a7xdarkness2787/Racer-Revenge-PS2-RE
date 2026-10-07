# Reverse-engineering status

Baseline date: 2026-10-07

## Overall

Estimated overall completion: **4%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game, not toward a playable reimplementation.

| Area | Status | Notes |
| --- | ---: | --- |
| Input preservation / provenance | 90% | Source BIN/CUE and converted ISO hashes recorded |
| Disc filesystem inventory | 35% | Full extracted-file manifest and extension counts available |
| Executable reconnaissance | 8% | Main ELF identified; strings reveal extensive C++ class/source information |
| Resource container formats | 3% | Format families identified; independent verification pending |
| Pod data | 3% | Pod dataset preserved for analysis |
| Track data | 3% | Track dataset preserved for analysis |
| Audio | 10% | VAG/INI/JUK/JUB organization inventoried |
| Gameplay / race logic | 1% | Named systems visible in executable strings; behavior not mapped |
| Physics / collision | 1% | Candidate classes and diagnostics identified |
| AI | 1% | Initial executable evidence only |
| Camera | 2% | Camera class/config names visible |
| Renderer / VU / GS | 1% | PS2 rendering paths not yet mapped |
| Runtime validation | 0% | PCSX2 tracing plan not started |

## Confirmed dataset counts

- 2,010 `.VAG`
- 136 `.INI`
- 103 `.RES`
- 23 `.CAM`
- 18 `.PST`
- 8 `.IRX`
- 3 `.PSS`
- 3 `.JUK`
- 2 `.LSI`
- 2 `.JUB`

These counts come from the preserved extracted retail filesystem.
