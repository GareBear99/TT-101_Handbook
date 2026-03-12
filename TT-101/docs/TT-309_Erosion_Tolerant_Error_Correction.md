# TT-309 — Erosion-Tolerant Error Correction

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


Erosion is the deep-time failure mode. Standard QR error correction is good,
but for slates we design for **chunk loss** and **edge damage**.

## Multi-Scale Redundancy
- In-block error correction (within each tile)
- Cross-block parity (RAID-like reconstruction)
- Cross-slate duplication (multiple slates contain overlapping chunks)

## Practical Guidance
- Prefer lower density modules (larger squares) to survive abrasion
- Use thick borders and alignment markers
- Encode block IDs + hashes in multiple positions

## Verification
Each block contains:
- Block ID
- Payload length
- SHA-256 hash (or simpler checksum ladder also shown)
- Parity group ID

This enables reconstruction even with partial corruption.


## Concept Summary

Write a plain-language summary of this segment.


## Purpose

State why this segment exists in the overall continuity notebook.


## How This Fits the Continuity Plan

Explain where this fits in the training → artifact → verification → journal chain.


## Notebook Entry

- Date:
- What you did (verifiable):
- Evidence (hash/file/photo):


## Next Segment

- Next: [TT-310](./TT-310_Slate_RAID_Block_Format.md)
