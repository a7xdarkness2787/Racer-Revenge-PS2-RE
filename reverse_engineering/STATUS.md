# Reverse-engineering status

Baseline date: 2026-10-07  
Last evidence update: 2026-10-07

## Overall

Estimated overall research maturity: **about 21%**

This percentage measures progress toward a documented, reproducible understanding of the North American retail PS2 game. It is not a playable-game percentage and is not a claim that 21% of the machine code has been semantically recovered.

The current increase is driven by complete outer RES parsing plus address-backed PHY, SPL and COL format/loader work.

| Area | Weight | Current evidence score | Notes |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail identity and extracted manifests are available |
| Executable, platform and object system | 10% | 25% | Resource, pod config, TunnelTrack and collision loaders are address-backed |
| Containers and asset formats | 15% | 45% | RES, PHY, SPL and all three serialized COL types documented with reproducible parsers |
| Tracks, world and collision | 15% | 25% | Track graph mapped; 2,505 collision resources parse; geometry/render formats still open |
| Vehicle physics, boost and damage | 15% | 17% | PHY runtime offsets plus pod collision families now exposed; equations/upgrade selection remain open |
| Race logic, AI and progression | 10% | 3% | SPL graph and authored AI/race flags exposed; higher-level behavior remains open |
| Renderer, textures and effects | 15% | 0% | PSG/PSM/PST/VIF/VU/GS behavior not yet mapped |
| Camera, audio, UI and save behavior | 5% | 8% | CAM/INI/JUK families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime capture yet |
| Reproducibility and closure | 3% | 35% | RES, PHY, SPL and COL tools plus dated evidence records are retained |

Weighted total from this rubric is approximately **21.3%**, rounded to **21%**.

## Latest verified developments

### Resource containers

All 103 retail `.RES` containers parse under the recovered version-3 layout, exposing 34,128 logical resources and 44,861 zlib chunks.

### Pod physics

All 23 retail pod `.phy` configurations parse. The loader beginning at `0x002146c0` maps authored physics/control/damage values into stable runtime offsets.

### Track graph

All 26 retail `.spl` resources parse, containing 4,999 nodes and 5,108 explicit edges. The `TunnelTrack` loader at `0x002a1260..0x002a1d70` establishes a 0x80-byte runtime node and the packed routing/AI flag byte.

### Collision

All **2,505** embedded `.col` resources now parse exactly:

- 2,292 type-0 static triangle trees
- 9 type-1 compound static trees
- 204 type-2 two-point trees

The corpus contains 222,577 verified BVH nodes. Their first float is the AABB volume after clamping each half-extent to a minimum of 0.005. Child bit 15 distinguishes leaves from internal nodes.

The executable validates the COL magic/tag/version and dispatches at `0x00124f80` to readers at `0x00125890`, `0x00126450`, and `0x00126640`.

See `formats/RES.md`, `formats/PHY.md`, `formats/SPL.md`, `formats/COL.md` and the matching executable/record notes.

## Confirmed disc-level dataset counts

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

Disc-level counts must not be mixed with the much larger embedded-resource counts recovered from RES directories.
