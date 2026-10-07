# Reverse-engineering status

Baseline date: 2026-10-07  
Last evidence update: 2026-10-07

## Overall

Estimated overall research maturity: **about 11%**

This percentage measures progress toward a documented, reproducible understanding of the North American retail PS2 game. It is not a playable-game percentage and is not a claim that 11% of the machine code has been semantically recovered.

The increase from the initial baseline is driven mainly by a complete structural pass over the outer `.RES` corpus and an address-backed resource-loader anchor in `SLUS_202.68`.

| Area | Weight | Current evidence score | Notes |
| --- | ---: | ---: | --- |
| Input identity and corpus inventory | 5% | 80% | Retail image identity and complete extracted manifests are available; full local re-hash remains a separate clean-run gate |
| Executable, platform and object system | 10% | 15% | ELF layout fixed; `LoadResourceFile` routine strongly anchored at `0x0012cea0..0x0012dca0`; broader object/runtime map remains open |
| Containers and asset formats | 15% | 25% | 103/103 outer RES files pass the recovered v3 parser; embedded formats are mostly not decoded yet |
| Tracks, world and collision | 15% | 3% | TA/TB internal resource inventories are now reconstructable; geometry/collision semantics remain open |
| Vehicle physics, boost and damage | 15% | 4% | 23 physics resources reconstruct; consolidated and pod-local `.phy` copies match 23/23; equations and runtime state remain open |
| Race logic, AI and progression | 10% | 1% | Names and resource evidence only |
| Renderer, textures and effects | 15% | 0% | Not yet mapped to VIF/VU/GS behavior |
| Camera, audio, UI and save behavior | 5% | 8% | Readable CAM/INI/JUK families and inventory evidence; code behavior still mostly open |
| Differential runtime validation | 7% | 0% | No retained PCSX2 runtime capture yet |
| Reproducibility and closure | 3% | 15% | RES parser and dated evidence record added; clean end-to-end verifier run still open |

Weighted total from this rubric is approximately **10.9%**, rounded to **11%**.

## Latest verified development

The retail `.RES` outer format is now structurally reproducible across all 103 extracted containers:

- 34,128 logical resource directory records
- 44,861 zlib chunks
- every chunk expands to `0x6000` bytes
- every compressed chunk is followed by `0xff`
- every logical resource offset is on a `0x6000` virtual boundary
- no overlapping resource ranges
- no unexplained trailing bytes

See `formats/RES.md`, `executable/resource_loader.md` and `records/2026-10-07-res-container.md`.

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
