# SECURITY_MODEL

TIMESTAMP_UTC: 2026-03-03T12:46:36.361386+00:00
VERSION: v1.0
STATUS: CANON

## Scope
This repository is a fail-closed canonical handbook. Primary goal: prevent silent drift or undetected tampering.

## Threats
- Unauthorized edits to canon segments
- Accidental regressions (broken links, missing segments, drift)
- Release substitution (zip mismatch vs manifest)
- Narrative drift into physics-claim language

## Trust Boundaries
- `manifest/hashes.txt` is the file integrity ledger (SHA-256).
- `release/RELEASE_v1.0.txt` pins the manifest hash.
- Validation gates run fail-closed via `tools/validate_repo.py` and CI.

## Mitigations
- CI enforcement (`.github/workflows/ci.yml`)
- Deterministic release builder (`tools/build_release.py`)
- Semantic wording boundaries (`tools/semantic_lint.py`)
- Link/orphan/style gates

## Residual Risk
Meaning can still drift while passing lints; mitigate with human review and (optional) signed releases.
