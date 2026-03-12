# TT-367 Archive Journal & Continuity Token

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


This segment turns the handbook into a **living archive journal**: each applicable segment can produce a short, structured “journal line” you can record **now**, and later export as an immutable evidence bundle.

This is not a claim that time travel exists. It is a **continuity-friendly record format** that remains meaningful even if nothing else happens.

## What to record now (meaningful + possible)

Record only things you can verify in the present:

- **Who/where/when** (UTC timestamp, rough location, device context)
- **What you observed** (plain language, no speculation required)
- **What artifact you produced** (hashes, file names, printed/etched slates, photos)
- **What test you ran** (procedure + result)
- **What changed** (repo version, manifest hash, release ID)

Avoid:
- “Proof” claims
- coercive “future must respond” language
- personal sensitive data

## Journal Entry Format (canonical)

Each entry is a single JSON object:

- `id` (stable entry id)
- `t_utc` (ISO 8601)
- `segment` (e.g., `TT-366`)
- `title`
- `content` (short text)
- `evidence` (optional list of hashes, filenames, photos)
- `prev_token` (optional)
- `token` (computed)

## Continuity Token (hash chain)

A **continuity token** is a deterministic SHA-256 hash computed over:

1) the previous token (or a genesis seed)
2) the normalized entry payload

This produces a chain where **any edit changes all downstream tokens**.

Genesis seed (recommended):
- `TT32|2026-03-05|GENESIS`

See TT-368 for the exact normalization + hashing rules.

## Practical usage

- Use TT-365 / TT-366 games as “decoder practice”
- When you solve them, the handbook prompts you to add a journal line
- The Journal page lets you export JSON + a token chain summary



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

- Next: [TT-368](./TT-368_Continuity_Token_Spec.md)
