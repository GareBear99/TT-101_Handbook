TIMESTAMP_UTC: 2026-03-03T10:08:31.102117+00:00
VERSION: v1.0
STATUS: CANON

**Prev**: [TT-350](./TT-350.md)  
**Next**: [TT-370](./TT-370.md)

---

## Thesis

This segment (TT-360) formalizes a component of the TT-101 continuity model and contributes to the overall deterministic, fail-closed architecture.

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

# TT-360 — Optical Slate Block Specification (v1)


This document defines a **testable, etchable** QR-like optical block format for the TT-307 Passive Core.

This is NOT “standard QR.” It is a **self-describing grid** designed for:
- deep engraving
- erosion tolerance
- reconstruction with minimal tools

## 1) Design Targets
- Readable with: **naked eye + magnifier**
- Decodable with: **hand transcription** (worst case)
- Verifiable with: **checksum/hash**
- Reconstructable with: **parity blocks** (Slate RAID; TT-310)

## 2) Coordinate System
- A block is an `N × N` module grid.
- Modules are indexed `(r, c)` with `r=0..N-1`, `c=0..N-1`.
- `(0,0)` is top-left.

## 3) Mandatory Visual Structures
### 3.1 Border Frame
- Outer frame is a **thick border** (2 modules wide recommended).
- Purpose: preserve alignment under edge damage.

### 3.2 Finder Patterns
- Three corner finders (TL/TR/BL), each `7×7` modules:
  - black ring, white ring, black core (classic-style)
- Purpose: orientation + scale.

### 3.3 Timing Track
- A 1-module alternating track between TL→TR and TL→BL.
- Purpose: recover module pitch under distortion.

## 4) Data Region
After reserving:
- border
- finders
- timing track
- metadata strip (see below)

Remaining modules are filled row-major with payload bits.

## 5) Metadata Strip (Human + Encoded)
A reserved strip (e.g., bottom 3 module rows rendered as larger engraved text nearby) must include:

Human-readable text:
- `FORMAT: TT-SLATE-BLOCK v1`
- `BLOCK_ID: ####`
- `PAYLOAD_BYTES: ####`
- `CHECK: SHA256:<first16hex>` (full hash can be stored on slate pages)
- `PARITY_GROUP: #` (optional)

Encoded metadata:
- The same fields encoded in payload header bytes.

## 6) Payload Encoding (v1)
- ASCII/UTF-8 text payload for test artifacts.
- For binary archives: chunked bytes (future v2).
- Bit order: MSB-first per byte.

## 7) Integrity
Minimum:
- SHA-256 of payload bytes (store at least first 16 hex chars on the slate face)
Optional:
- CRC32 for fast manual checking

## 8) Parity (Slate RAID)
For a parity group of `k` data blocks:
- One XOR parity block is computed over equal-length payload bytes.
- Missing one block can be reconstructed.

## 9) Density Profiles
- **LOW**: N=41 (large modules; best for abrasion tolerance)
- **MED**: N=65
- **HIGH**: N=97 (only for protected, stable environments)

## 10) Compliance Rule
A TT-SLATE-BLOCK is not “canon-ready” unless:
- TT-308 decoding ladder exists on same slate set
- A human-readable example decode is included (TT-314)
