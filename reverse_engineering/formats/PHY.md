# Pod physics configuration (.phy)

Status: **OBSERVED / partially VERIFIED** for the North American retail build.

The pod physics resources are plain-text INI-style configuration files embedded in `.RES` containers. The retail corpus contains 23 logical pod physics files.

## Corpus shape

All 23 pod physics files contain the same core configuration families:

- `Pod Setup`
- `Wreckage`
- `Physical Properties`
- `Repulsor`
- `Roll Control`
- `Engine`
- `Engine Aerodynamics`
- `Pod Animation`
- `Collisions`
- `Joystick`
- `CameraInfo`
- `DamageRepair`
- `Pod Audio`
- `BaseAbilities`
- `MaxAbilities`
- `Tuning`

They also contain component sections for `chariot`, `englt1`, and `engrt1`.

`POD02` is the structural outlier in the current corpus: its `Pod Setup` also names `BottomLeftEngine` and `BottomRightEngine`, its wreckage list extends through `Part5`, and it has `englt2` / `engrt2` component sections.

## Important data families

The files expose the game's authored vehicle parameters directly. Examples include:

### Engine / upgrade values

- `MaxThrustA/B/C`
- `TheoreticalTopSpeedA/B/C`
- `MinMaxThrust` / `MaxMaxThrust`
- `MinTheoreticalTopSpeed` / `MaxTheoreticalTopSpeed`
- `BoostThrust`
- `RepairThrust`
- `BoostSpeed`
- `ActualTopSpeed`
- `RampUpFilter` / `RampDownFilter`

### Aerodynamics / steering

- lift, drag and pitch-moment coefficients
- side-slip, rudder, roll-rate and yaw-rate terms
- spoiler drag / side-force / yaw-moment terms
- powerslide thrust and steering terms
- inverted-flight coefficients

### Pod animation / physical response

- impact, thrust, lift and drag forces
- engine and binder spring/damping values
- yaw, pitch and roll torques
- cable forces
- chariot impulse and velocity response
- turbulence and orientation scales

### Collision / control

- restitution
- friction
- impulse response
- explosive-wreck and reset speeds
- joystick steering speed/scale pairs and axis rate limits

### Damage / repair

- `DefenseA/B/C`
- `BaseRepairAmountA/B/C`
- `BaseCoolingTimeA/B/C`
- min/max ranges for the same abilities

## Retail tuning observations

The current 23-file corpus consistently contains `UseValues=1`, with `UseAValues`, `UseBValues`, and `UseCValues` set to zero. The A/B/C authored values are still present and are consumed by executable code; they should not be treated as dead fields.

Examples from the retail data:

| Pod | MaxThrust A/B/C | TopSpeed A/B/C | Defense A/B/C |
| --- | --- | --- | --- |
| POD01 | 8475 / 8475 / 8475 | 900 / 900 / 900 | 0.8 / 0.8 / 0.8 |
| POD02 | 5325 / 7162.5 / 9000 | 540 / 680 / 820 | 0.1 / 0.45 / 0.8 |
| POD14 | 9000 / 9000 / 9000 | 900 / 900 / 900 | 0.9 / 0.9 / 0.9 |
| POD26 | 9000 / 9000 / 9000 | 1200 / 1200 / 1200 | 1 / 1 / 1 |

These are authored file values, not yet claims about final in-race units.

## Duplicate physics payloads

The 23 `.phy` resources in `UI/PODPHYS.RES` are byte-identical to the corresponding `.phy` resources inside the individual `PODS/PODxx/PODxx.RES` files.

Result: **23/23 SHA-256 matches**.

## Executable-backed field mapping

A large configuration routine begins at `0x002146c0`. It directly references the pod configuration section/key strings and stores parsed values into the active vehicle object. The nearby string block also contains `PodVehicle.cpp`, so this routine is the current pod-configuration loader candidate.

The following offsets are directly visible in standard MIPS stores and do not depend on decoding R5900-only instructions:

| Key | Runtime offset |
| --- | ---: |
| `EngineMotion` | `+0xab0` |
| `Gravity` | `+0x378` |
| `AirborneGravity` | `+0x37c` |
| `MaxLiftHeight` | `+0x7ec` |
| `ImpactForce` | `+0x9f0` |
| `GroundImpactForce` | `+0x9f4` |
| `SeparationForce` | `+0x9f8` |
| `ThrustForce` | `+0x9fc` |
| `LiftForce` | `+0xa00` |
| `DragForce` | `+0xa04` |
| `EngineSpring` | `+0xa08` |
| `EngineDamping` | `+0xa0c` |
| `BinderSpring` | `+0xa10` |
| `YawTorque` | `+0xa14` |
| `PowerslideYawTorque` | `+0xa18` |
| `PowerslidePitchTorque` | `+0xa1c` |
| `PitchTorque` | `+0xa20` |
| `RollTorque` | `+0xa24` |
| `EngineTorque` | `+0xa28` |
| `EngineTorqueDamping` | `+0xa2c` |
| `BinderTorque` | `+0xa30` |
| `MinTurbulenceTimeScale` | `+0xa34` |
| `MaxTurbulenceTimeScale` | `+0xa38` |
| `MinChariotTurbulenceTimeScale` | `+0xa3c` |
| `MaxChariotTurbulenceTimeScale` | `+0xa40` |
| `MinTurbulenceScale` | `+0xa44` |
| `MaxTurbulenceScale` | `+0xa48` |
| `MinChariotTurbulenceScale` | `+0xa4c` |
| `MaxChariotTurbulenceScale` | `+0xa50` |
| `MaxTurbulenceSpeed` | `+0xa54` |
| `DamageTurbulenceScale` | `+0xa58` |
| `DamageOrientationTurbulenceScale` | `+0xa5c` |
| `ChariotOrientationScale` | `+0xa60` |
| `OrientationScale` | `+0xa64` |
| `MaxInputScaleSpeed` | `+0xa68` |
| `CableForce` | `+0xa6c` |
| `CableRadiusForce` | `+0xa70` |
| `ChariotVelocityForce` | `+0xa74` |
| `ChariotPowerslideVelocityForce` | `+0xa78` |
| `ChariotVelocityRateForce` | `+0xa7c` |
| `ChariotVelocityDamping` | `+0xa80` |
| `ChariotAngularRateDamping` | `+0xa84` |
| `ChariotMaxYawRate` | `+0xa88` |
| `ChariotMaxYawAngle` | `+0xa8c` |
| `ChariotMaxPowerslideYawAngle` | `+0xa90` |
| `ChariotMaxImpulse` | `+0xa98` |
| `ChariotMaxRepulsorImpulse` | `+0xa9c` |
| `ChariotImpactForce` | `+0xaa0` |
| `ChariotHeadOnImpactForce` | `+0xaa4` |
| `ChariotRepulsorImpactForce` | `+0xaa8` |
| `ChariotLandingImpulseScale` | `+0xaac` |
| `SteerSpeed1` | `+0xb84` |
| `SteerScale1` | `+0xb88` |
| `SteerSpeed2` | `+0xb8c` |
| `SteerScale2` | `+0xb90` |
| `XAxisRateLimit` | `+0xb94` |
| `YAxisRateLimit` | `+0xb98` |
| selected defense | `+0xcf0` |
| selected repair amount | `+0xcf4` |
| selected cooling time | `+0xcf8` |

The A/B/C damage-repair keys each feed the same three runtime slots on different code paths. Later code also references the min/max values and performs floating-point interpolation/clamping. The exact upgrade-selection state feeding those paths is still being mapped.

## Open questions

- exact identity and full size of the vehicle structure
- conversion factors applied to authored units
- selection/interpolation rules for A/B/C upgrade values
- exact runtime use of `BaseAbilities`, `MaxAbilities`, and `Tuning`
- component damage-state structures and break thresholds
- relationship between physics values and AI-only overrides

Use `scripts/phy_inspect.py` for repeatable inspection of user-supplied `.phy` files.
