#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

def seg_id_from_name(name: str):
    m = re.search(r"(TT-\d{3,4})", name)
    return m.group(1) if m else None

def find_links(text: str):
    out = []
    for m in MD_LINK.finditer(text):
        url = m.group(1).strip()
        if url.startswith(("http://","https://","mailto:","#")):
            continue
        url = url.split("#",1)[0].split("?",1)[0].replace('\\','/').strip()
        if url:
            out.append(url)
    return out

def main():
    repo = Path(__file__).resolve().parents[1]
    all_files = {p.relative_to(repo).as_posix() for p in repo.rglob("*") if p.is_file()}
    failures = []
    canon = repo/"canon"
    for md in sorted(canon.rglob("*.md")):
        sid = seg_id_from_name(md.name)
        if not sid:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        for lp in find_links(text):
            target = (md.parent/lp).resolve()
            try:
                rel = target.relative_to(repo.resolve()).as_posix()
            except Exception:
                failures.append(f"{md.relative_to(repo)} link escapes repo: {lp}")
                continue
            if rel not in all_files:
                failures.append(f"{md.relative_to(repo)} broken link: {lp}")
    hb = repo/"handbook"
    required = set()  # v2.8: require handbook page for every canon segment
    for md in canon.rglob("TT-*.md"):
        sid = seg_id_from_name(md.name)
        if sid:
            required.add(sid)
    for sid in sorted(required):
        if not (hb/f"{sid}.html").exists():
            failures.append(f"missing handbook page: handbook/{sid}.html")
    if failures:
        print("LINK_LINT: FAIL\n")
        for f in failures[:300]:
            print(" -", f)
        return 2
    print("LINK_LINT: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
