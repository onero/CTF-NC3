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

The challenge provided 21 shredded pieces of a JPEG image. The goal was to reassemble them to reveal the flag.

1.  **Initial Analysis - Identifying the Start and End**:

  JPEG files have specific "Magic Bytes" that mark their beginning and end.
    * Start of Image (SOI): FF D8
    * End of Image (EOI): FF D9
    * Since the image was shredded, one file should start with FF D8, and one file should end with FF D9
    *   Files were analyzed using `file`, `ls -l`, `xxd`, `head`, and `tail` to identify potential JPEG headers and footers.

We search for the first octets with
```bash
xxd -l 2 -p {IMAGE}
```
Where [xxd](https://linux.die.net/man/1/xxd) creates a hex dump, `-l 2` stops processing after reading 2 octets and -p outputs in "plain" hexdump style (no line numbers of ASCII)

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

    *   File `19` was identified as the start of the JPEG (`FF D8`).
    *   File `15` was identified as the end of the JPEG (`FF D9`).
    *   So our chain starts: 19 -> ... -> 15
    *   Now we need to find what comes after File 19. 
    *   Since the image was shredded (split), the bytes at the end of File 19 flow directly into the start of the next file. 
    *   File 19 likely contains the image header (metadata). 
    *   We'll inspect it to see if it cuts off in the middle of a known text string or structure. This is
  often the easiest way to find the next piece manually.
    *   Through byte-level matching of known JPEG metadata structures (e.g., `bplist`, `xmpmeta`), an initial chain `19 -> 3 -> 11` was established as the header block.
    *   `djpeg -v` confirmed image dimensions (3012x1923) were read after these initial pieces.

2.  **Iterative Reassembly and OCR for Flag Reconstruction**:
    *   A greedy search algorithm was employed, using `djpeg` for stream validation and `tesseract` for OCR on partial image concatenations.
    *   The primary goal was to find a chain that clearly spells out the flag, informed by user hints about its content.
    *   The phrase "Samler du billedet som du samler pokemon kort, så kommer flaget" (Collect the image like you collect Pokémon cards, then the flag will come) was a crucial hint, implying the numerical order of the files was significant. However, simple numerical ordering did not work.
    *   By carefully examining OCR output from various combinations, the most coherent sequence for the flag was derived. This involved identifying "NC3{", "Pokemonkort i", "2025 er", and "nostalgisk" across different image fragments.
    *   The key fragments were located in files `21`, `13`, `4`, `14`, `17`.

3.  **Final Reconstructed Chain**:
    *   The final chain derived was `[19, 3, 11, 21, 13, 4, 14, 17, 15]`. This sequence best reconstructs the text elements of the flag based on OCR and user hints. OCR on this final image, combined with user input, confirmed the full flag.

## Flag

```text
NC3{Pokemonkort_i_2025_er_nostalgisk}
```

## Reflections and Learnings
*   Reassembling shredded JPEG byte streams is challenging due to OCR noise and the forgiving nature of JPEG decoders.
*   User hints and specific target phrases are invaluable for guiding the reconstruction process when automated methods are inconclusive.
*   Iterative testing with OCR and careful interpretation of garbled text is essential.

