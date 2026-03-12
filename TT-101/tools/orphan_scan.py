#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

def seg_id_from_name(name: str):
    m = re.search(r"(TT-\d{3,4})", name)
    return m.group(1) if m else None

def main():
    repo = Path(__file__).resolve().parents[1]
    index = repo/"index.html"
    canon = repo/"canon"
    if not index.exists():
        print("ORPHAN_SCAN: FAIL\n - index.html missing")
        return 2
    idx = index.read_text(encoding="utf-8", errors="ignore")
    ids = re.findall(r"(TT-\d{3,4})", idx)
    dupes = {x for x in set(ids) if ids.count(x) > 1}
    canon_ids = set()
    for md in canon.rglob("*.md"):
        sid = seg_id_from_name(md.name)
        if sid:
            canon_ids.add(sid)
    missing = sorted([sid for sid in canon_ids if sid not in set(ids)])
    failures = []
    if dupes:
        failures.append("duplicate ids in index.html: " + ", ".join(sorted(dupes)))
    for sid in missing:
        failures.append(f"missing from index.html: {sid}")
    if failures:
        print("ORPHAN_SCAN: FAIL\n")
        for f in failures[:300]:
            print(" -", f)
        return 2
    print("ORPHAN_SCAN: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
