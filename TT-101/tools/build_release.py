#!/usr/bin/env python3
from __future__ import annotations
import sys, zipfile, hashlib, subprocess, re
from pathlib import Path
from datetime import datetime, timezone

def sha256_file(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    repo = Path(__file__).resolve().parents[1]
    tools = repo/"tools"
    dist = repo/"dist"
    dist.mkdir(exist_ok=True)

    subprocess.run([sys.executable, str(tools/"build_handbook_pages.py")], check=False)
    p = subprocess.run([sys.executable, str(tools/"validate_repo.py")], capture_output=True, text=True)
    print(p.stdout)
    if p.returncode != 0:
        print(p.stderr)
        return p.returncode

    manifest = repo/"manifest"/"hashes.txt"
    release = repo/"release"/"RELEASE_v1.0.txt"

    entries = []
    for fp in repo.rglob("*"):
        if fp.is_file():
            rel = fp.relative_to(repo).as_posix()
            if rel.startswith(("manifest/","release/","dist/")):
                continue
            entries.append(f"{sha256_file(fp)}  {rel}")
    entries.sort()
    manifest.write_text("TT-101 MANIFEST — SHA-256 (v1)\n" + "\n".join(entries) + "\n", encoding="utf-8")

    msha = sha256_file(manifest)
    now = datetime.now(timezone.utc).isoformat()
    if release.exists():
        rtxt = release.read_text(encoding="utf-8", errors="ignore")
        rtxt = re.sub(r"(?im)^MANIFEST_SHA256:\s*.*$", f"MANIFEST_SHA256: {msha}", rtxt)
        if re.search(r"(?im)^GENERATED_UTC:", rtxt):
            rtxt = re.sub(r"(?im)^GENERATED_UTC:\s*.*$", f"GENERATED_UTC: {now}", rtxt)
        else:
            rtxt += f"\nGENERATED_UTC: {now}\n"
        release.write_text(rtxt, encoding="utf-8")

    out = dist / f"TT-101_Release_{now.replace(':','-')}.zip"
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for fp in repo.rglob("*"):
            if fp.is_file():
                rel = fp.relative_to(repo).as_posix()
                if rel.startswith("dist/"):
                    continue
                z.write(str(fp), arcname=rel)
    print(f"BUILT: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
