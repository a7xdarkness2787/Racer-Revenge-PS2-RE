# Reverse-Engineering Update Protocol

This document defines how meaningful new developments in **Racer-Revenge-PS2-RE** must be recorded.

A future researcher should be able to reproduce what was learned without the original chat history.

## Mandatory same-cycle update rule

Whenever a meaningful reverse-engineering development occurs, document it during the same work cycle.

This includes a newly identified function/global/structure/flag/address, corrected function boundary, new format field/invariant/parser, corpus-wide result, failed experiment that changes direction, invalidated hypothesis, runtime behavior, new tool limitation, or new canonical input identity.

## Where information belongs

- `STATUS.md` — current high-level verified state
- `CURRENT_WORK.md` — active handoff
- `RESEARCH_INDEX.md` — strongest evidence path per subsystem
- `DEVELOPMENT_LOG.md` — concise chronological milestone index
- `records/` — chronological investigations, corrections and dead ends
- `analysis/` — deeper technical investigations not yet stable
- `formats/` — stable serialized format specifications
- `structures/` — runtime field/offset/type maps
- `symbols/` and `executable/` — build-specific address ownership
- `behavior/` — portable runtime behavior specifications
- `database/` — machine-readable questions/state
- `reference/` — target identities and generated metadata
- `raw/` — safe text-only raw output
- `scripts/` — parsers and verifiers
- `runtime_oracle/` and `traces/` — dynamic-validation contracts

## Required evidence fields

Detailed records should include applicable identity, question, evidence, commands/tools, raw artifacts, interpretation label, confidence, reproduction instructions, and follow-up.

Use: `VERIFIED`, `OBSERVED`, `INFERRED`, `HYPOTHESIS`, `TODO`, `BLOCKED`, `INVALIDATED`.

## Corrections and failed work

Never silently erase a failed result. Preserve the earlier record or Git history, state the correcting evidence, identify affected conclusions and only then update the stable specification.

The collision BVH volume correction is the current example: ordinary AABB volume appeared correct on a small sample; degenerate boxes disproved it; full-corpus testing established the 0.005 half-extent clamp.

## Address-sensitive work

Addresses are specific to the canonical `SLUS_202.68` build unless independently correlated. Record target hash, address/range, evidence anchor, callers/callees where known, relevant strings/constants, structure offsets, status, confidence and open questions.

## Format work

Keep these separate:

- bytes proven by complete parsing;
- executable-side agreement;
- semantic interpretation;
- runtime behavior.

A field should not receive a semantic name solely because one sample looks plausible.

## Runtime work

PCSX2 experiments should record emulator/version, track, pod, initial state, input sequence, duration/frame definition, addresses watched, outputs, repeatability and first divergence/trigger.

## Proprietary payload policy

Never commit disc images, `SLUS_202.68`, IRX/IMG binaries, extracted RES/PSG/PSM/PST/COL/PHY/SPL payloads, or retail audio/movie content.

## Current-state synchronization

When a finding changes project direction, update the stable subsystem document, a dated record, `DEVELOPMENT_LOG.md`, and any affected `STATUS.md`, `CURRENT_WORK.md`, `RESEARCH_INDEX.md`, or `database/questions-current.json`.
