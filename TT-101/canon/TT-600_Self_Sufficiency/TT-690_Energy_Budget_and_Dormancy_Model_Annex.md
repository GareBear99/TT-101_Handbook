TIMESTAMP_UTC: 2026-03-03T10:08:31.113077+00:00
VERSION: v1.0
STATUS: CANON

**Prev**: [TT-680](./TT-680.md)  
**Next**: [TT-700](./TT-700.md)

---

## Thesis

This segment (TT-690) formalizes a component of the TT-101 continuity model and contributes to the overall deterministic, fail-closed architecture.

## Concept Summary

- Defines scope and constraints within the canon framework
- Locks terminology for downstream bands
- Contributes to continuity preservation logic
- Aligns with fail-closed verification doctrine

## Operational Implications

- Must be interpreted within model-agnostic boundaries
- Reinforces deterministic validation discipline
- Supports survivability-first strategy

## Prerequisites / Next

Refer to adjacent segments in numerical order for escalation continuity.

# TT-690 — Energy Budget & Dormancy Model Annex (v1.0)


This annex provides a **minimum viable power model** for a continuity outpost.
It explicitly supports **dormant mode** where power is *not required* for knowledge survival (optical slate tier).

## Operating Modes
### Mode 0 — Passive Archive (No Power)
- Optical slates + human-readable metadata only
- Survival depends on materials + placement, not electricity

### Mode 1 — Low-Power Steward (Wake/Verify/Copy)
Typical equipment:
- low-power compute (ARM SBC class)
- camera/scanner
- small motion stage / simple robot arm for handling

### Mode 2 — Fabrication Burst (Maintenance/Replication)
- 3D printer(s) + CNC/laser usage windows
- batch operations only

## Planning Power Budget (Order-of-Magnitude)
| Subsystem | Avg W | Peak W | Notes |
|---|---:|---:|---|
| Compute (SBC + storage) | 10–25 | 30 | duty-cycled |
| Sensors/camera/lighting | 5–15 | 25 | verify only |
| Small robot handling | 0–20 | 150–300 | bursts |
| Laser engraver (small) | 0 | 200–800 | burst only |
| FDM printer | 0 | 120–300 | burst only |
| Environmental control | 0–100 | 500+ | optional |

### Suggested Baseline Targets
- **Mode 1 average:** 20–60 W
- **Mode 2 burst:** 0.5–2.0 kW while active
- **Duty cycle:** 1–5% active, 95–99% dormant

## Storage Example
30-day Mode 1 reserve at 40W:
- 40 W × 24 h/day × 30 = 28,800 Wh ≈ **28.8 kWh**

## Doctrine (Fail-Closed)
- The system must always be **complete in Mode 0**.
- Power-enabled modes only increase redundancy, replication, and verification speed.
