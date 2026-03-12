#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

META_REQ = ["TIMESTAMP_UTC", "VERSION", "STATUS"]

def split_meta(text: str):
    lines = text.splitlines()
    meta = []
    for line in lines[:80]:
        if re.match(r"^\s*[A-Z0-9_]+\s*:\s*.+$", line):
            meta.append(line)
        else:
            break
    return meta

def main():
    repo = Path(__file__).resolve().parents[1]
    canon = repo/"canon"
    failures = []
    for md in canon.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        meta = "\n".join(split_meta(text))
        for k in META_REQ:
            if f"{k}:" not in meta:
                failures.append(f"{md.relative_to(repo)} missing metadata key: {k}")
        if re.search(r"(?m)[ \t]{4,}$", text):
            failures.append(f"{md.relative_to(repo)} has long trailing whitespace")
        if re.search(r"\bTODO\b", text):
            failures.append(f"{md.relative_to(repo)} contains TODO")
        # v2.7 required publication assets
    req = [
        repo/'assets'/'book.css',
        repo/'assets'/'diagrams'/'continuity_pivot_window.svg',
        repo/'assets'/'diagrams'/'ics_loop.svg',
        repo/'assets'/'diagrams'/'artifact_pipeline.svg',
        repo/'handbook'/'print.html',
    ]
    for rp in req:
        if not rp.exists():
            failures.append(f"missing required asset: {rp.relative_to(repo)}")

    if failures:
        print("STYLE_LINT: FAIL\n")
        for f in failures[:300]:
            print(" -", f)
        return 2
    print("STYLE_LINT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
