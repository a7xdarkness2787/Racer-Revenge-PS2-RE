# Development Log

Concise chronological index of meaningful reverse-engineering developments. Detailed evidence belongs in `records/`, `analysis/`, stable subsystem documents, and Git history.

## 2026-10-07 — Canonical retail target established

North American retail disc identity, filesystem conversion identity and `SLUS_202.68` baseline were recorded.

## 2026-10-07 — RES container format structurally recovered

All 103 retail RES files passed one bounded version-3 parser: 34,128 logical resource entries and 44,861 compressed chunks.

## 2026-10-07 — Pod physics and TunnelTrack graph mapped

All 23 pod PHY resources and all 26 SPL resources parse; key executable consumers are address-backed.

## 2026-10-07 — Collision format recovered across complete corpus

All 2,505 COL resources pass the parser. Full-corpus testing established the corrected 0.005 minimum-half-extent BVH metric across 222,577 nodes.

## 2026-10-07 — PSG hierarchy and material tables recovered

All 9,917 embedded PSG files pass the fixed-table parser: 17,942 hierarchy descriptors and 22,175 material names.

## 2026-10-07 — Repository research structure formalized

The standalone research tree was organized around the evidence-first layout used by the companion Episode I Racer retail RE project.

## 2026-10-07 — First PSG VIF payload block verified

All 881 sampled first PSG packets begin with the same VIF anchor and decode without unknown command or packet-boundary failure.

## 2026-10-07 — PSG VIF geometry grammar recovered

The first-packet work established MSCNT-terminated geometry batches, contiguous VU destinations and repeated V4/V3/V2 attribute streams.

## 2026-10-08 — PSG payload parsed end-to-end in the canonical sample

**Status:** VERIFIED sample serialization

All 881 PSGs from POD01, TA and TB are now consumed through the render header, LOD groups, 1,216 material blocks, VIF packets and optional multi-object remap tail.

No unexplained payload bytes remain in this sample.

## 2026-10-08 — Position/object encoding and ordinary mesh topology recovered

**Status:** VERIFIED sample behavior

Signed V4-16 and V4-32 position data decode as `origin + raw * position_scale`.

Position W encodes hierarchy object ownership as `abs(W)/16 - 1`.

Negative W pairs restart/setup ordinary triangle strips and positive W records emit triangles with alternating winding. The rule has zero structural warnings across 877 ordinary PSGs.

The four CableShadow resources are retained as an explicit special case.

## 2026-10-08 — Independent mesh and collision-bounds validation

A private OBJ reconstruction from POD01 geometry loaded successfully in an independent mesh library.

Six POD01 PSG components were cross-checked against corresponding type-0 COL resources. Reconstructed PSG bounds, fixed PSG bounds and COL bounds agree within quantization/floating-point precision.

Retail-derived OBJ data remains outside Git.

Evidence:
- `analysis/2026-10-08-psg-mesh-reconstruction.md`
- `records/2026-10-08-psg-render-payload.md`
- `formats/PSG.md`
- `raw/2026-10-08-psg-render-summary.txt`
