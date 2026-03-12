# DARPA Audit Report — v11 (ICS + Deterministic TOC + Validator Hardening)

Generated: 2026-03-02T22:38:46.498250Z

## Additions
- **TT-260 — Iterative Counterjump Steering (ICS)** added under TT-200 Protocol.
  - Reframes “cancellation windows” as **control windows** (control theory), not literal branch hopping.
  - Works across self-consistent, branching, overwrite, or unknown models.

## Landing Surface Integrity
- Added **TOC markers** in `index.html`:
  - `<!-- TOC:BEGIN -->` / `<!-- TOC:END -->`
- Added **tools/build_index.py** to generate the Key Documents TOC deterministically from:
  - canon band folders
  - TT numbering
  - markdown H1 titles

## Validator (No Silent Failures)
- Replaced fragile regex checks with robust rules:
  - Exactly one TOC container
  - TOC link count threshold
  - `build_index.py --check` must pass
  - Manifest excludes release files (no circular hashing)
  - Release manifest hash must match

## Status
- Validation: **VALIDATION OK**
- MANIFEST_SHA256: 896e9a01211af6a14a8b2346317c080c2aa6224a3c874973d8bb4f2816724452
