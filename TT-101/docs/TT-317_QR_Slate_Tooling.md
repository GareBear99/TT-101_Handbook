# TT-317 — QR Slate Tooling (Pack/Unpack + Verify)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---

STATUS: Stable
VERSION: 1.0

## Concept Summary
Tooling converts a file into binary chunks (for QR encoding) and reconstructs it back with verification.

## Purpose
Make slate creation and recovery deterministic: same inputs → same outputs, with hashes to prove correctness.

## How This Fits the Continuity Plan
TT-315 defines the binary encoding format. **TT-317 operationalizes it** with repeatable pack/unpack commands.

## Explanation
### Packing
Produces:
- `blocks/D000.bin ...`
- optional `parity/P000.bin ...`
- `slate.json` (includes per-block SHA-256 + payload SHA-256)
- optional `journal_entry.json/.txt`

### Unpacking
Consumes `slate.json` + the scanned/decoded blocks and:
- rebuilds missing chunks (if parity allows)
- verifies per-block hashes (optional strict mode)
- verifies payload hash
- decompresses if required

## Verification
- Run pack → unpack on the same machine and confirm byte-identical payload.
- Verify `payload_sha256` matches `slate.json`.

## Notebook Entry
- Date:
- Input payload filename:
- Output slate directory:
- Payload SHA-256:
- Notes (scanner settings / ECC used / failures observed):

## Next Segment
- Next: [TT-318](./TT-318_Bootstrap_Decoder_Slate.md)
