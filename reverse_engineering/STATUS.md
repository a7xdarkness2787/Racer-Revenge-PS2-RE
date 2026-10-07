# Reverse-engineering status

Baseline date: 2026-10-07  
Last evidence update: 2026-10-07

## Overall

Estimated overall research maturity: **about 24%**

This percentage measures progress toward a documented, reproducible understanding of the North American retail PS2 game. It is not a playable-game percentage and is not a claim that 24% of the machine code has been semantically recovered.

The current increase is driven by complete outer RES parsing, address-backed PHY/SPL/COL work, and a complete fixed-table pass over all embedded PSG resources.

| Area | Weight | Current evidence score | Notes |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail identity and complete extracted manifests available |
| Executable, platform and object system | 10% | 28% | Resource, pod config, TunnelTrack, collision and surface-geometry loader families address-backed |
| Containers and asset formats | 15% | 50% | RES, PHY, SPL, COL and PSG fixed tables documented with repeatable tooling |
| Tracks, world and collision | 15% | 28% | Track graph and complete COL corpus structurally mapped; world render payload still open |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod collision/geometry hierarchies exposed; equations and upgrade selection remain open |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing flags exposed; higher-level state logic remains open |
| Renderer, textures and effects | 15% | 5% | PSG object/material tables mapped; PS2 geometry payload/VIF/VU/GS details remain open |
| Camera, audio, UI and save behavior | 5% | 8% | CAM/INI/JUK families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime capture yet |
| Reproducibility and closure | 3% | 40% | RES/PHY/SPL/COL/PSG inspection tools and dated records retained |

Weighted total from this rubric is approximately **23.9%**, rounded to **24%**.

## Latest verified developments

### Resource containers

All 103 retail `.RES` containers parse under the recovered version-3 layout, exposing 34,128 logical resources and 44,861 zlib chunks.

### Pod physics and track graph

All 23 pod `.phy` configurations and all 26 track `.spl` graphs parse. Address-backed loaders expose runtime physics fields, 0x80-byte TunnelTrack nodes and packed routing/AI flags.

### Collision

All 2,505 embedded `.col` resources parse exactly across three serialized types. The corpus contains 222,577 verified BVH nodes, and the executable collision dispatcher/readers are mapped.

### Surface geometry fixed tables

All **9,917** embedded `.psg` files now pass a fixed-table parser:

- 17,942 object descriptors
- 22,175 material-name records
- one rooted object hierarchy per file
- 0xe0-byte object descriptors
- 0x40-byte material names
- exact payload boundary for every file

The executable create path around `0x0026e820`, hierarchy reader at `0x0028cac0`, and material-name reader at `0x0026e640` independently confirm those structures.

The PS2-specific geometry command payload after the fixed tables is not yet decoded.

See the stable notes under `reverse_engineering/formats/` and `reverse_engineering/executable/`.

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
