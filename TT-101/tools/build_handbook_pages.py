#!/usr/bin/env python3
"""
build_handbook_pages.py — Generate handbook HTML pages from the canonical docs index.

DARPA invariants (reader reliability):
- No JS-required pagination. Pages are scroll-reader, JS-free.
- Prev/Next links are deterministic and never self-loop.
- The set + order of pages is driven by docs/INDEX.md (single source of truth).
- Custom interactive pages (handbook/TT-364.html, TT-365.html, TT-366.html, TT-367.html, TT-369.html, TT-370.html, TT-990.html)
  are preserved (not overwritten), but their Prev/Next buttons are updated to match the canonical order.

Also generates:
- handbook/index.html (plain-language TOC map)
- handbook/print.html (single-file print edition built from the same page set)

This fixes the mismatch where print.html contained segments that had no per-segment page.
"""
from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime, timezone

CUSTOM_PAGES = {
    "TT-364.html",
    "TT-365.html",
    "TT-366.html",
    "TT-367.html",
    "TT-369.html",
    "TT-370.html",
    "TT-990.html",
}

CUSTOM_SUMMARY = {
    "TT-364": "DIY game: learn every byte (0–255) and decode binary into characters safely.",
    "TT-366": "DIY game: decode binary clues into time-travel words, then solve the crossword.",
    "TT-365": "DIY game: Continuum hangman with binary/ASCII hints; trains byte-first recovery.",
    "TT-367": "Archive Journal + Continuity Token: record verifiable actions and hash-chain them.",
    "TT-369": "Practice: paste a QR block and verify its SHA-256 vs slate.json; log results.",
    "TT-370": "Rules: which segments may generate journal lines (only meaningful, verifiable ones).",
    "TT-990": "Appendix: full binary decoder dictionary (0–255) for offline reference.",
}

def seg_id_from_name(name: str) -> str|None:
    m = re.search(r"(TT-\d{3,4})", name)
    return m.group(1) if m else None

def split_meta_body(text: str) -> tuple[str,str]:
    lines = text.splitlines()
    i = 0
    while i < len(lines) and re.match(r"^\s*[A-Z0-9_]+\s*:\s*.+$", lines[i]):
        i += 1
    return "\n".join(lines[:i]).strip(), "\n".join(lines[i:]).lstrip()

def md_to_html(md: str) -> str:
    """Small, deterministic markdown-to-html converter (enough for this repo)."""
    html_lines: list[str] = []
    in_code = False
    in_ul = False

    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def linkify(line: str) -> str:
        # [text](url) -> anchor
        def repl(m: re.Match) -> str:
            return f"<a href='{m.group(2)}'>{m.group(1)}</a>"
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, line)

    for raw in md.splitlines():
        line = raw.rstrip("\n")

        if line.startswith("```"):
            if not in_code:
                html_lines.append("<pre><code>")
                in_code = True
            else:
                html_lines.append("</code></pre>")
                in_code = False
            continue

        if in_code:
            html_lines.append(esc(raw))
            continue

        # unordered list
        if re.match(r"^\s*-\s+", line):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item = re.sub(r"^\s*-\s+", "", line)
            html_lines.append(f"<li>{linkify(item)}</li>")
            continue
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl = len(m.group(1))
            html_lines.append(f"<h{lvl}>{linkify(m.group(2))}</h{lvl}>")
            continue

        if line.strip() == "":
            html_lines.append("<div class='sp'></div>")
            continue

        html_lines.append(f"<p>{linkify(line)}</p>")

    if in_ul:
        html_lines.append("</ul>")
    if in_code:
        html_lines.append("</code></pre>")

    return "\n".join(html_lines)

SHELL = """<!doctype html>
<html lang=\"en\"><head>
<meta charset=\"utf-8\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/>
<title>{sid} — TT-101 Handbook</title>
<link rel=\"stylesheet\" href=\"../assets/book.css\"/>
</head><body>
  <div class=\"book-shell\">
    <aside class=\"book-nav\">
      <div class=\"kicker\">TT-101</div>
      <div class=\"title\">{sid}</div>

      <a class=\"btn\" href=\"./START_HERE.html\">Start Here</a>
      <a class=\"btn\" href=\"./index.html\">All Segments</a>
      <a class=\"btn\" href=\"./print.html\">Print Edition</a>
      <a class=\"btn\" href=\"../index.html\">Main Landing</a>

      <div class=\"btnrow\" aria-label=\"Pager\">
        {prev_btn}
        {next_btn}
      </div>

      <div style=\"margin-top:12px\">
        <div style=\"font-size:12px; opacity:.9\">Reader Mode</div>
        <div style=\"margin-top:6px; font-size:12px; opacity:.85\" class=\"page-num\">Scroll (JS-free) · Use Prev/Next</div>
      </div>
    </aside>

    <main class=\"paper-scroll\">
      <article class=\"paper-body dropcap\">
        {body}
      </article>
      <footer class=\"paper-footer\">
        <div class=\"pn\">{sid}</div>
        <div class=\"pn\">Generated: {gen}</div>
      </footer>
    </main>
  </div>
</body></html>
"""

def btn(label: str, href: str, disabled: bool=False) -> str:
    if disabled:
        return f"<span class='btn disabled' aria-disabled='true'>{label}</span>"
    return f"<a class='btn' href='{href}'>{label}</a>"

def extract_summary(md_text: str) -> str:
    # remove metadata
    lines = [l.strip() for l in md_text.splitlines() if l.strip() and not re.match(r"^[A-Z0-9_]+:\s*.+$", l)]
    if lines and lines[0].startswith("#"):
        lines = lines[1:]
    for l in lines[:30]:
        if l.startswith("#"):
            continue
        return l[:160]
    return ""

def patch_custom_nav(html_text: str, prev_href: str, next_href: str) -> str:
    # Update the first Prev/Next hrefs found inside the Pager block.
    html_text = re.sub(r"(aria-label=\"Pager\"[\s\S]*?href=\")([^\"]+)(\"[^>]*>← Prev<)", rf"\1{prev_href}\3", html_text, count=1)
    html_text = re.sub(r"(aria-label=\"Pager\"[\s\S]*?href=\")([^\"]+)(\"[^>]*>Next →<)", rf"\1{next_href}\3", html_text, count=1)
    return html_text

def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    docs = repo / "docs"
    hb = repo / "handbook"
    hb.mkdir(exist_ok=True)

    # Parse docs/INDEX.md to get the canonical ordered list.
    idx = (docs / "INDEX.md").read_text(encoding="utf-8", errors="ignore")
    rels = re.findall(r"\(([^)]+\.md)\)", idx)

    ordered: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for rel in rels:
        rel = rel.strip()
        p = docs / rel
        if not p.exists():
            continue
        sid = seg_id_from_name(p.name)
        if not sid:
            continue
        if sid in seen:
            continue
        seen.add(sid)
        ordered.append((sid, p))

    # Force the DIY ladder order right after TT-315:
    # TT-364 (atlas) -> TT-366 (crossword) -> TT-365 (hangman)
    sids = [sid for sid, _ in ordered]
    def remove_if_present(x: str):
        while x in sids:
            sids.remove(x)

    remove_if_present("TT-364")
    remove_if_present("TT-365")
    remove_if_present("TT-366")

    if "TT-315" in sids:
        ins = sids.index("TT-315") + 1
        # Insert TT-364 if the custom page exists.
        if (hb / "TT-364.html").exists():
            sids.insert(ins, "TT-364"); ins += 1
        # TT-366 and TT-365 are custom pages in this repo.
        if (hb / "TT-366.html").exists():
            sids.insert(ins, "TT-366"); ins += 1
        if (hb / "TT-365.html").exists():
            sids.insert(ins, "TT-365")

    # Add appendix dictionary at end if present.
    if (hb / "TT-990.html").exists() and "TT-990" not in sids:
        sids.append("TT-990")

    gen_time = datetime.now(timezone.utc).isoformat()

    # Build markdown-driven pages (skip custom pages; keep them but update nav later)
    by_sid = {sid: p for sid, p in ordered}

    # Remove previously generated TT pages (except custom).
    for p in hb.glob("TT-*.html"):
        if p.name in CUSTOM_PAGES:
            continue
        p.unlink()

    for i, sid in enumerate(sids):
        out = hb / f"{sid}.html"
        prev_href = f"./{sids[i-1]}.html" if i > 0 else "#"
        next_href = f"./{sids[i+1]}.html" if i < len(sids)-1 else "#"

        if out.name in CUSTOM_PAGES and out.exists():
            # Patch navigation only.
            html = out.read_text(encoding="utf-8", errors="ignore")
            out.write_text(patch_custom_nav(html, prev_href, next_href), encoding="utf-8")
            continue

        src = by_sid.get(sid)
        if not src:
            # Missing source: create a stub page that still doesn't break paging.
            body = f"<h1>{sid}</h1><p><b>Missing source file.</b> This segment is referenced in docs/INDEX.md but the markdown file was not found.</p>"
        else:
            md = src.read_text(encoding="utf-8", errors="ignore")
            _meta, body_md = split_meta_body(md)
            body = md_to_html(body_md)

        prev_btn = btn("← Prev", prev_href, disabled=(prev_href == "#"))
        next_btn = btn("Next →", next_href, disabled=(next_href == "#"))
        out.write_text(SHELL.format(sid=sid, prev_btn=prev_btn, next_btn=next_btn, body=body, gen=gen_time), encoding="utf-8")

    # Build handbook index with plain-language summaries.
    items = []
    for sid in sids:
        summ = CUSTOM_SUMMARY.get(sid)
        if not summ:
            src = by_sid.get(sid)
            summ = extract_summary(src.read_text(encoding="utf-8", errors="ignore")) if src else ""
        items.append(f"<li><a href='./{sid}.html'>{sid}</a> <span class='toc-sum'>{summ}</span></li>")

    (hb / "index.html").write_text(
        f"""<!doctype html>
<html lang='en'><head>
<meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>TT-101 Handbook — Index</title>
<link rel='stylesheet' href='../assets/book.css'/>
<style>.toc-sum{{opacity:.75;margin-left:.5rem;font-size:.95em}}</style>
</head><body>
<div class='book-shell' style='grid-template-columns:1fr'>
  <main class='page'>
    <div class='page-inner'>
      <div class='page-header'>
        <div class='page-kicker'>TT-101 Handbook</div>
        <div class='page-title'>All Segments</div>
      </div>
      <div class='page-body'>
        <p><a href='./START_HERE.html'>Start Here</a> · <a href='./print.html'>Print Edition</a> · <a href='../index.html'>Main Landing</a></p>
        <h2>Plain-language map</h2>
        <p>One sentence per segment so you can navigate fast.</p>
        <ul>{''.join(items)}</ul>
      </div>
      <div class='page-footer'>
        <div class='pn'>Total: {len(sids)}</div>
        <div class='pn'>Generated: {gen_time}</div>
      </div>
    </div>
  </main>
</div></body></html>""",
        encoding="utf-8",
    )

    # Build print edition from the same pages set (ensures no mismatch).
    toc_lines = [f"<li><b>{sid}</b> — {CUSTOM_SUMMARY.get(sid,'')}</li>" for sid in sids]
    toc_html = "<h1>TT-101 Print Edition</h1><h2>Table of Contents — Plain Language</h2><ul>" + "".join(toc_lines) + "</ul><hr/>"

    sections = []
    for sid in sids:
        page = hb / f"{sid}.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"<article[^>]*>([\s\S]*?)</article>", html)
        body = m.group(1) if m else html
        sections.append(f"<section class='print-section' id='{sid}'><h2>{sid}</h2>{body}</section>")

    (hb / "print.html").write_text(
        f"""<!doctype html><html lang='en'><head>
<meta charset='utf-8'/><meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>TT-101 Handbook — Print</title>
<link rel='stylesheet' href='../assets/book.css'/>
<style>.print-section{{page-break-before:always}} .print-section h2{{margin-top:0}}</style>
</head><body><main class='paper-scroll' style='padding:24px'>
{toc_html}
{''.join(sections)}
</main></body></html>""",
        encoding="utf-8",
    )

    print(f"BUILT {len(sids)} handbook segment pages (docs-index driven).")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
