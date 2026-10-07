# Track spline / graph format (.spl)

Status: **OBSERVED / partially VERIFIED** for the North American retail build.

The track `.spl` resources are ASCII INI-style graph descriptions embedded in track `.RES` containers.

## Retail corpus

The extracted retail track set contains **26 `.spl` files** across 13 track containers. Every file parsed successfully with the current structural checker.

Across those 26 files:

- 4,999 declared nodes
- 4,999 matching `[NodeN]` sections
- 5,108 directed edges
- 103 nodes with more than one outgoing edge
- node counts range from 88 to 293

The graph is therefore not merely a visual spline. It explicitly carries routing, AI and race-control metadata.

## Top-level section

Observed `[Track]` keys include:

```ini
[Track]
NumNodes=...
TrackWidth=...
```

The executable parser also contains keys for `DefaultReverb`, `StartNode`, and `NumShortcuts`; those keys are optional in the 26 retail spline resources currently inspected.

## Node sections

Nodes are numbered `Node0` through `Node(N-1)`.

Common keys:

```ini
[NodeN]
Position=x,y,z
LeftTrackWidth=...
RightTrackWidth=...
SpeedLimit=...
DistanceToFinish=...
BranchID=...
NumNextNodes=...
Next0=...
Next1=...
...
```

Observed optional keys:

- `NodeHeight`
- `NodeBlocked`
- `BoostScale`
- `NodeReverb`
- `NoCombatZone`
- `SkipPlayerTest`
- `DriveFullSpeed`
- `ShortestBranch`
- `SecretBranch`
- `Pretty`
- `Ugly`
- `ProgressNode`

The current 26-file corpus uses these optional markers with the following counts:

| Marker | Nodes carrying it |
| --- | ---: |
| `SkipPlayerTest` | 442 |
| `SecretBranch` | 214 |
| `NodeHeight` | 181 |
| `NoCombatZone` | 86 |
| `ProgressNode` | 81 |
| `Ugly` | 39 |
| `DriveFullSpeed` | 21 |
| `NodeBlocked` | 15 |
| `Pretty` | 15 |

`ShortestBranch`, `BoostScale`, and `NodeReverb` are recognized by executable code even when absent from this retail spline sample.

## Executable parser

The routine at `0x002a1260..0x002a1d70` is strongly identified as the current `TunnelTrack` spline loader. It references all of the keys above and the diagnostic source string `TunnelTrack.cpp`.

The routine allocates each runtime node with a **0x80-byte stride**.

Current object-level mapping:

| Track object offset | Meaning |
| --- | --- |
| `+0x30` | node-array pointer |
| `+0x34` | node count |
| `+0x38` | track width |
| `+0x3c` | computed track-distance value |
| `+0x40` | shortcut count |
| `+0x44` | shortcut table pointer |
| `+0x48` | progress-node count |
| `+0x4c...` | progress-node indices |
| `+0x74` | parsed start-node index |

Current node mapping within each 0x80-byte record:

| Node offset | Meaning |
| --- | --- |
| `+0x50` | node height |
| `+0x54` | left width after adding half the top-level track width |
| `+0x58` | right width after adding half the top-level track width |
| `+0x5c` | speed limit |
| `+0x60` | distance to finish |
| `+0x64` | boost scale as float; defaults to 1.0 when absent |
| `+0x68` | branch ID |
| `+0x6c` | pointer to next-node index array |
| `+0x70` | number of outgoing nodes |
| `+0x74` | node reverb value |
| `+0x79` | packed node flags |

The position vector is parsed earlier in each node record, but the R5900 vector store used by this build is not named here until checked with an Emotion Engine-aware disassembler.

## Packed node flags

The parser folds eight optional boolean-like node keys into the byte at node offset `+0x79`:

| Bit | Key |
| ---: | --- |
| `0x01` | `NodeBlocked` |
| `0x02` | `NoCombatZone` |
| `0x04` | `ShortestBranch` |
| `0x08` | `SkipPlayerTest` |
| `0x10` | `DriveFullSpeed` |
| `0x20` | `SecretBranch` |
| `0x40` | `Pretty` |
| `0x80` | `Ugly` |

This bit assignment is directly visible in the masks used at `0x002a165c..0x002a18bc`.

## Progress nodes

When `ProgressNode` is present, the loader records the node index in a track-level list. A diagnostic in the same routine states that no more than 10 progress nodes are allowed.

The parser also writes floating-point `10000.0` to the node-height slot for a progress node before recording the index. The gameplay meaning of that forced height value remains open.

## Edges and shortcuts

`NumNextNodes` controls an allocated integer array referenced from node `+0x6c`; `Next%d` fills the entries.

If `NumNextNodes` is absent, the loader creates a single implicit edge to the next sequential node, wrapping the last node back to zero.

Optional `[ShortcutN]` sections are supported by the executable. Each runtime shortcut entry is 8 bytes and is populated from:

- `PlayerTestNode`
- `AIBlockNode`

No `ShortcutN` sections were present in the 26 retail spline resources examined so far.

Use `scripts/spl_inspect.py` to validate and summarize user-supplied spline files.
