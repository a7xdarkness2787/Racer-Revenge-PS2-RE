# Runtime Oracle

Static reconstruction is only one half of the research program. This directory defines repeatable PCSX2 runtime captures for the canonical North American retail build.

Initial goals:

- stable emulator/version identity;
- deterministic initial state;
- controlled input sequence;
- known frame/tick definition;
- address-based state capture;
- repeatable output schema;
- first-divergence comparison against an implementation or independent model.

Highest-value initial observations are RES/PSG/COL object lifetimes, pod values after upgrade selection, TunnelTrack current-node/progress state, collision contact results and geometry/material ownership.

No runtime capture is promoted to `VERIFIED` until the procedure is repeatable and documented.
