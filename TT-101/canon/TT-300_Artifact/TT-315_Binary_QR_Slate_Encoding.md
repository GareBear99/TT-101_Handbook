# TT-315 Binary QR Slate Encoding (Smallest-Size Storage)

TIMESTAMP_UTC: 2026-03-05T00:00:00Z  
VERSION: v1.0  
STATUS: draft-canon  

**Purpose:** Define a **binary-first** encoding pathway for QR-code “slates” (laser‑etched or printed) where the payload is stored in **raw bytes** for maximum density and minimal file size.

This segment extends the Optical Slate Passive Core workstream (TT-301…TT-380).

---

## Concept summary

A QR slate may store **bytes directly** (QR Byte mode) rather than text to maximize payload density. The slate includes a minimal human-readable wrapper and a binary envelope (`TTB1`) so that reconstruction is deterministic even if tooling changes.

---

## Operational implications

- Enables dense storage for:
  - segment archives
  - compressed bundles
  - tool-seed decoders
- Requires robust chunking and reconstruction rules.
- Must include integrity verification (CRC32 + SHA-256).

---

## Specification

See the companion doc: `docs/TT-315_Binary_QR_Slate_Encoding.md` for the full envelope and block layout.

**Canonical envelope name:** `TTB1`  
**Canonical integrity:** `SHA-256(payload_bytes)` + optional CRC32

---


## Related segments (next)
- **TT-316** QR Slate Redundancy & Parity
- **TT-317** QR Slate Tooling (Pack/Unpack + Verify)
- **TT-318** Bootstrap Decoder Slate

## Prerequisites / next

- Ensure TT-310 slate RAID format and TT-309 erosion-tolerant ECC assumptions are aligned.
- Add TT-315A parity blocks and TT-315C tooling-seed slate.
