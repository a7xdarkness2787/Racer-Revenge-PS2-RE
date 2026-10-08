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

A POD01/TA/TB sample established the initial VIF packet grammar and executable VIF anchors.

## 2026-10-08 — PSG position scale and sample strip topology recovered

The sampled payload established position dequantization, hierarchy W tags, material grouping and independent PSG/COL bounds checks.

## 2026-10-08 — VIF UNPACK control bits verified

FLG/USN interpretation was checked against PS2SDK and the sampled packets. V4-8 was established as unsigned source data and material-block bit `0x8` as its presence flag.

## 2026-10-08 — Complete PSG render corpus validated

**Status:** VERIFIED

Detailed parsing was expanded to all 9,917 PSG resources in all 103 RES containers.

Totals:

- 22,175 material/VIF blocks
- 366,935 geometry batches
- 4,869,177 positions
- 3,124,861 reconstructed triangles
- 0 payload parse failures
- 0 unexplained payload bytes

## 2026-10-08 — PSG topology interpretation corrected

Full-corpus animated/cutscene/cable geometry invalidated the earlier same-transform-per-triangle restriction.

Correct interpretation:

- W sign seeds/restarts strips
- W magnitude selects a hierarchy transform per vertex

The corrected rule has zero topology warnings across the complete corpus.

This correction is preserved in the dated research record rather than silently replacing the earlier interpretation.
