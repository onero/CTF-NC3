+++
title = 'Makulatoren'
categories = ['forensics']
date = 2025-12-05T10:00:57+01:00
scrollToTop = true
+++

## Challenge Name:

Makulatoren

## Category:

forensics

## Challenge Description:

Nistrid havde gemt et billede af sin Pokémonsamling og holdt det kært. En aften havde Nissen, ja ham drillenissen I alle kender, stjålet billedet og kommet det i julemakulatoren.

Stakkels Nistrid, der nu prøver at samle resterne, men det er ikke nemt uden hjælp.

## Approach

### Initial metadata analysis aka. finding the beginning and the end
- Overview: We received 21 shredded JPEG fragments. The goal was to rebuild the image and extract the flag.

JPEG files have specific "Magic Bytes" that mark their beginning and end.
- Step 1 — Identify Start of and end of image (SOI/EOI): JPEGs start with `FF D8` (SOI) and end with `FF D9` (EOI). Using this on each fragment
```bash
xxd -l 2 -p {IMAGE}
```
Where [xxd](https://linux.die.net/man/1/xxd) creates a hex dump, `-l 2` stops processing after reading 2 octets and -p outputs in "plain" hexdump style (no line numbers of ASCII)

The output
```bash
 --- HEADERS ---
File 1: 430b
File 2: 8171
File 3: 6c69
File 4: 29e4
File 5: 8ca8
File 6: 3c98
File 7: 2be0
File 8: 0206
File 9: b568
File 10: 0a7b
File 11: 6574
File 12: c876
File 13: 3e95
File 14: 1a87
File 15: 1685
File 16: 0382
File 17: 0335
File 18: 7c2c
File 19: ffd8
File 20: 63a7
File 21: 38ad
 --- FOOTERS ---
File 1: 13b4
File 2: 7fc5
File 3: 706d
File 4: 0923
File 5: e2ee
File 6: b270
File 7: ba7b
File 8: 7a80
File 9: 8ca2
File 10: 05f5
File 11: ea7d
File 12: a672
File 13: 2324
File 14: 73ee
File 15: ffd9
File 16: 9270
File 17: aa6e
File 18: 07a7
File 19: 6270
File 20: b5a0
File 21: 09f0
```

We find
  - File `19`: `ffd8` → Start of Image (SOI)
  - File `15`: `ffd9` → End of Image (EOI)
  - Chain anchors: `19 → ... → 15`
  - Now we need to find what comes after File 19. 
  - Since the image was shredded (split), the bytes at the end of File 19 flow directly into the start of the next file. 
  - File 19 likely contains the image header (metadata). 
  - We'll inspect it to see if it cuts off in the middle of a known text string or structure. This is
  often the easiest way to find the next piece manually.

### String analysis to fill out the entire sequence

- Step 2 — Establish continuity: Match cut strings across fragment boundaries to find neighbors.
  - `19` ends with `bp`; `3` starts with `list` → `bplist` (Apple Property List)
  - `3` ends with `xmpm`; `11` starts with `eta>` → `xmpmeta>` (XMP Metadata)
  - Solid start: `19 → 3 → 11`


### Trial & Error... lots of errors
  - From here on it was A LOT of trial and error with the sequence, throughout which we also got some "Du er tæt på flaget" = "You are closed to the flag"...
  - I finally got the flag with the following sequence
  - Final sequence: `19 → 3 → 11 → 21 → 13 → 4 → 14 → 17 → 15` ![solution](images/solution.jpg)
  - The pythong script for assembling the picture can be found [here](scripts/solve_makulatoren.py)
  - I tried embedding OCR scanning (to programmatically track progress), but ultimately found it much faster and more reliable to simply look at the images as they were assembled!

## Flag

```text
NC3{Pokemonkort_i_2025_er_nostalgisk}
```

## Reflections and Learnings
-
- JPEG forensics: SOI/EOI identification quickly anchors start/end fragments.
- Continuity cues: Split strings (e.g., `bplist`, `xmpmeta>`) are reliable neighbor indicators.
- OCR iteration: Enhance images (invert/contrast) and iterate until coherent phrases emerge.
- Hints matter: Use contextual clues to prioritize promising sequences.

