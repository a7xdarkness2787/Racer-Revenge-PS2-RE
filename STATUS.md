# Reverse-Engineering Status

**Record date:** 2026-10-07  
**Canonical build:** North American retail `SLUS_202.68`

## Overall

Estimated overall research maturity: **about 26%**

This percentage measures progress toward a documented, reproducible understanding of the retail PS2 game. It is not a playable-game percentage and is not a claim that 26% of machine code has been semantically recovered.

| Area | Weight | Evidence score | Current state |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail target and extracted manifests recorded |
| Executable, platform and object system | 10% | 30% | Resource, pod config, TunnelTrack, collision and PSXSurfaceGeometry families address-backed |
| Containers and asset formats | 15% | 53% | RES, PHY, SPL, COL and PSG fixed tables plus the first PSG VIF block documented |
| Tracks, world and collision | 15% | 28% | Track graph and complete COL corpus structurally mapped |
| Vehicle physics, boost and damage | 15% | 18% | PHY runtime offsets and pod collision/geometry hierarchy exposed |
| Race logic, AI and progression | 10% | 3% | SPL graph and routing/AI markers exposed; higher-level logic remains open |
| Renderer, textures and effects | 15% | 14% | PSG hierarchy/material tables and first VIF packet structure now verified in an 881-file sample |
| Camera, audio, UI and save behavior | 5% | 8% | Major file families inventoried; code behavior mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime trace yet |
| Reproducibility and closure | 3% | 45% | RES/PHY/SPL/COL/PSG/VIF tools, raw summaries and dated evidence retained |

Weighted total is approximately **25.8%**, rounded to **26%**.

## Canonical target

- executable: `SLUS_202.68`
- executable size: `2,972,720` bytes
- SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

## Verified format coverage

### RES
103/103 containers parse; 34,128 logical resources; 44,861 zlib chunks.

### PHY
23/23 pod configurations parse; consolidated and pod-local copies match 23/23; config consumer begins at `0x002146c0`.

### SPL
26/26 track graphs parse; 4,999 nodes; 5,108 explicit edges; TunnelTrack loader `0x002a1260..0x002a1d70`.

### COL
2,505/2,505 collision resources parse; 222,577 verified BVH nodes; dispatcher `0x00124f80`.

### PSG fixed tables
9,917/9,917 files pass fixed-table validation; 17,942 object descriptors; 22,175 material-name records.

### PSG first VIF block
A focused canonical sample from POD01, TA and TB contains **881 PSG resources**.

All 881 have:

- a 0x40-byte first payload descriptor;
- a u32 VIF packet byte size at descriptor `+0x3c`;
- a 16-byte-aligned, in-bounds first packet;
- first VIF word `0x6c018000`;
- a first packet fully consumable by the current bounded VIF decoder.

The executable independently emits the same `0x6c018000` constant in the PS2 surface-geometry path at `0x00246a58..0x00246a9c`.

## Highest-priority unknowns

- semantic names for the remaining PSG 0x40 descriptor fields
- additional PSG payload records after the first VIF packet
- material indices and VU/GIF/GS semantics
- signed-16 collision vertex dequantization
- exact pod upgrade A/B/C selection/interpolation
- track graph connection to checkpoint/progression and AI decisions
- retained PCSX2 runtime capture/oracle

See `database/questions-current.json` and `CURRENT_WORK.md`.
