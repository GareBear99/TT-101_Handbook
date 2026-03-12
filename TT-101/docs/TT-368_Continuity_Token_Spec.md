# TT-368 Continuity Token Spec

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


This defines the exact token computation so that different implementations can reproduce identical tokens.

## Inputs

- `prev_token` (hex SHA-256) OR `GENESIS`
- `entry` (JSON object)

## Normalization Rules

1) Create a new object containing only these fields, in this order:

- `t_utc`
- `segment`
- `title`
- `content`
- `evidence` (array of strings; optional; if absent use `[]`)

2) Normalize:
- Trim whitespace on strings
- Convert CRLF → LF
- `t_utc` must be ISO 8601 (e.g., `2026-03-05T00:00:00Z`)

3) Serialize as canonical JSON:
- UTF-8
- no extra whitespace
- keys strictly in the specified order

## Token computation

Let `payload_bytes = UTF8(prev_token + "\n" + canonical_json)`.

Token = `SHA256(payload_bytes)` as lowercase hex.

## Minimal verification bundle

A journal export is “complete” if it includes:

- `genesis`
- `entries[]`
- `final_token`
- `manifest_sha256` (optional but strongly recommended)



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

- Next: [TT-369](./TT-369_QR_Block_Practice.md)
