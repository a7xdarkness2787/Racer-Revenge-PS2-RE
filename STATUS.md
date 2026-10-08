# Reverse-Engineering Status

**Record date:** 2026-10-08  
**Canonical build:** North American retail `SLUS_202.68`

## Overall

Estimated overall research maturity: **about 30%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game. It is not a playable-game percentage and is not a claim that 30% of machine code has been semantically recovered.

| Area | Weight | Evidence score | Current state |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail target and extracted manifests recorded |
| Executable, platform and object system | 10% | 33% | Major resource/config/collision/geometry loader families address-backed |
| Containers and asset formats | 15% | 60% | RES, PHY, SPL, COL and PSG fixed structures documented; detailed PSG payload closed for an 881-file canonical sample |
| Tracks, world and collision | 15% | 29% | Track graph and complete COL corpus structurally mapped; render/collision bounds cross-validated on POD components |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod component geometry/collision ownership exposed |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing/AI markers exposed |
| Renderer, textures and effects | 15% | 27% | PSG LOD/material/VIF layout, position decode, ordinary strip topology and object ownership recovered in the detailed sample |
| Camera, audio, UI and save behavior | 5% | 8% | Major file families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime trace yet |
| Reproducibility and closure | 3% | 55% | Stable specs, machine-readable state, parsers and mesh reconstruction tooling retained |

Weighted total is approximately **30%**.

## Latest renderer result

The detailed canonical PSG payload sample now includes every PSG embedded in POD01, TA and TB:

- PSG files: **881**
- LOD groups: **890**
- material/VIF blocks: **1,216**
- MSCNT geometry batches: **18,965**
- submitted positions: **250,514**
- file-level parse failures: **0**
- unexplained bytes after the known optional tail: **0**

Recovered behavior includes the 0x24-byte render header, LOD groups and thresholds, material-block ownership, signed V4-16/V4-32 position decoding, hierarchy object ownership encoded in position W, ordinary triangle-strip reconstruction, strongly validated V3-8 normals, and multi-object remap tails.

VIF control bits are now also validated across every sampled geometry batch: positions/normals/V2-16 use signed expansion, V4-8 uses unsigned expansion, and all geometry UNPACK ADDR fields are VIF1_TOPS-relative. Material-block bit `0x8` tracks V4-8 presence in 1,216/1,216 blocks.

All 865 single-object sample PSGs reproduce their fixed bounds within one position quantization unit.

Six POD01 render components also match corresponding type-0 COL bounds to floating-point precision, independently validating the render coordinate recovery.

The four `CableShadow*.psg` resources remain a known special topology exception.

## Full-corpus coverage still retained

- RES: 103/103 containers
- PHY: 23/23 pod configurations
- SPL: 26/26 track graphs
- COL: 2,505/2,505 resources, 222,577 BVH nodes
- PSG fixed tables: 9,917/9,917 resources

Detailed PSG render-payload statistics currently cover the 881-file POD01/TA/TB sample and must not be presented as 9,917-file payload coverage.

## Highest-priority unknowns

- VU microprogram and GIF/GS output
- remaining material-block flag bits and metric semantics
- exact LOD runtime selection metric
- direct texture proof for V2-16 and channel meaning for V4-8
- CableShadow special geometry path
- full 9,917-file PSG payload validation
- pod upgrade A/B/C selection/interpolation
- race/checkpoint/AI runtime consumers
- retained PCSX2 runtime oracle

See `database/questions-current.json` and `CURRENT_WORK.md`.
