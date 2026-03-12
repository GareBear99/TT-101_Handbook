TIMESTAMP_UTC: 2026-03-03T10:08:31.104342+00:00
VERSION: v1.0
STATUS: CANON

**Prev**: [TT-401](./TT-401.md)  
**Next**: [TT-501](./TT-501.md)

---

## Thesis

This segment (TT-410) formalizes a component of the TT-101 continuity model and contributes to the overall deterministic, fail-closed architecture.

## Concept Summary

- Defines scope and constraints within the canon framework
- Locks terminology for downstream bands
- Contributes to continuity preservation logic
- Aligns with fail-closed verification doctrine

## Operational Implications

- Must be interpreted within model-agnostic boundaries
- Reinforces deterministic validation discipline
- Supports survivability-first strategy

## Prerequisites / Next

Refer to adjacent segments in numerical order for escalation continuity.

# TT-410 — Distributed Signing & Verification Policy (v1)


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
