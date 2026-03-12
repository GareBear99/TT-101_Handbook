#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, zlib, hashlib
from pathlib import Path
from datetime import datetime, timezone

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def main():
    ap = argparse.ArgumentParser(description="Pack a file into binary QR slate blocks (+ optional XOR parity).")
    ap.add_argument("--in", dest="inp", required=True, help="Input file path")
    ap.add_argument("--out", dest="outdir", required=True, help="Output directory")
    ap.add_argument("--chunk-bytes", type=int, default=900, help="Bytes per block (QR byte-mode payload size)")
    ap.add_argument("--compress", choices=["none","zlib"], default="none", help="Optional compression")
    ap.add_argument("--parity-groups", type=int, default=0, help="0 disables parity; N enables N group parities (+global P0)")
    args = ap.parse_args()

    src = Path(args.inp)
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    blocks_dir = out/"blocks"
    parity_dir = out/"parity"
    blocks_dir.mkdir(exist_ok=True)
    if args.parity_groups > 0:
        parity_dir.mkdir(exist_ok=True)

    raw = src.read_bytes()
    payload = raw
    if args.compress == "zlib":
        payload = zlib.compress(payload, level=9)

    payload_len = len(payload)
    chunk = args.chunk_bytes
    n_blocks = (payload_len + chunk - 1) // chunk
    padded_len = n_blocks * chunk
    payload_padded = payload + (b"\x00" * (padded_len - payload_len))

    blocks: list[bytes] = []
    block_sha256: list[str] = []
    for i in range(n_blocks):
        blk = payload_padded[i*chunk:(i+1)*chunk]
        blocks.append(blk)
        (blocks_dir / f"D{i:03d}.bin").write_bytes(blk)
        block_sha256.append(sha256_bytes(blk))

    parity = {}
    if args.parity_groups > 0:
        # P0 global parity
        p0 = bytes([0]*chunk)
        for blk in blocks:
            p0 = xor_bytes(p0, blk)
        (parity_dir/"P0.bin").write_bytes(p0)
        parity["P0"] = {"file": "parity/P0.bin", "sha256": sha256_bytes(p0)}

        G = args.parity_groups
        for g in range(G):
            pg = bytes([0]*chunk)
            for i, blk in enumerate(blocks):
                if i % G == g:
                    pg = xor_bytes(pg, blk)
            fname = f"PG{g:02d}.bin"
            (parity_dir/fname).write_bytes(pg)
            parity[f"PG{g:02d}"] = {"file": f"parity/{fname}", "group": g, "sha256": sha256_bytes(pg)}

    slate = {
        "schema": "TT-315/QR_SLATE_v1",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": src.as_posix(),
        "compress": args.compress,
        "chunk_bytes": chunk,
        "payload_len": payload_len,
        "payload_sha256": sha256_bytes(payload),
        "blocks": {"count": n_blocks, "pattern": "blocks/D{index:03d}.bin", "sha256": block_sha256},
        "parity_groups": args.parity_groups,
        "parity": parity,
        "notes": [
            "Encode each *.bin as QR in BYTE MODE for maximum density.",
            "If using text-only QR tools, base64 is possible but larger."
        ],
    }
    (out/"slate.json").write_text(json.dumps(slate, indent=2, sort_keys=True), encoding="utf-8")

    label = "\n".join([
        "TT-315 QR SLATE (v1)",
        f"CHUNK_BYTES={chunk}",
        f"BLOCKS={n_blocks}",
        f"COMPRESS={args.compress}",
        f"PAYLOAD_LEN={payload_len}",
        f"SHA256={slate['payload_sha256']}",
        f"PARITY_GROUPS={args.parity_groups}",
        "ORDER=D000..DNNN (+ optional P0, PGxx)",
    ]) + "\n"
    (out/"outer_label.txt").write_text(label, encoding="utf-8")


# journal entry artifacts (for TT-367 continuity journal)
try:
    slate_bytes = (out/"slate.json").read_bytes()
    slate_sha = sha256_bytes(slate_bytes)
    j = {
        "schema": "TT-367/JOURNAL_ENTRY_v1",
        "t_utc": slate["generated_utc"],
        "segment": "TT-315",
        "title": "QR slate packed",
        "content": f"Packed {src.name} into {n_blocks} blocks (chunk={chunk}, compress={args.compress}, parity_groups={args.parity_groups}).",
        "evidence": [
            f"payload_sha256={slate['payload_sha256']}",
            f"slate_json_sha256={slate_sha}",
            f"blocks={n_blocks}",
            f"chunk_bytes={chunk}",
        ]
    }
    (out/"journal_entry.json").write_text(json.dumps(j, indent=2, sort_keys=True), encoding="utf-8")
    (out/"journal_entry.txt").write_text(
        "\n".join([j["t_utc"], j["segment"], j["title"], j["content"]] + j["evidence"]) + "\n",
        encoding="utf-8"
    )
except Exception:
    pass

    print(f"OK: wrote {n_blocks} blocks to {blocks_dir}")
    if args.parity_groups > 0:
        print(f"OK: wrote parity blocks to {parity_dir}")
    print("OK: wrote slate.json and outer_label.txt")

if __name__ == "__main__":
    main()
