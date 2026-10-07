# Analysis Environment

## Current static-analysis tools

The retained research records currently rely on:

- Python 3 for binary parsing, corpus validation, hashing and consistency checks;
- GNU Binutils/`readelf` for ELF metadata;
- LLVM `llvm-objdump` for generic MIPS address/disassembly checks;
- independent byte/corpus validation to confirm serialized structures.

## Emotion Engine limitation

The PlayStation 2 Emotion Engine is not ordinary generic MIPS.

LLVM's generic MIPS backend does not correctly name every R5900-specific instruction and can emit unknown or misleading decodes for vector/EE-specific operations.

Repository rule: do not assign semantics to an R5900-only instruction solely from generic LLVM output.

Claims promoted to stable documentation should rely on evidence that is unambiguous from standard loads/stores, constants, control flow, string references, allocation arithmetic, serialized data, runtime evidence, or full-corpus validation.

## Preferred additions

Future analysis should retain an Emotion Engine-aware disassembly export and record tool/version, target/load settings, executable SHA-256, function/address range, raw output path when safe, and manual corrections.
