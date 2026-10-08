# Reverse-Engineering Status

**Record date:** 2026-10-07  
**Canonical build:** North American retail `SLUS_202.68`

## Overall

Estimated overall research maturity: **about 27%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game. It is not a playable-game percentage or a claim that 27% of machine code has been semantically recovered.

| Area | Weight | Evidence score | Current state |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail target and extracted manifests recorded |
| Executable, platform and object system | 10% | 32% | Resource, pod config, TunnelTrack, collision and PSXSurfaceGeometry families address-backed |
| Containers and asset formats | 15% | 55% | RES, PHY, SPL, COL and PSG/VIF structures have repeatable tooling |
| Tracks, world and collision | 15% | 28% | Track graph and complete COL corpus structurally mapped |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod collision/geometry hierarchy exposed |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing/AI markers exposed |
| Renderer, textures and effects | 15% | 18% | PSG hierarchy/materials plus VIF batch grammar verified in 881-file sample |
| Camera, audio, UI and save behavior | 5% | 8% | Major file families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime trace yet |
| Reproducibility and closure | 3% | 48% | Stable specs, tools, raw summaries and dated analysis retained |

Weighted total is approximately **27%**.

## Renderer development

The current POD01/TA/TB sample contains 881 PSG resources and 12,356 MSCNT-terminated VIF batches.

The VIF memory layout is now structurally verified:

- one V4-32 header vector at VU address 0;
- `N` position elements beginning at address 1;
- `N` V3-8 elements at `1+N`;
- `N` V2-16 elements at `1+2N`;
- optional `N` V4-8 elements at `1+3N`;
- MSCNT terminates the batch.

All 12,356 batches use contiguous destinations. The batch header encodes `N` as `0x8000 | N`.

Most batches use V4-16 positions; 106 use V4-32 positions.

The likely position/normal/UV/color interpretation remains explicitly marked inferred until independent geometry/runtime confirmation.

## Other verified coverage

- RES: 103/103 containers
- PHY: 23/23 pod configurations
- SPL: 26/26 track graphs
- COL: 2,505/2,505 resources, 222,577 BVH nodes
- PSG fixed tables: 9,917/9,917 files

## Highest-priority unknowns

- PSG position scaling and primitive topology
- material ownership and VU microprogram
- later PSG payload records
- s16 collision dequantization
- pod upgrade A/B/C selection
- track graph use by race logic/AI
- retained PCSX2 runtime oracle
