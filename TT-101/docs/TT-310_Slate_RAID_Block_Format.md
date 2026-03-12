# TT-310 — Slate RAID Block Format (Physical Dataset Assembly)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


Treat slates like a physical RAID array.

## Block Anatomy
- Alignment frame (thick border)
- Finder patterns (corners)
- Version tag
- Block ID (human-readable + encoded)
- Payload bits
- Embedded checksum/hash
- Parity metadata

## Reconstruction Rules
- Blocks are ordered by Block ID
- Missing blocks can be reconstructed if parity blocks exist
- Multiple identical copies across sites increase survival probability

## Why RAID-on-Stone
Because “some blocks will be lost.”
Design for graceful degradation, not perfection.


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

- Next: [TT-311](./TT-311_Materials_and_Engraving_Depth.md)
