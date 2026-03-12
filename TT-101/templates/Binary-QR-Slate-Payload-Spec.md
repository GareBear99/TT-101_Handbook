# Binary QR Slate Payload Spec (TTB1)

Use this template when creating a slate payload intended to be split into QR blocks.

## Payload identity
- Payload Name:
- Payload Type: (ZIP / TAR / RAW / TEXT-MIRROR)
- Compression: (none / zlib-deflate)
- Flags:

## Integrity
- SHA-256(payload_bytes):
- CRC32(payload_bytes) [optional]:

## Chunking plan
- Block count (N):
- Target bytes per QR:
- Error correction level: (L / M / Q / H)
- Module size (mm):
- QR version (if fixed):

## Outer label (etch text)
- Title line:
- Format line:
- Verify line:
- Decode ladder pointer:

## Notes
- Include at least one “Rosetta” decoding pointer (TT-308/TT-310).
- Avoid executable payloads. Prefer data and source.
