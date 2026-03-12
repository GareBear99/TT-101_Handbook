# TT-320 — Optical Slate Materials Testing Plan (v1)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


Purpose: Convert TT-307..314 from “spec” to “validated physical protocol”.

## Test Matrix
Materials:
- stainless steel (deep etch)
- titanium (deep etch)
- granite/basalt (laser + mechanical engraving)
- ceramic tile (glaze vs deep cut)
- acrylic (control / not for deep time)

Variables:
- module size (e.g., 1mm, 2mm, 4mm)
- engraving depth (shallow/medium/deep)
- contrast method (cut depth only vs fill)

## Required Tests
1) **Legibility** at:
- naked eye @ 0.5m
- magnifier @ 10×
- phone camera @ 1× / 3×

2) **Abrasion**
- sandpaper cycles
- grit rub cycles
- brush cycles

3) **Moisture / Freeze-Thaw** (if relevant to storage)
- humidity exposure
- freeze-thaw cycles (limited)

4) **Reconstruction**
- manual transcription of a block
- byte decode
- hash verification

## Acceptance Criteria
- TT-314 must decode after abrasion test within defined tolerance
- Alignment markers remain usable
- Metadata remains readable

## Output Artifact
A short “Test Report” appended to CANON_LOG with:
- photos
- measured params
- pass/fail


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

- Next: [TT-321](./TT-321_Incident_Response_and_Freeze_Template.md)
