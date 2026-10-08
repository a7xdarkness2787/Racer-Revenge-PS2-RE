# Development Log

Concise chronological index of meaningful reverse-engineering developments. Detailed evidence belongs in `records/`, `analysis/`, stable subsystem documents, and Git history.

## 2026-10-07 — Canonical retail target established
North American retail disc identity, filesystem conversion identity and `SLUS_202.68` baseline were recorded.

## 2026-10-07 — RES container format structurally recovered
**Status:** VERIFIED / OBSERVED executable linkage

All 103 retail RES files passed one bounded version-3 parser: 34,128 logical resource entries and 44,861 compressed chunks.

## 2026-10-07 — Pod physics and TunnelTrack graph mapped
**Status:** VERIFIED file structure / OBSERVED executable field mapping

All 23 pod PHY resources and all 26 SPL resources parse; key executable consumers are address-backed.

## 2026-10-07 — Collision format recovered across complete corpus
**Status:** VERIFIED structure / OBSERVED executable conversion

All 2,505 COL resources pass the parser. Full-corpus testing established the corrected 0.005 minimum-half-extent BVH metric across 222,577 nodes.

## 2026-10-07 — PSG hierarchy and material tables recovered
**Status:** VERIFIED fixed tables

All 9,917 embedded PSG files pass the fixed-table parser: 17,942 hierarchy descriptors and 22,175 material names.

## 2026-10-07 — Repository research structure formalized
The standalone research tree was organized around the evidence-first layout used by the companion Episode I Racer retail RE project.

## 2026-10-07 — First PSG VIF payload block verified
**Status:** VERIFIED sample structure / OBSERVED executable linkage

All 881 sampled first PSG packets begin with the same VIF anchor and decode without unknown command or packet-boundary failure.

## 2026-10-07 — PSG VIF geometry batch grammar recovered
**Status:** VERIFIED serialized/VU layout / semantic attributes still inferred

The 881-file sample contains 12,356 MSCNT-terminated batches. Each batch encodes its element count `N` in a fixed header and lays position-width, V3-8, V2-16 and optional V4-8 streams into contiguous VU destinations.

Observed forms:

- 11,710 compressed-position batches with the optional fourth stream;
- 540 compressed-position batches without it;
- 106 V4-32-position batches.

All 12,356 destination layouts validate.

Evidence:
- `analysis/2026-10-07-psg-vif-payload.md`
- `formats/PSG.md`
- `raw/2026-10-07-psg-vif-summary.txt`
