# TT-318 — Bootstrap Decoder Slate (Self-Contained Recovery)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---

STATUS: Draft
VERSION: 0.9

## Concept Summary
A minimal “decoder-on-slate” specification so recovery is possible even if modern tools disappear.

## Purpose
Ensure the archive remains decodable with only:
- the etched QR blocks
- basic computation (or manual transcription)
- this bootstrap spec

## How This Fits the Continuity Plan
TT-315/316/317 define the artifact + redundancy + tooling. **TT-318 ensures survivability across software collapse**.

## Explanation
### Minimum decode recipe (language-agnostic)
1) Read `slate.json` (or its printed equivalent): chunk size, ordering, compression flag, payload hash.
2) Decode QR blocks to bytes (byte-mode).
3) Order blocks by index: D000..DNNN.
4) If parity exists and one block missing per group: reconstruct with XOR.
5) Concatenate blocks → compressed stream (optional).
6) If compressed: inflate (zlib).
7) SHA-256 verify payload.

### What must be etched/printed alongside
- Chunk size
- Compression flag
- Payload SHA-256
- Block count
- Parity scheme summary

## Verification
- Perform a recovery using only `slate.json` + blocks (no external metadata).
- Confirm SHA-256 match.

## Notebook Entry
- Date:
- Bootstrap fields etched:
- Recovery rehearsal performed:
- Evidence:

## Next Segment
- Next: [TT-364](./TT-364_Binary_Character_Atlas.md)
