# SAFETY_CASE

TIMESTAMP_UTC: 2026-03-03T12:46:36.361905+00:00
VERSION: v1.0
STATUS: CANON

## Claims
C1. Structural completeness (no missing indexed segments).
C2. Navigability (no broken internal links; required handbook pages exist).
C3. Fail-closed enforcement (gates block regressions).
C4. Physics-claim wording boundaries enforced.
C5. Releases are reproducible and verifiable (manifest + pinned release hash + pipeline).

## Evidence
E1. `tools/validate_repo.py` runs semantic, link, orphan, and style gates.
E2. `manifest/hashes.txt` includes SHA-256 for all release files.
E3. `release/RELEASE_v1.0.txt` pins the manifest hash.
E4. CI runs gates on push/PR.
E5. `tools/build_release.py` builds dist artifacts after passing gates.

## Limitations
Linting enforces boundaries and structure; it cannot prove truth of any physical claims.
