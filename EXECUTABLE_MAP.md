# Executable Map

**Canonical target:** `SLUS_202.68`  
**SHA-256:** `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

## Resource system

| Address/range | Identification |
| --- | --- |
| `0x0012cea0..0x0012dca0` | `LoadResourceFile` candidate |
| `0x0012d330` | RES read-error path |
| `0x0012d370` | RES wrong-version path |
| `0x0012d5cc` | 0x6000 amount check |
| `0x0012d740` | 0x6000 buffer advance |

## Collision

| Address/range | Identification |
| --- | --- |
| around `0x0011b920` | COL open/header validation wrapper |
| `0x00124f80` | collision type dispatcher |
| `0x00125890` | type-0 static collision reader |
| `0x00126450` | type-1 compound collision reader |
| `0x00126640` | type-2 collision reader |

## Pod configuration

`0x002146c0` — pod configuration loader candidate, anchored by PHY section/key strings and stable runtime stores.

## PS2 surface geometry

| Address/range | Identification |
| --- | --- |
| `0x00246300` | PS2 serialized geometry/packet helper |
| around `0x002469c0` | VIF packet construction family |
| `0x00246a58..0x00246a9c` | emits VIF data including `0x6c018000` |
| `0x0026e34c` | higher-level loader call into `0x00246300` |
| `0x0026e640` | PSG material-name table reader |
| around `0x0026e820` | SurfaceGeometry create/open/format-validation path |
| `0x0028cac0` | PSG hierarchy descriptor reader |

## TunnelTrack

`0x002a1260..0x002a1d70` — TunnelTrack spline/graph loader.

## Current address frontier

- VU microprogram and MSCNT execution target
- material/render-state handling and GIF/GS submission
- exact LOD comparison metric
- multi-object remap-tail runtime use
- s16 collision vertex dequantization
- pod A/B/C upgrade selection/interpolation
- race/checkpoint/AI consumers of TunnelTrack flags and branches
