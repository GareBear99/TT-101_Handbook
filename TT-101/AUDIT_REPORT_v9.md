# DARPA Audit Report — v9 (Nav Containment + De-dup)

Generated: 2026-03-02T21:59:25.660719Z

## Finding
A legacy “link dump” segment existed outside the TOC panel and rendered below the card,
creating the appearance of duplicated navigation.

## Fix
- Removed the legacy nav-dump segment from `index.html`.
- Enforced strict containment:
  - `.card { overflow: hidden; }`
  - `.bd.toc` gets a viewport-relative max height and internal scrolling
- Validator now fails if `index.html` contains anything other than **exactly one** `class="bd toc"`.

## Validation
tools/validate_repo.py → VALIDATION OK

## MANIFEST_SHA256
e89be3753355e086e54da8aafdcf94936a0a538cd9672000e0842b7438c1f06f
