# TT-364 — Binary Character Atlas (0–255) + Decoder (DIY Game (Canon))

TIMESTAMP_UTC: 2026-03-05T00:00:00Z  
VERSION: 1.0  
STATUS: ACTIVE  

## Purpose
Provide an offline, deterministic way to decode **all possible 8-bit values (0–255)** into characters and common encodings (ASCII control names, printable ASCII, Latin-1), and to practice binary decoding as a first training step for QR-slate recovery.

## What This Establishes Now (Journal-Applicable)
This segment is journal-applicable because it produces verifiable outcomes:
- The decoding mode used (7-bit / 8-bit / 16-bit grouping)
- Sample input bytes and decoded output
- Any observed ambiguities (e.g., control codes)

## Safety / Scope
This is an encoding/decoding training tool. It does not claim time travel is real. It supports the archive's goal of **recoverability** and **integrity**.

## Output
- A byte table 0–255
- A decoder box (binary/hex/text input)
- A journal line generator compatible with TT-367 continuity token
