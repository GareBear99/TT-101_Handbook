# TT-321 — Incident Response & Canon Freeze Template

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


When integrity is uncertain, the system must **fail closed**.

## Trigger Conditions
- Validator fails (`make validate` non-zero)
- Manifest mismatch across mirrors
- Suspected key compromise
- Conflicting canon branches
- Unauthorized edits detected

## Immediate Actions (0–24h)
1) Freeze canon updates
2) Snapshot current manifests from all mirrors
3) Publish incident note referencing the last known-good manifest hash
4) Quarantine suspect branch/mirror

## Investigation
- Identify changed files
- Verify hashes
- Determine who/what changed and why

## Recovery
- Roll forward using append-only corrections
- Rotate keys if needed
- Re-enable updates only after validation passes

## Postmortem (Required)
- timeline
- root cause
- mitigation applied
- new controls


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

- Next: [TT-324](./TT-324_Self_Fabrication_and_Self_Sufficiency_Doctrine.md)
