#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canon"
INDEX = ROOT / "index.html"

def band_key(p: Path) -> int:
    m = re.match(r"TT-(\d{3})_", p.name)
    return int(m.group(1)) if m else 9999

def tt_key(p: Path):
    m = re.match(r"TT-(\d{3})", p.stem)
    n = int(m.group(1)) if m else 9999
    return (n, p.stem)

def extract_h1(md: Path) -> str:
    try:
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return md.stem.replace("_", " ")

def build_groups():
    groups = []
    for band in sorted([d for d in CANON.iterdir() if d.is_dir()], key=band_key):
        bnum = band_key(band)
        label = band.name.split("_", 1)[1].replace("_", " ").upper() if "_" in band.name else band.name.upper()
        header = f"TT-{bnum} — {label}"
        items = []
        for md in sorted(band.glob("*.md"), key=tt_key):
            tid = md.stem.split("_", 1)[0]
            title = extract_h1(md)
            right = title[len(tid):].strip(" —-") if title.startswith(tid) else title
            items.append((str(md.relative_to(ROOT)).replace("\\", "/"), f"{tid} — {right}"))
        if items:
            groups.append((header, items))

    rel_item = ("release/RELEASE_v1.0.txt", "Release — v1.0 Statement")
    man_item = ("manifest/hashes.txt", "Manifest — Integrity Hashes")
    for i, (h, items) in enumerate(groups):
        if h.startswith("TT-900"):
            out = []
            inserted = False
            for href, label in items:
                out.append((href, label))
                if href.endswith("TT-940_Release_Statement.md"):
                    out.append(rel_item); out.append(man_item)
                    inserted = True
            if not inserted:
                out.append(rel_item); out.append(man_item)
            groups[i] = (h, out)
            break
    else:
        groups.append(("TT-900 — META", [rel_item, man_item]))
    return groups

def render_toc(groups):
    lines = ['      <div class="bd toc">']
    for header, items in groups:
        lines.append(f'        <div class="toc-h">{header}</div>')
        for href, label in items:
            if "—" in label:
                left, right = [x.strip() for x in label.split("—", 1)]
                lines.append(f'        <a href="{href}"><b>{left}</b> — {right}</a>')
            else:
                lines.append(f'        <a href="{href}">{label}</a>')
        lines.append('        <div class="sep"></div>')
    lines[-1] = '      </div>'
    return "\n".join(lines) + "\n"

def main():
    html = INDEX.read_text(encoding="utf-8", errors="replace")
    begin, end = "<!-- TOC:BEGIN -->", "<!-- TOC:END -->"
    if begin not in html or end not in html:
        raise SystemExit("index.html missing TOC markers")
    toc = render_toc(build_groups())
    new = re.sub(re.escape(begin) + r".*?" + re.escape(end),
                 begin + "\n" + toc + "      " + end,
                 html, flags=re.S)
    if "--check" in sys.argv:
        if new != html:
            raise SystemExit("index.html TOC is out of date. Run: python3 tools/build_index.py")
        return
    INDEX.write_text(new, encoding="utf-8")

if __name__ == "__main__":
    main()
