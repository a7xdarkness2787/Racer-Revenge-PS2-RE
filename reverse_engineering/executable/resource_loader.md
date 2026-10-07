# Resource loader anchors

Build: North American retail `SLUS_202.68`  
Executable SHA-256: `c1f1b63eb422b624189e68eb0140b318455e341d73182703017298fea6ce6c30`

Status: **OBSERVED**, with the main routine identity strongly anchored by its own diagnostic strings.

## LoadResourceFile candidate

A large routine at `0x0012cea0..0x0012dca0` contains direct references to several `LoadResourceFile` diagnostics from `DataAccess.cpp`. This makes it the current primary resource-file loader candidate rather than a name assigned only from call shape.

Observed references include:

| Code address | Referenced diagnostic / evidence |
| --- | --- |
| `0x0012d110` | `LoadResourceFile: realloc of DeviceList failed` |
| `0x0012d1d0` | `LoadResourceFile: NextAvailableDevice >= NumberOfDevicesInList` |
| `0x0012d330` | `Could not load resource file (%s) - read error.` |
| `0x0012d370` | `Could not load resource file (%s) - wrong file version.` |
| `0x0012d56c` | `LoadResourceFile: numberOfItemsToAdd == 0` |
| `0x0012db50` | `LoadResourceFile: currentDevice->fileName != NULL` |
| `0x0012dbb8` | `LoadResourceFile: currentDevice->flagData doesn't include DATAACCESS_FLAG_AVAILABLE` |

The function opens the named resource using the nearby `rb` mode string.

## Format behavior visible in code

The static routine agrees with the independent corpus parser on an important constant: `0x6000` bytes.

- `0x0012d5cc`: compares a current amount against `0x6000`.
- `0x0012d740`: computes the next boundary by adding `0x6000`.

The loader also checks the resource version near `0x0012d33c`. The observed retail files use version 3, while the routine contains a distinct path for version 2.

This evidence connects the `.RES` byte layout to executable behavior. It does not yet name all helper calls or explain the meanings of the constant header words at `+0x08` and `+0x0c`.

## Analysis caution

The current disassembly was checked with LLVM's generic MIPS backend. It decodes standard MIPS instructions but reports some R5900-specific instructions as unknown or misleading generic opcodes. Those instructions are not being assigned semantics until an Emotion Engine-aware analysis pass is retained.
