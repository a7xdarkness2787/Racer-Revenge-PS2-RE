# Current work

## Active target

Trace the resource system from `SLUS_202.68` into one complete pod and track dependency chain.

## Latest development

The outer retail `.RES` format is no longer only a string/header hypothesis.

A bounded parser now reconstructs all 103 extracted retail containers with 103/103 passing the same version-3 rules. The corpus contains 34,128 directory records and 44,861 compressed chunks. Each chunk expands to `0x6000` bytes and is followed by `0xff`; directory offsets address a reconstructed virtual data stream.

`UI/PODPHYS.RES` contains 23 `.phy` resources. Each one is byte-identical to the `.phy` copy inside its corresponding `PODS/PODxx/PODxx.RES` bundle.

The executable routine at `0x0012cea0..0x0012dca0` is strongly anchored as the current `LoadResourceFile` candidate by direct references to its own `DataAccess.cpp` diagnostics. Standard MIPS instructions in that routine independently show `0x6000` block handling and a version check that includes the retail version 3 path.

## Current evidence files

- `formats/RES.md`
- `executable/resource_loader.md`
- `scripts/res_inspect.py`
- `records/2026-10-07-res-container.md`

## Next targets

1. Follow a `POD01.RES` geometry/material resource from the reconstructed directory into the executable consumer.
2. Trace one `UI/PODPHYS.RES` `.phy` read into `PodPhysicsObject` state and identify the first typed fields.
3. Map `TA.RES` and `TB.RES` top-level `.tob`, `.aub`, `.scb`, `.col`, `.psg` and `.spl` consumers without assuming extension semantics from names alone.
4. Retain an Emotion Engine-aware disassembly export so R5900-only instructions in the loader can be named safely.
5. Start a nonempty PCSX2 runtime capture after the first loader/object addresses are stable.

## Evidence rule

New findings should be written into the dated record and stable subsystem note as soon as they change the current understanding. Failed hypotheses and corrected interpretations stay in the record rather than being silently removed.
