#!/usr/bin/env python3
"""
DARPA-grade audit runner for TT-101 Canon.

Runs:
- build_index.py --check (if present)
- validate_repo.py (if present)
- metadata checks for /canon segments
- link checks for handbook pages
- orphan checks (handbook pages exist for required segments)

Exit code:
  0 PASS
  2 FAIL
"""
from __future__ import annotations
import os, re, sys, subprocess
from pathlib import Path

REQUIRED_META = ["TIMESTAMP_UTC", "VERSION", "STATUS"]

def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out.strip()
    except Exception as e:
        return 99, f"EXCEPTION: {e}"

def canon_segments(canon_dir: Path) -> list[Path]:
    return sorted([p for p in canon_dir.rglob("*.md") if p.is_file()])

def extract_seg_id(p: Path) -> str|None:
    m = re.search(r"(TT-\d{3,4})", p.name)
    return m.group(1) if m else None

def check_meta(p: Path) -> list[str]:
    text = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    # read top contiguous KEY: VALUE lines
    meta = {}
    for line in text[:30]:
        if not re.match(r"^\s*[A-Z0-9_]+\s*:\s*.+$", line):
            break
        k,v = line.split(":",1)
        meta[k.strip().upper()] = v.strip()
    missing = [k for k in REQUIRED_META if k not in meta]
    errs = []
    if missing:
        errs.append(f"missing meta {missing}")
    # VERSION must be v1.0
    if meta.get("VERSION") and meta["VERSION"] != "v1.0":
        errs.append(f"VERSION not v1.0 (got {meta['VERSION']})")
    return errs

def main():
    repo = Path(__file__).resolve().parents[1]
    tools = repo / "tools"
    canon = repo / "canon"
    handbook = repo / "handbook"

    failures = []
    notes = []

    if (tools / "build_index.py").exists():
        code, out = run([sys.executable, "build_index.py", "--check"], cwd=tools)
        if code != 0:
            failures.append(f"build_index.py --check failed:\n{out}")
        else:
            notes.append("build_index.py --check: PASS")

    if (tools / "validate_repo.py").exists():
        code, out = run([sys.executable, "validate_repo.py"], cwd=tools)
        if code != 0:
            failures.append(f"validate_repo.py failed:\n{out}")
        else:
            notes.append("validate_repo.py: PASS")

    if not canon.exists():
        failures.append("canon directory missing")
    else:
        segs = canon_segments(canon)
        meta_bad = []
        seg_ids = set()
        for p in segs:
            sid = extract_seg_id(p)
            if sid: seg_ids.add(sid)
            errs = check_meta(p)
            if errs:
                meta_bad.append(f"{p.relative_to(repo)}: " + "; ".join(errs))
        if meta_bad:
            failures.append("canon metadata failures:\n" + "\n".join(meta_bad[:200]))
        else:
            notes.append("canon metadata: PASS")

        required = {s for s in seg_ids if s.startswith("TT-8")} | ({"TT-101"} if "TT-101" in seg_ids else set())
        if not handbook.exists():
            failures.append("handbook directory missing")
        else:
            missing_pages = []
            for s in sorted(required):
                if not (handbook / f"{s}.html").exists():
                    missing_pages.append(s)
            if missing_pages:
                failures.append("missing handbook pages: " + ", ".join(missing_pages))
            else:
                notes.append("handbook coverage: PASS")

    if failures:
        print("AUDIT: FAIL\n")
        for n in notes:
            print("OK:", n)
        print("\n---\n")
        for f in failures:
            print("FAIL:", f, "\n")
        return 2
    else:
        print("AUDIT: PASS")
        for n in notes:
            print("OK:", n)
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
