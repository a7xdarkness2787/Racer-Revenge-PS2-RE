# Contributing to Racer Revenge PS2 RE

This repository is an evidence-first reverse-engineering notebook for the North American PlayStation 2 retail release of **Star Wars: Racer Revenge**.

Useful contributions include independently derived format specifications, function/address mapping, structure and flag identification, parsers/verifiers, corpus validation, safe text-only output, PCSX2 runtime probes, and corrections with explicit provenance.

## Proprietary-data rule

Do not commit original or extracted retail payloads: disc images, `SLUS_202.68`, IRX/IMG modules, RES archives, extracted models/textures/collision/track data, audio or movies.

Tools should accept private fixture paths at runtime and commit only derived metadata/specifications.

## Evidence standard

Substantive claims should identify the target build, address/file offset where relevant, strings/xrefs, serialized offsets/strides, runtime offsets, corpus pass/fail counts, parser/verifier, evidence status and open follow-up.

Use the evidence labels in `UPDATE_PROTOCOL.md`.

## Corrections

Do not silently rewrite history. Preserve prior evidence and add the correction.

## R5900 caution

Generic MIPS disassemblers may decode Emotion Engine instructions incorrectly or leave them unknown. Do not assign semantics to R5900-only instructions without an EE-aware check.

## Repository organization

Put material in the narrowest appropriate directory. Avoid one-off root documents when the subject belongs under an existing category.
