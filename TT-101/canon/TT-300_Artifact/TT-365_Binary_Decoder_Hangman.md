TIMESTAMP_UTC: 2026-03-05T00:00:00Z
VERSION: v1.0
STATUS: ACTIVE
TIER: TT-300 (Artifact / Slate Decoding)

# TT-365 Binary Decoder + Binary Hangman (DIY Handbook Game)

## Concept Summary
This segment provides two practical tools for slate/QR recovery work:

1) **Binary Decoder** — convert 8-bit (or 7/16-bit) binary into characters and codepoints.
2) **Binary Hangman (DIY game)** — a small training game that teaches binary↔text by solving a target word.

The target word for the included game is: **Continuum**.

## Operational Implications
- Helps verify that **scanned QR bytes** and **decoded payload bytes** map to expected text.
- Acts as a human training exercise for working with byte-aligned encodings under degraded tooling.

## Prerequisites / Next
Prerequisites:
- TT-310 Decoding Ladder (Rosetta)
- TT-315 Binary QR Slate Encoding

Next:
- Use the interactive handbook tool: `handbook/TT-365.html`

## Notes
- “All possible characters” in this context means **all 256 byte values (0–255)** with safe display rules for non-printables.
- This segment does not claim time travel is real; it is an encoding/decoding utility.
