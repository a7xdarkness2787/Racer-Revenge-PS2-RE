# Reverse-Engineering Status

**Record date:** 2026-10-07  
**Canonical build:** North American retail `SLUS_202.68`

## Overall

Estimated overall research maturity: **about 24%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game. It is not a playable-game percentage and is not a claim that 24% of machine code has been semantically recovered.

| Area | Weight | Evidence score | Current state |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail target and extracted manifests recorded |
| Executable, platform and object system | 10% | 28% | Resource, pod config, TunnelTrack, collision and surface-geometry loader families address-backed |
| Containers and asset formats | 15% | 50% | RES, PHY, SPL, COL and PSG fixed tables documented with repeatable tooling |
| Tracks, world and collision | 15% | 28% | Track graph and complete COL corpus structurally mapped |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod collision/geometry hierarchy exposed |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing/AI markers exposed; higher-level logic remains open |
| Renderer, textures and effects | 15% | 5% | PSG object/material tables mapped; PS2 geometry payload remains open |
| Camera, audio, UI and save behavior | 5% | 8% | Major file families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime trace yet |
| Reproducibility and closure | 3% | 40% | RES/PHY/SPL/COL/PSG inspection tools and dated evidence records retained |

Weighted total is approximately **23.9%**, rounded to **24%**.

## Canonical target

- executable: `SLUS_202.68`
- executable size: `2,972,720` bytes
- SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

## Verified format coverage

### RES
103/103 containers parse; 34,128 logical resources; 44,861 zlib chunks; exact 0x6000 decoded chunks and no unexplained trailing bytes.

### PHY
23/23 pod physics configurations parse; consolidated and pod-local copies match 23/23; pod configuration consumer begins at `0x002146c0`.

### SPL
26/26 track graph resources parse; 4,999 nodes; 5,108 explicit edges; TunnelTrack loader `0x002a1260..0x002a1d70`; 0x80-byte runtime nodes.

### COL
2,505/2,505 collision resources parse; 222,577 verified BVH nodes; dispatcher `0x00124f80`; readers `0x00125890`, `0x00126450`, `0x00126640`.

### PSG fixed tables
9,917/9,917 files pass fixed-table validation; 17,942 object descriptors; 22,175 material-name records; hierarchy reader `0x0028cac0`; material reader `0x0026e640`.

The PS2-specific geometry payload after the PSG fixed tables remains open.

## Highest-priority unknowns

- PSG payload record boundaries and object ownership
- material indices and VIF/VU/GIF/DMA packet structure
- signed-16 collision vertex dequantization
- exact pod upgrade A/B/C selection/interpolation
- track graph connection to checkpoint/progression and AI decisions
- retained PCSX2 runtime capture/oracle

See `database/questions-current.json` and `CURRENT_WORK.md`.
