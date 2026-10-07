# Current work

## Active target

Move from configuration and routing metadata into geometry, collision, race logic and runtime validation.

## Latest development

The resource dependency chain now reaches beyond the outer container.

### Pod side

All 23 pod `.phy` resources are parsed and structurally compared. A loader beginning at `0x002146c0` directly references the authored pod sections/keys and stores many values into stable runtime offsets.

High-confidence mapped regions now include:

- gravity / airborne gravity at `+0x378/+0x37c`
- repulsor lift height at `+0x7ec`
- pod animation forces/torques around `+0x9f0..+0xaac`
- joystick steering controls at `+0xb84..+0xb98`
- selected defense/repair/cooling values at `+0xcf0..+0xcf8`

### Track side

All 26 retail `.spl` graph files parse successfully. The `TunnelTrack` loader at `0x002a1260..0x002a1d70` now has an address-backed structure map.

Confirmed behavior includes:

- 0x80-byte node records
- node array/count at track `+0x30/+0x34`
- per-node speed, distance, branch and outgoing-edge fields
- an explicit next-node array
- implicit sequential/wrapping edges when `NumNextNodes` is absent
- eight packed routing/AI flags at node `+0x79`
- a maximum-10 progress-node list
- optional 8-byte shortcut records using `PlayerTestNode` and `AIBlockNode`

## Current evidence files

- `formats/RES.md`
- `formats/PHY.md`
- `formats/SPL.md`
- `executable/resource_loader.md`
- `executable/pod_track_loaders.md`
- `scripts/res_inspect.py`
- `scripts/phy_inspect.py`
- `scripts/spl_inspect.py`
- `records/2026-10-07-res-container.md`
- `records/2026-10-07-pod-track-config.md`

## Next targets

1. Recover the header and record layout for `.col` collision meshes and tie the reader to executable code.
2. Recover enough `.psg` geometry structure to identify object/mesh boundaries and references to materials/textures.
3. Trace the `TunnelTrack` graph into checkpoint/progress validation and AI path selection.
4. Finish the A/B/C vehicle upgrade-selection calculation and determine how it feeds thrust, top speed, defense, repair and cooling.
5. Retain an Emotion Engine-aware disassembly export for the R5900 vector operations that remain intentionally unnamed.
6. Start a nonempty PCSX2 runtime capture once the collision/geometry load addresses are stable.

## Evidence rule

New findings should be written into the dated record and stable subsystem note as soon as they change the current understanding. Failed hypotheses and corrected interpretations stay in the record rather than being silently removed.
