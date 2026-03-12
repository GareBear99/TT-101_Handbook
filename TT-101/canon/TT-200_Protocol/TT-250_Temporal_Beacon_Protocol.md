# TT-250 — Temporal Beacon Protocol

A **Temporal Beacon** is a *publicly verifiable, low-interference marker* placed in history so that any hypothetical future observer can:
- locate the same pivot window,
- verify integrity via hashes,
- interpret non-response conservatively.

This is **not** established physics. It is a disciplined signaling + archive layer that remains useful even if time travel is impossible.

## Beacon record (minimum fields)
1) Beacon ID
2) Publish timestamp (local + UTC)
3) Public mirror locations
4) Pivot Window reference
5) Observation Window
6) Listener Contract (response constraints)
7) Non-response interpretation

Template: [templates/Beacon-Entry.md](../../templates/Beacon-Entry.md)

## Listener Contract (safe default)
Allowed:
- signed acknowledgement of an existing public hash
- minimal public note referencing an integrity anchor
Not allowed:
- harm, coercion, destabilization
- disruptive “prove it by changing X” demands
- financial requests

## Non-response meaning
Non-response is ambiguous; it is not proof.
See: [docs/timeline_divergence.md](../../docs/timeline_divergence.md)
