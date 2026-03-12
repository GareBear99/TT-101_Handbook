# TT-327 — Distributed Signing & Verification Policy (v1)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


This tier upgrades canon integrity from “hash-only” to “hash + signatures”.

## Why
Hashes detect corruption.
Signatures detect impersonation (malicious forks claiming to be official).

## Minimal Policy (v1)
- Every release (vX.Y) must publish:
  1) manifest hash
  2) signed statement of that hash (by multiple stewards)

## Signing Artifact
Create a file:
- `release/RELEASE_vX.Y.txt` containing:
  - version
  - UTC timestamp
  - SHA-256 of `manifest/hashes.txt`
  - short description
Then sign it using:
- PGP / GPG signatures (preferred)
- or multiple independent signing methods

## Verification Rule
A mirror is “canonical” if:
- `make validate` passes
- manifest hash matches the signed release statement
- at least threshold signatures are present (policy-defined)

## Threshold Guidance
- v1: 2-of-N signatures required
- v2+: increase threshold for higher-stakes deployments

## Offline Verification
All verification must be possible without internet:
- printed release statement
- printed public keys / fingerprints
- manual hash verification

## Note
This repo ships policy, not keys.
Keys are steward-managed and must be distributed physically (paper/etched) in the substrate tier.


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

- Next: [TT-328](./TT-328_Optical_Slate_Certification_Standard.md)
