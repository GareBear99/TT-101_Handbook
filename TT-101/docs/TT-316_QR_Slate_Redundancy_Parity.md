# TT-316 — QR Slate Redundancy & Parity (Missing-Chunk Survival)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---

STATUS: Stable
VERSION: 1.0

## Concept Summary
If some QR blocks are lost/damaged, parity blocks let you reconstruct missing data chunks.

## Purpose
Increase recoverability of etched/slate QR archives under erosion, loss, and scanning failure.

## How This Fits the Continuity Plan
Training (TT-364/366/365) → Artifact generation (TT-315) → **Redundancy (TT-316)** → Tooling (TT-317) → Verification (TT-369) → Journal (TT-367) → Token (TT-368).

## Explanation
### Redundancy strategies
- **Group XOR parity**: for each group of N data blocks, store 1 parity block = XOR of all bytes.
- **Global parity**: optional additional parity across all blocks (weak, but cheap).

### What XOR parity can recover
- Recovers **exactly one missing block per parity group** (if others present).
- If 2+ blocks in a group are missing, XOR parity alone cannot fully recover.

### Recommended settings
- Group size: **8–16** data blocks per parity block (balance recovery vs overhead).
- QR ECC: use high ECC when etching small or scanning in harsh conditions.

## Verification
- Delete one data block in a group and confirm `qr_slate_unpack.py` reconstructs it using parity.
- Confirm recovered payload SHA-256 matches `slate.json`.

## Notebook Entry
- Date:
- Slate ID / directory:
- Chunk bytes:
- Parity groups:
- Recovery test performed:
- Result (pass/fail) + evidence:

## Next Segment
- Next: [TT-317](./TT-317_QR_Slate_Tooling.md)
