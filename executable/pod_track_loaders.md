# Pod and track configuration loader map

Build: North American retail `SLUS_202.68`

This note records executable addresses tied directly to the newly parsed `.phy` and `.spl` configuration families.

## Pod configuration

Current loader candidate:

`0x002146c0`

Evidence:

- direct references to `Pod Setup`, `Physical Properties`, `Repulsor`, `Engine`, `Engine Aerodynamics`, `Pod Animation`, `Collisions`, `Joystick`, `CameraInfo`, `DamageRepair`, `BaseAbilities`, `MaxAbilities`, and `Tuning`
- direct references to individual authored key names
- direct stores from parsed values into stable offsets of the active object
- nearby `PodVehicle.cpp` diagnostic strings
- component/resource construction strings such as `.mcf`, `.col`, particle emitters, cable-shadow resources, binder resources, and engine/chariot names

Verified direct stores include the physical-property, pod-animation, joystick, and selected damage/repair offsets documented in `formats/PHY.md`.

## TunnelTrack spline loader

Current loader:

`0x002a1260..0x002a1d70`

Evidence:

- direct `Track`, `Node%d`, and `Shortcut%d` section lookup
- direct references to every documented spline key
- `TunnelTrack.cpp` diagnostic strings in the same code family
- node allocation with `index << 7`, establishing a 0x80-byte runtime node stride
- explicit edge-array allocation from `NumNextNodes`
- explicit default sequential/wrapping edge construction when `NumNextNodes` is absent
- packed flag-byte masks matching the optional node keys

Useful addresses:

| Address | Observation |
| --- | --- |
| `0x002a1334` | reads `NumNodes` |
| `0x002a136c` | reads `TrackWidth` |
| `0x002a13bc` | reads `StartNode` |
| `0x002a13e4` | reads `NumShortcuts` |
| `0x002a14f8` | reads node `Position` |
| `0x002a152c` | reads `NodeHeight` |
| `0x002a155c` | reads `LeftTrackWidth` |
| `0x002a15a4` | reads `RightTrackWidth` |
| `0x002a15ec` | reads `SpeedLimit` |
| `0x002a161c` | reads `DistanceToFinish` |
| `0x002a164c` | `NodeBlocked` -> flag bit 0x01 |
| `0x002a1708` | `NoCombatZone` -> flag bit 0x02 |
| `0x002a17cc` | `ShortestBranch` -> flag bit 0x04 |
| `0x002a174c` | `SkipPlayerTest` -> flag bit 0x08 |
| `0x002a178c` | `DriveFullSpeed` -> flag bit 0x10 |
| `0x002a180c` | `SecretBranch` -> flag bit 0x20 |
| `0x002a184c` | `Pretty` -> flag bit 0x40 |
| `0x002a188c` | `Ugly` -> flag bit 0x80 |
| `0x002a18cc` | reads `BranchID` |
| `0x002a18fc` | handles `ProgressNode` |
| `0x002a19d4` | reads `NumNextNodes` |
| `0x002a1a38` | reads `Next%d` |
| `0x002a1cb0` | looks up `Shortcut%d` |
| `0x002a1cd8` | reads `PlayerTestNode` |
| `0x002a1d00` | reads `AIBlockNode` |

## Caution

The executable uses R5900 instructions that LLVM's generic MIPS backend does not completely decode. Claims in this note are limited to standard instructions, string references, arithmetic, branches, and stores that are unambiguous in the current disassembly.
