# TT-000 — Canon Status

STATUS: FROZEN  
CANON_VERSION: v1.0  
FROZEN_UTC: 2026-03-02T11:23:34.285801Z

## Policy (Fail-Closed)
- No new namespace bands may be added in v1.x.
- No renaming of canonical TT-* files in v1.x.
- Changes in v1.x must be additive and backward-compatible (append-only preferred).
- Any structural change requires a new major version (v2.0).

## What Counts as “Canonical”
- Files under `canon/` and governance files referenced by the validator.
- Integrity is defined by `manifest/hashes.txt` and release statements.

## What This Is
A deterministic deep-time continuity & archival integrity protocol.

Time travel is treated only as an optional compatibility edge-case, not a claim.


## Namespace Bands (v1.0)
- 100 Core
- 200 Protocol
- 300 Artifact
- 400 Integrity
- 500 Governance
- 600 Self-Sufficiency
- 700 Expansion (Optional)
