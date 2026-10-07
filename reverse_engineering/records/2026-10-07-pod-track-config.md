# 2026-10-07 — pod physics and track graph investigation

## Scope

Continue from the recovered RES directory by following two high-value embedded resource families:

- pod `.phy` configuration
- track `.spl` graph data

Retail assets were analyzed privately and are not committed.

## VERIFIED — pod physics corpus

All 23 retail pod physics files parse as INI-style text.

Sixteen named configuration families are present in every file, along with `chariot`, `englt1`, and `engrt1` component sections.

`POD02` is the only current structural outlier: it adds lower left/right engines, two additional wreckage parts, and `englt2` / `engrt2` sections.

The configuration contains authored values for thrust, top speed, boost, repair, aerodynamics, repulsor behavior, collision response, control response, damage, cooling and repair.

## OBSERVED — pod configuration consumer

A configuration routine starts at `0x002146c0` and directly references the pod section/key strings. The routine performs direct stores into the active object, providing the first address-backed field map for pod physics.

High-confidence examples:

- `Gravity` -> `+0x378`
- `AirborneGravity` -> `+0x37c`
- `MaxLiftHeight` -> `+0x7ec`
- pod-animation parameters occupy a dense region beginning at `+0x9f0`
- joystick steering parameters occupy `+0xb84..+0xb98`
- selected defense/repair/cooling values occupy `+0xcf0..+0xcf8`

The exact class/object boundary is not yet named as a formal type.

## VERIFIED — track spline corpus

All 26 retail `.spl` resources parse successfully.

Aggregate:

- 4,999 nodes
- 5,108 explicit directed edges
- 103 branch nodes
- 88 minimum nodes in one spline
- 293 maximum nodes in one spline

Optional routing/AI markers are present in authored data, including `SkipPlayerTest`, `SecretBranch`, `NoCombatZone`, `ProgressNode`, `DriveFullSpeed`, `NodeBlocked`, `Pretty`, and `Ugly`.

## VERIFIED — TunnelTrack parser map

The executable routine `0x002a1260..0x002a1d70` reads the spline files.

Important new structural findings:

- runtime node stride is `0x80`
- node count is stored at track object `+0x34`
- node-array pointer is stored at `+0x30`
- top-level track width is stored at `+0x38`
- per-node `LeftTrackWidth` and `RightTrackWidth` are adjusted by adding half the top-level `TrackWidth`
- `BoostScale` is converted to float and defaults to 1.0
- `BranchID` is stored at node `+0x68`
- next-node array pointer/count are node `+0x6c/+0x70`
- eight authored node markers are packed into flag byte `+0x79`
- missing `NumNextNodes` creates an implicit sequential edge, with the last node wrapping to zero
- `ProgressNode` entries are tracked in a maximum-10 list and force the node-height slot to 10000.0
- shortcut entries, when present, are 8-byte pairs populated from `PlayerTestNode` and `AIBlockNode`

## Correction / caution

LLVM's generic MIPS disassembler reports several R5900 operations as unknown or as generic instructions with misleading names. Position-vector storage and any claim that depends on those opcodes remains open. The structure offsets above are limited to unambiguous standard loads/stores, shifts, masks and floating-point arithmetic.

## Next

- map the remaining position-vector fields in the 0x80-byte TunnelTrack node with an R5900-aware disassembly
- trace the next-node graph into race progression and AI path selection
- connect `Defense`, thrust and top-speed runtime slots to the upgrade-selection calculation
- follow one pod geometry `.psg` and collision `.col` resource into its consumer
