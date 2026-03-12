#!/usr/bin/env python3
"""
semantic_lint.py — TT-101 semantic invariants (fail-closed)

Checks:
- Each canon segment contains required reader headings
- Each segment H1 contains its TT id
- Forbidden physics-claim phrasing not present (best-effort lint)
"""
from __future__ import annotations
import re, sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Thesis",
    "## Concept Summary",
    "## Operational Implications",
    "## Prerequisites / Next",
]

FORBIDDEN_PHRASES = [
    r"\btime travel is real\b",
    r"\bproves time travel\b",
    r"\bguarantees time travel\b",
    r"\bwe can time travel\b",
    r"\bthis allows time travel\b",
]

def seg_id_from_name(name: str) -> str|None:
    m = re.search(r"(TT-\d{3,4})", name)
    return m.group(1) if m else None

def split_meta_body(text: str) -> tuple[str,str]:
    lines = text.splitlines()
    i = 0
    while i < len(lines) and re.match(r"^\s*[A-Z0-9_]+\s*:\s*.+$", lines[i]):
        i += 1
    return "\n".join(lines[:i]).strip(), "\n".join(lines[i:]).lstrip()

def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    canon = repo / "canon"
    if not canon.exists():
        print("FAIL: canon directory missing")
        return 2

    failures: list[str] = []
    seg_files = sorted([p for p in canon.rglob("*.md") if p.is_file()])

    for p in seg_files:
        sid = seg_id_from_name(p.name)
        if not sid:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        _, body = split_meta_body(text)

        # required headings
        for h in REQUIRED_HEADINGS:
            if h not in body:
                failures.append(f"{p.relative_to(repo)} missing heading: {h}")

        # H1 must contain segment id
        m = re.search(r"(?m)^\s*#\s+(.+)$", body)
        if not m:
            failures.append(f"{p.relative_to(repo)} missing H1")
        else:
            h1 = m.group(1)
            if sid not in h1:
                failures.append(f"{p.relative_to(repo)} H1 missing id {sid} (got: {h1})")

        # forbidden phrases
        for rx in FORBIDDEN_PHRASES:
            if re.search(rx, body, flags=re.I):
                failures.append(f"{p.relative_to(repo)} contains forbidden phrase: /{rx}/")

    if failures:
        print("SEMANTIC_LINT: FAIL\n")
        for f in failures[:300]:
            print(" -", f)
        if len(failures) > 300:
            print(f"... and {len(failures)-300} more")
        return 2

    print("SEMANTIC_LINT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
