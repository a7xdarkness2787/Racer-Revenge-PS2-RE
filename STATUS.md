# Reverse-Engineering Status

**Record date:** 2026-10-08  
**Canonical build:** North American retail `SLUS_202.68`

## Overall

Estimated overall research maturity: **about 34%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game. It is not a playable-game percentage and is not a claim that 34% of machine code has been semantically recovered.

| Area | Weight | Evidence score | Current state |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail target and extracted manifests recorded |
| Executable, platform and object system | 10% | 35% | Major resource/config/collision/geometry loader families address-backed |
| Containers and asset formats | 15% | 70% | RES, PHY, SPL, COL and complete PSG render serialization documented with repeatable tooling |
| Tracks, world and collision | 15% | 32% | Track graph and complete COL corpus mapped; PSG/COL coordinate relationships partly cross-validated |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod component geometry/collision relationships exposed |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing/AI markers exposed |
| Renderer, textures and effects | 15% | 40% | Complete PSG payload grammar, VIF attributes, position decode, hierarchy tags, LOD/material blocks and strip topology recovered |
| Camera, audio, UI and save behavior | 5% | 8% | Major file families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime trace yet |
| Reproducibility and closure | 3% | 65% | Full-corpus verifiers, machine-readable state, records and stable format notes retained |

Weighted total is approximately **34.2%**, rounded to **34%**.

## Latest renderer milestone

The detailed PSG parser now validates **all 9,917 retail PSG resources** from all 103 RES containers.

Complete-corpus totals:

- 17,942 hierarchy descriptors
- 22,175 material/VIF blocks
- 366,935 MSCNT geometry batches
- 4,869,177 submitted position records
- 872,158 serialized strip starts
- 3,124,861 reconstructed triangles
- parser failures: 0
- topology warnings under the corrected strip rule: 0
- unexplained payload bytes: 0

The earlier assumption that triangle vertices must share one transform index was invalidated. W magnitude is a per-vertex hierarchy transform index; W sign seeds/restarts triangle strips.

The four previously suspected CableShadow exceptions are therefore no longer format exceptions.

## Other verified coverage

- RES: 103/103 containers
- PHY: 23/23 pod configurations
- SPL: 26/26 track graphs
- COL: 2,505/2,505 resources, 222,577 BVH nodes
- PSG: 9,917/9,917 detailed render payloads

## Highest-priority unknowns

- hierarchy matrix composition for assembled/articulated PSG geometry
- VU microprogram and GIF/GS output
- material-block `+0x08` float and remaining flag semantics
- exact LOD runtime metric
- direct texture proof for V2-16
- V4-8 channel semantics
- pod upgrade A/B/C selection/interpolation
- race/checkpoint/AI runtime consumers
- retained PCSX2 runtime oracle

See `database/questions-current.json` and `CURRENT_WORK.md`.
