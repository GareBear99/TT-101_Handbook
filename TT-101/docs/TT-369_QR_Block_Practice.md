# TT-369 — QR Block Practice (Decode → Verify)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


TIMESTAMP_UTC: 2026-03-05T00:00:00Z  
VERSION: v1.0  
STATUS: draft-canon  

**Purpose:** Provide a lightweight, offline training + verification surface for **TT-315 QR slates**.

This segment exists to let you verify **one scanned QR block** at a time:

- Load `slate.json` (from `tools/qr_slate_pack.py`).
- Paste one block payload (HEX or base64).
- Compute `SHA-256(block_bytes)`.
- Compare to `slate.json -> blocks.sha256[index]`.

## Concept summary

A slate system is only as good as its recovery workflow. TT-369 ensures you can:

- detect scanner corruption immediately
- build confidence in your capture pipeline
- generate **journal lines** that link artifact work to the continuity token (TT-367)

## Operational implications

- Requires `slate.json` to contain per-block SHA-256 hashes.
- Supports “evidence-first” journaling (no claims, just verification results).

## Related segments

- TT-315 Binary QR Slate Encoding
- TT-316 Parity / redundancy
- TT-317 Tooling
- TT-367 Archive Journal + Continuity Token


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

- Next: [TT-370](./TT-370_Archive_Journal_Prompts.md)
