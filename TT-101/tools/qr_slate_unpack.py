#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, hashlib, zlib
from pathlib import Path

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def load_bin(path: Path) -> bytes:
    return path.read_bytes()

def try_recover_missing(blocks: dict[int, bytes], n: int, chunk: int, slate: dict, base_dir: Path) -> dict[int, bytes]:
    # Supports TT-316 XOR parity:
    # - global P0 recovers exactly 1 missing overall
    # - group parity PGxx recovers exactly 1 missing within a group (per group)
    missing = [i for i in range(n) if i not in blocks]
    if not missing:
        return blocks

    G = int(slate.get("parity_groups") or 0)
    parity = slate.get("parity") or {}

    def xor_many(idxs):
        out = bytes([0] * chunk)
        for i in idxs:
            out = xor_bytes(out, blocks[i])
        return out

    if len(missing) == 1 and "P0" in parity:
        p0 = load_bin(base_dir / parity["P0"]["file"])
        present = [i for i in range(n) if i in blocks]
        rec = xor_bytes(p0, xor_many(present))
        blocks[missing[0]] = rec
        return blocks

    if G > 0:
        missing_by_group: dict[int, list[int]] = {}
        for i in missing:
            g = i % G
            missing_by_group.setdefault(g, []).append(i)

        for g, miss_list in missing_by_group.items():
            if len(miss_list) != 1:
                continue
            key = f"PG{g:02d}"
            if key not in parity:
                continue
            pg = load_bin(base_dir / parity[key]["file"])
            present = [i for i in range(n) if i in blocks and (i % G) == g]
            rec = xor_bytes(pg, xor_many(present))
            blocks[miss_list[0]] = rec

    return blocks

def main():
    ap = argparse.ArgumentParser(description="Unpack a binary QR slate set into the original payload.")
    ap.add_argument("--slate", required=True, help="Path to slate.json")
    ap.add_argument("--out", required=True, help="Output file path (recovered bytes)")
    args = ap.parse_args()

    slate_path = Path(args.slate)
    base_dir = slate_path.parent
    slate = json.loads(slate_path.read_text(encoding="utf-8"))

    n = int(slate["blocks"]["count"])
    chunk = int(slate["chunk_bytes"])
    payload_len = int(slate["payload_len"])
    expected = slate["payload_sha256"]
    compress = slate.get("compress", "none")

    blocks: dict[int, bytes] = {}
    for i in range(n):
        fp = base_dir / "blocks" / f"D{i:03d}.bin"
        if fp.exists():
            b = fp.read_bytes()
            if len(b) != chunk:
                raise SystemExit(f"BLOCK SIZE ERROR: {fp} expected {chunk} bytes got {len(b)}")
            blocks[i] = b

    blocks = try_recover_missing(blocks, n, chunk, slate, base_dir)

    missing = [i for i in range(n) if i not in blocks]
    if missing:
        raise SystemExit(f"RECOVERY FAIL: missing blocks {missing}. Add mirrors or parity.")

    payload_padded = b"".join(blocks[i] for i in range(n))
    payload = payload_padded[:payload_len]

    if sha256_bytes(payload) != expected:
        raise SystemExit("HASH FAIL: payload SHA-256 does not match slate.json")

    if compress == "zlib":
        payload = zlib.decompress(payload)

    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_bytes(payload)
    print("OK: recovered payload to", outp)

if __name__ == "__main__":
    main()
