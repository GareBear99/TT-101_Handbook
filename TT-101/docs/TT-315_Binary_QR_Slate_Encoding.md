# TT-315 Binary QR Slate Encoding (Smallest-Size Storage)

> “Knowledge preserved is civilization extended.”
> — Unknown Archivist

---


**Purpose:** Define a **binary-first** encoding pathway for QR-code “slates” (laser‑etched or printed) where the payload is stored in **raw bytes** for maximum density and minimal file size.

This segment complements:
- **TT-307–TT-314** (Optical Slate Passive Core + decoding ladder + block formats)
- **TT-312** (Laser workflow / QA)
- **TT-309** (Erosion‑tolerant error correction)

---

## Scope and assumptions

- QR codes are used as the *optical carrier*.
- The archival payload is treated as **bytes**, not text.
- The system is designed to survive:
  - device loss / software loss
  - partial slate damage
  - imperfect scanning
- This is a **storage + decoding** spec, not proof of time travel.

---

## Design goals

1. **Density:** use QR **Byte mode** where possible.
2. **Determinism:** chunking and reconstruction must be unambiguous.
3. **Redundancy:** tolerate missing or corrupted QR blocks.
4. **Decode ladder compatibility:** include a minimal human-readable outer wrapper so future readers can reconstruct tooling.

---

## High-level approach

A complete “slate payload” is serialized as:

1) **Envelope bytes** (a small header)
2) **Payload bytes** (the actual archive segment, compressed or raw)
3) **Integrity bytes** (hashes / checksums)
4) Split into **QR blocks** (chunks) with per-block checks

### Key principle
**Binary is the canonical layer**. Any text labels are *only* for decoding guidance.

---

## Binary envelope format (TTB1)

**Magic:** 4 bytes  
`TTB1` (0x54 0x54 0x42 0x31)

**Header (fixed):**
- `u8 version` (currently `1`)
- `u8 flags`
  - bit0 = payload compressed (zlib/deflate)
  - bit1 = payload is a ZIP container
  - bit2 = payload is a TAR container
  - bit3 = payload is raw single file
- `u16 header_len` (bytes, big-endian) — for forward compatibility

**Body (variable):**
- `u32 payload_len` (bytes, big-endian)
- `payload_bytes[payload_len]`
- `sha256_payload[32]` (SHA-256 over *payload_bytes* only)

**Optional (recommended when chunking):**
- `u32 crc32_payload` (CRC32 over payload_bytes)

### Why SHA-256 + CRC32?
- CRC32: fast error detection on reconstruction (human debugging / fast reject)
- SHA-256: strong integrity guarantee for final verification

---

## Compression choice

If the goal is **smallest size**, enable compression flag (bit0) and compress the payload bytes using **zlib/deflate**.

**Note:** For deep-time resilience, you may store **both**:
- a compressed payload (density)
- an uncompressed payload (simplicity)
…on separate slates or separate layers.

---

## QR chunking format (Structured Blocks)

Because a single QR may be insufficient, split the `TTB1` byte stream into blocks.

Each QR block encodes:

**Block header (binary, before block data):**
- `u16 block_index` (0…N-1)
- `u16 block_count` (N)
- `u32 stream_offset` (byte offset into the full TTB1 stream)
- `u16 block_len` (bytes of block_data)
- `u32 crc32_block` (CRC32 over block_data only)

**Block data:**
- `block_data[block_len]` — slice of the full TTB1 stream

### Reconstruction algorithm
1. Collect blocks
2. Verify `crc32_block` per block
3. Sort by `stream_offset`
4. Concatenate `block_data` to reconstruct full stream
5. Parse `TTB1`, extract `payload_bytes`
6. Verify `sha256_payload` (and CRC32 payload if present)

---

## QR capacity guidance (practical)

Density depends on:
- QR Version (size)
- Error correction level (L/M/Q/H)
- Print/etch quality
- Scanner quality

**Rule of thumb for etched slates:**
- prefer **lower density** than theoretical maximum
- prefer **Q or H** error correction for damage tolerance
- increase module size (bigger squares) for reliability

---

## Minimal human-readable wrapper (outer label)

Every slate should include an outer label (etched text) that explains:

- This is a **Binary QR Slate**
- Expected decoding steps:
  - scan all QR blocks
  - reconstruct TTB1 stream
  - verify SHA-256
  - decompress (if flagged)
- A pointer to the decoding ladder document (TT-308 / TT-310)

Example outer label (suggested):
- `TT-315 / BINARY QR SLATE / FORMAT: TTB1 / BLOCKED / VERIFY SHA-256`

---

## Security and safety (non-negotiable)

- **Do not execute** decoded payloads.
- Treat decoded files as **data** until inspected.
- Prefer storing:
  - plain text
  - simple structured files (JSON / CBOR)
  - images / diagrams
  - source code
- Avoid distributing opaque executables.

---

## Reference: Python decode sketch (illustrative)

This is a minimal reconstruction outline (not a full toolchain):

```python
# blocks = list of dicts with fields: idx,count,offset,data,crc32
# 1) validate crc32 per block
# 2) sort by offset
# 3) concatenate data
# 4) parse TTB1, verify sha256, decompress if flagged
```

---

## Next recommended additions

- TT-315A: “QR Block Redundancy (RAID-like parity blocks)”
- TT-315B: “Multi‑format payload (ZIP + plaintext mirror)”
- TT-315C: “Rosetta ‘tooling seed’ slate (minimal decoder implementation)”

## Related segments (next)
- **TT-316** QR Slate Redundancy & Parity
- **TT-317** QR Slate Tooling (Pack/Unpack + Verify)
- **TT-318** Bootstrap Decoder Slate


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

- Next: [TT-364](./TT-364_Binary_Character_Atlas.md)
