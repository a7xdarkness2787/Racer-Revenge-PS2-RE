# Reverse-engineering status

Baseline date: 2026-10-07  
Last evidence update: 2026-10-07

## Overall

Estimated overall research maturity: **about 16%**

This percentage measures progress toward a documented, reproducible understanding of the North American retail PS2 game. It is not a playable-game percentage and is not a claim that 16% of the machine code has been semantically recovered.

The current increase is driven by three concrete advances: the complete outer `.RES` parser, an address-backed pod physics/configuration map, and an address-backed `TunnelTrack` spline graph map.

| Area | Weight | Current evidence score | Notes |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail image identity and complete extracted manifests are available; full local re-hash remains a separate clean-run gate |
| Executable, platform and object system | 10% | 20% | Resource loader, pod configuration loader and TunnelTrack loader are now address-backed |
| Containers and asset formats | 15% | 30% | 103/103 outer RES files pass; PHY and SPL families are now structurally documented |
| Tracks, world and collision | 15% | 12% | 26 SPL graphs validated and runtime node layout/flags mapped; geometry/collision formats remain open |
| Vehicle physics, boost and damage | 15% | 12% | 23 PHY files parsed; many runtime field offsets mapped; upgrade selection/equations remain open |
| Race logic, AI and progression | 10% | 3% | SPL branch graph and AI/race-control node markers exposed; higher-level behavior still open |
| Renderer, textures and effects | 15% | 0% | PSG/PSM/PST/VU/GS behavior not yet mapped |
| Camera, audio, UI and save behavior | 5% | 8% | Readable CAM/INI/JUK families and inventory evidence; code behavior still mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime capture yet |
| Reproducibility and closure | 3% | 25% | RES, PHY and SPL inspection tooling and dated evidence records are now retained |

Weighted total from this rubric is approximately **15.6%**, rounded to **16%**.

## Latest verified developments

### Resource containers

The retail `.RES` outer format is structurally reproducible across all 103 extracted containers:

- 34,128 logical resource directory records
- 44,861 zlib chunks
- every chunk expands to `0x6000` bytes
- every compressed chunk is followed by `0xff`
- no overlapping resource ranges
- no unexplained trailing bytes

### Pod physics

All 23 retail pod `.phy` configurations parse as INI-style text. The executable routine beginning at `0x002146c0` directly consumes the same section/key names and provides a first runtime field map for gravity, repulsor, pod-animation, steering and damage/repair data.

The consolidated `UI/PODPHYS.RES` copies still match the matching pod-local `.phy` resources 23/23 byte-for-byte.

### Track graphs

All 26 retail `.spl` resources parse successfully:

- 4,999 nodes
- 5,108 directed edges
- 103 branch nodes

The `TunnelTrack` loader at `0x002a1260..0x002a1d70` uses 0x80-byte runtime node records and packs eight authored routing/AI markers into a flags byte at node `+0x79`.

See `formats/RES.md`, `formats/PHY.md`, `formats/SPL.md`, `executable/resource_loader.md`, and `executable/pod_track_loaders.md`.

## Confirmed disc-level dataset counts

- 2,010 `.VAG`
- 136 `.INI`
- 103 `.RES`
- 23 `.CAM`
- 18 `.PST`
- 8 `.IRX`
- 3 `.PSS`
- 3 `.JUK`
- 2 `.LSI`
- 2 `.JUB`

These are disc-level counts. The recovered RES directories expose tens of thousands of additional embedded resources and should not be mixed with the disc-file count.
