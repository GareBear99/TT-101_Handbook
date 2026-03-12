# TT-331 — Morse Code Fundamentals (Signal Continuity Layer)

> “Information is the resolution of uncertainty.”
> — Claude Shannon

---

Morse code is a **time-based encoding**: information is carried by **duration** and **spacing**, not by ink, pixels, or power.
That makes it valuable for continuity systems because it can be transmitted and recovered with:

- sound (beeps)
- light (flashes)
- taps (mechanical)
- radio (continuous wave)
- simple on/off circuits

This segment introduces the **rules** you’ll use in the Morse training games and in any low-tech “beacon” scenario.

## Core Symbols
Morse uses two signal elements:

- **Dit** = `.` (short)
- **Dah** = `-` (long)

## Timing Rules (ITU-style)
All timing is based on a single unit length **T**.

- Dit length = **1T**
- Dah length = **3T**
- Intra-character gap (between dits/dahs in a letter) = **1T**
- Inter-character gap (between letters) = **3T**
- Inter-word gap (between words) = **7T**

If you can keep these ratios consistent, decoding works even if the absolute speed changes.

## Why Morse Belongs in This Handbook
Morse is a **bridge** between:

- high-tech encoding (binary / QR slates)
- low-tech signaling (beeps/flash/tap)

In a collapse scenario, Morse can still transmit:
- identifiers
- coordinates
- short messages
- “beacon pings” that confirm continuity

## Notebook Entry
Record a baseline you can reproduce:

- Your chosen unit time (T) in milliseconds (or approximate “count”)
- Your chosen training speed (slow/medium/fast)
- Any decoding mistakes you made today

## Next
Proceed to the decoder table:

- **TT-332 — Morse Decoder (Full Character Set)**
