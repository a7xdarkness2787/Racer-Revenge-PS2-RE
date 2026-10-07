# Development Log

Concise chronological index of meaningful reverse-engineering developments. Detailed evidence belongs in `records/`, `analysis/`, stable subsystem documents, and Git history.

## 2026-10-07 — Canonical retail target established
North American retail disc identity, filesystem conversion identity and `SLUS_202.68` baseline were recorded.

## 2026-10-07 — RES container format structurally recovered
**Status:** VERIFIED / OBSERVED executable linkage

All 103 retail RES files passed one bounded version-3 parser: 34,128 logical resource entries and 44,861 compressed chunks. The `LoadResourceFile` candidate at `0x0012cea0..0x0012dca0` independently exposes version and 0x6000-block behavior.

Evidence: `formats/RES.md`, `records/2026-10-07-res-container.md`, `executable/resource_loader.md`.

## 2026-10-07 — Pod physics and TunnelTrack graph mapped
**Status:** VERIFIED file structure / OBSERVED executable field mapping

All 23 pod PHY resources parse; the pod configuration consumer at `0x002146c0` supplies runtime field offsets. All 26 SPL resources parse, exposing 4,999 nodes and 5,108 explicit edges. TunnelTrack loader: `0x002a1260..0x002a1d70`.

## 2026-10-07 — Collision format recovered across complete corpus
**Status:** VERIFIED structure / OBSERVED executable conversion

All 2,505 COL resources pass the parser. Full-corpus testing corrected the BVH volume interpretation by proving the 0.005 minimum half-extent rule across 222,577 nodes.

## 2026-10-07 — PSG hierarchy and material tables recovered
**Status:** VERIFIED fixed tables / payload still open

All 9,917 embedded PSG files pass the fixed-table parser: 17,942 hierarchy descriptors and 22,175 material-name records. Executable readers at `0x0028cac0` and `0x0026e640` independently confirm the table structures.

## 2026-10-07 — Repository research structure formalized
The standalone research tree was promoted to repository root and organized around an evidence-first layout matching the companion Episode I Racer retail RE project. This organizational change does not alter technical findings.
