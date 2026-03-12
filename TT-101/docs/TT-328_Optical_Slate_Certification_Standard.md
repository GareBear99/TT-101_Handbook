# TT-328 — Optical Slate Certification Standard (v1.0)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


This document defines the **non-negotiable engineering thresholds**
required for an optical slate to be considered CERTIFIED.

No hedge language. No approximation.

---

## 1. Substrate (Approved Materials)

One of:
- 316 stainless steel (deep engraving)
- Granite or basalt (mechanical or laser engraving)
- Fired ceramic tile (deep cut)

Surface coloration-only marks are NOT permitted.

---

## 2. Geometric Requirements

### Module Size
- MINIMUM: 2.0 mm
- RECOMMENDED: 4.0 mm

### Engraving Depth
- Stone: ≥ 0.5 mm
- Metal: ≥ 0.2 mm

Finder patterns must be oversized and engraved at same depth.

---

## 3. Metadata Requirements

Each slate must include engraved text:
- FORMAT ID (e.g., TT-SLATE-BLOCK v1)
- BLOCK ID
- SHA-256 prefix (minimum 16 hex chars)
- Version reference (e.g., TT-314)

Human-readable, not encoded only inside QR.

---

## 4. Acceptance Test (Mandatory)

The slate passes certification ONLY IF:

1. It decodes successfully via:
   - phone camera
   - manual grid transcription fallback
2. SHA-256 hash matches canonical manifest entry
3. It remains decodable after:
   - 20 cycles moderate abrasion (sandpaper or equivalent)
4. Finder patterns remain visually distinguishable

If any condition fails → NOT CERTIFIED.

---

## 5. Certification Record

When a slate passes:

- Add certification entry to CANON_LOG
- Include:
  - substrate
  - module size
  - depth
  - date (UTC)
  - verifier identity (optional but recommended)
  - photo hash (if available)

---

## 6. Deep-Time Doctrine

A slate that meets TT-328 is considered
operationally reliable for long-term passive survival
under typical environmental entropy.


## Concept Summary

Write a plain-language summary of this segment.


## Purpose

State why this segment exists in the overall continuity notebook.


## How This Fits the Continuity Plan

Explain where this fits in the training → artifact → verification → journal chain.


## Verification

- What would count as “worked” for this segment:
- What artifact/log proves it:


## Notebook Entry

- Date:
- What you did (verifiable):
- Evidence (hash/file/photo):


## Next Segment

- Next: End of canon index.
