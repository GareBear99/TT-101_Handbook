# Archive Base Protocol

Goal: Create a resilient, redundant information base that survives drift and enables reconstruction of intent.

## Layers
1. **Public layer (decoy / lore)**
   - Explains the project at a high level.
   - Contains no sensitive personal authentication material.

2. **Core layer (private)**
   - Handshake phrase seed (sealed)
   - Pivot window worksheet
   - Minimal-impact message budget
   - A “future contact” letter
   - Hash manifest of all files

## Storage strategy (recommended)
- Print core documents; seal; store in 2+ physical locations.
- Offline encrypted drive stored separately.
- Cloud mirror (private repo or encrypted blob storage).
- Optional: notarized hash list (public) to prove integrity without revealing content.

## Integrity
- Maintain `manifest/hashes.txt` with SHA-256 hashes.
- Append changes; never rewrite past entries.
