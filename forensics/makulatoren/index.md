+++
title = 'Makulatoren'
categories = ['forensics']
date = 2025-12-01T11:36:57+01:00
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

1.  **Initial Analysis**:
    *   Files were analyzed using `file`, `ls -l`, `xxd`, `head`, and `tail` to identify potential JPEG headers and footers.
    *   File `19` was identified as the start of the JPEG (`FF D8`).
    *   File `15` was identified as the end of the JPEG (`FF D9`).
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

