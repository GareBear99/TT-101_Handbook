# DARPA Audit Report — v1.0 Engineering Hardening (v7)

Generated: 2026-03-02T21:33:04.816692Z

## Summary
- Canon bands present: TT-100_Core, TT-200_Protocol, TT-300_Artifact, TT-400_Integrity, TT-500_Governance, TT-600_Self_Sufficiency, TT-700_Expansion, TT-900_Meta
- Missing bands: []
- Missing required annex files: []
- Manifest includes release files: False
- Manifest hash matches release statement (pre-fix): True
- Landing page missing link targets (pre-fix): []
- Landing page missing link targets (post-fix): []
- Validator result: VALIDATION OK

## Fixes Applied
1. Rebuilt `index.html` **Key documents** navigation with strict numeric band grouping:
   - TT-100, 200, 300, 400, 500, 600, 700, 900
   - `Release` and `Manifest` are now only listed under **TT-900 Meta**
2. Regenerated `manifest/hashes.txt` (release excluded to avoid circular hashing)
3. Updated `release/RELEASE_v1.0.txt` with new `MANIFEST_SHA256`
4. Ran `tools/validate_repo.py` — PASS

## Current MANIFEST_SHA256
d64a1ed0492b0921d884b50840ca10cd684db347566db125f345d5e5efc1dc0b
