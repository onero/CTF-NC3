+++
title = 'Julekortet'
categories = ['Reversing']
date = 2025-12-06T10:10:22+01:00
scrollToTop = true
+++

## Challenge Name:

Julekortet

## Category:

Reversing

## Challenge Description:

Jeg har fået sådan et smart e-julekort af mit barnebarn, men jeg tror han nisser rundt med mig, fordi jeg ikke er så teknisk. Jeg kan altså ikke finde ud af, hvad der står i, og hvor det bliver skrevet, kan du ikke hjælpe en gammel nisse lidt?

## Approach

1.  **Initial Analysis**: `file` identified the binary as a 32-bit Windows PE executable. `strings` revealed interesting messages like "Det lykkedes ikke at skrive julekortet" (Failed to write the Christmas card) and references to `WriteProcessMemory`, implying process injection.
2.  **Static Analysis**:
    - Disassembled the binary using `radare2`.
    - Located the `main` function and identified the call to `WriteProcessMemory`.
    - Analyzed the arguments to `WriteProcessMemory` and traced the source buffer `lpBuffer`.
    - Found a decryption loop immediately preceding the write operation, which XORed a stack buffer with `0x80`.
    - Traced the initialization of this stack buffer to a `rep movsd` instruction copying 34 bytes from the `.rdata` section (VA `0x46de5c`).
3.  **Extraction & Decryption**:
    - Calculated the file offset for the data at VA `0x46de5c` (Offset `0x6cc5c`).
    - Extracted the 34 bytes using `dd`.
    - Decrypted the bytes using Python: `print(''.join([chr(b ^ 0x80) for b in data]))`.
    - The result was the flag.

## Flag

```text
NC3{Julekort_i_naboens_postkasse}
```

## Reflections and Learnings
- Start with static inspection (file type, headers, strings, entropy) before dynamic work; this builds quick intuition about format and likely obfuscation!
- Identify file/container boundaries and metadata early; understanding format structures (headers, segments) prevents dead ends.