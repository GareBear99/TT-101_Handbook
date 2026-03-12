#!/usr/bin/env python3
"""
Deterministic TT-314 Hello World Slate Generator (v1)

Generates:
- artifacts/slate_hello_world_v1.svg (vector)
- artifacts/slate_hello_world_v1.png (raster preview; optional)

No external dependencies required for SVG.
PNG generation attempts Pillow; if missing, SVG still works.

Design:
- N x N module grid
- 3 finder patterns + timing tracks
- row-major payload fill into data region
- metadata printed as text outside grid
"""
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

PAYLOAD = "HELLO TT-101 :: OPTICAL SLATE TEST v1"
N = 41  # LOW density profile
MODULE = 12  # px per module in SVG (laser can scale)

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def bytes_to_bits(data: bytes) -> list[int]:
    bits = []
    for b in data:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def is_in_finder(r: int, c: int, top: int, left: int) -> bool:
    return top <= r < top+7 and left <= c < left+7

def finder_bit(r: int, c: int, top: int, left: int) -> int:
    # classic-ish: outer ring black, inner ring white, core black
    rr, cc = r-top, c-left
    if rr in (0,6) or cc in (0,6):
        return 1
    if rr in (1,5) or cc in (1,5):
        return 0
    return 1

def reserved(r: int, c: int) -> bool:
    # border 2 modules
    if r < 2 or c < 2 or r >= N-2 or c >= N-2:
        return True
    # finders: TL, TR, BL
    if is_in_finder(r,c,2,2): return True
    if is_in_finder(r,c,2,N-2-7): return True
    if is_in_finder(r,c,N-2-7,2): return True
    # timing tracks (between finders)
    # horizontal timing row at r=2+7 (just below top finders), from after TL finder to before TR finder
    timing_r = 2+7
    if r == timing_r and (2+7) <= c < (N-2-7):
        return True
    # vertical timing col at c=2+7, from after TL finder to before BL finder
    timing_c = 2+7
    if c == timing_c and (2+7) <= r < (N-2-7):
        return True
    return False

def timing_bit(r:int, c:int) -> int:
    # alternating pattern
    if r == 2+7:
        return ((c - (2+7)) % 2)
    if c == 2+7:
        return ((r - (2+7)) % 2)
    return 0

def build_grid() -> tuple[list[list[int]], dict]:
    payload_bytes = PAYLOAD.encode("utf-8")
    h = sha256_hex(payload_bytes)
    bits = bytes_to_bits(payload_bytes)

    grid = [[0 for _ in range(N)] for _ in range(N)]

    # fill reserved structures
    for r in range(N):
        for c in range(N):
            if r < 2 or c < 2 or r >= N-2 or c >= N-2:
                grid[r][c] = 1
            elif is_in_finder(r,c,2,2):
                grid[r][c] = finder_bit(r,c,2,2)
            elif is_in_finder(r,c,2,N-2-7):
                grid[r][c] = finder_bit(r,c,2,N-2-7)
            elif is_in_finder(r,c,N-2-7,2):
                grid[r][c] = finder_bit(r,c,N-2-7,2)
            elif r == 2+7 and (2+7) <= c < (N-2-7):
                grid[r][c] = timing_bit(r,c)
            elif c == 2+7 and (2+7) <= r < (N-2-7):
                grid[r][c] = timing_bit(r,c)

    # data fill row-major into non-reserved cells
    it = iter(bits)
    used = 0
    for r in range(N):
        for c in range(N):
            if reserved(r,c):
                continue
            try:
                b = next(it)
                grid[r][c] = b
                used += 1
            except StopIteration:
                grid[r][c] = 0

    meta = {
        "payload": PAYLOAD,
        "payload_bytes": len(payload_bytes),
        "sha256": h,
        "sha256_16": h[:16],
        "N": N,
        "bits_used": used,
        "bits_total": len(bits),
    }
    return grid, meta

def svg_rect(x,y,w,h,fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'

def write_svg(grid, meta):
    size = N * MODULE
    margin = 40
    w = size + margin*2
    h = size + margin*2 + 120
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">')
    out.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')
    # grid
    gx, gy = margin, margin
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 1:
                out.append(svg_rect(gx + c*MODULE, gy + r*MODULE, MODULE, MODULE, "black"))
    # metadata text
    ty = gy + size + 30
    out.append(f'<text x="{margin}" y="{ty}" font-family="monospace" font-size="16" fill="black">FORMAT: TT-SLATE-BLOCK v1</text>')
    out.append(f'<text x="{margin}" y="{ty+22}" font-family="monospace" font-size="16" fill="black">BLOCK_ID: 0001</text>')
    out.append(f'<text x="{margin}" y="{ty+44}" font-family="monospace" font-size="16" fill="black">PAYLOAD_BYTES: {meta["payload_bytes"]}</text>')
    out.append(f'<text x="{margin}" y="{ty+66}" font-family="monospace" font-size="16" fill="black">CHECK: SHA256:{meta["sha256_16"]}</text>')
    out.append('</svg>')
    svg = "\n".join(out)
    ART.mkdir(exist_ok=True)
    (ART / "slate_hello_world_v1.svg").write_text(svg, encoding="utf-8")

def try_write_png():
    try:
        from PIL import Image
    except Exception:
        return False
    svg_path = ART / "slate_hello_world_v1.svg"
    # Very simple rasterization by re-rendering grid (not full SVG parsing)
    grid, meta = build_grid()
    scale = 4
    img = Image.new("L", (N*scale, N*scale), 255)
    px = img.load()
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 1:
                for rr in range(scale):
                    for cc in range(scale):
                        px[c*scale+cc, r*scale+rr] = 0
    img = img.resize((N*12, N*12))
    img.save(ART / "slate_hello_world_v1.png")
    return True

def main():
    grid, meta = build_grid()
    write_svg(grid, meta)
    png_ok = try_write_png()
    print("TT-314 GENERATED")
    for k,v in meta.items():
        print(f"{k}: {v}")
    print("png_generated:", png_ok)

if __name__ == "__main__":
    main()
