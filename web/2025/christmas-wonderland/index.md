+++
title = 'Christmas Wonderland'
categories = ['Web']
date = 2025-12-05T20:16:22+01:00
scrollToTop = true
+++

## Challenge Name:

Christmas Wonderland

## Category:

Web

## Challenge Description:

Nisserne har dedikeret en hjemmeside til deres Wonderland. Besøg siden, nyd stemningen og måske kan du finde et flag.

https://tryhackme.com/jr/xmaswonderland

## Approach

The flag was constructed by piecing together information from various sources:
- **Flag Prefix:** `NC3{c0` was found by decoding `TkMze2Mw` in `{URL}/private/`.
- **Flag Middle part 1:** `zy_chr` was found by decoding `enlfY2hy` in `{URL}/index.html` (container class)
- **Flag Middle part 2:** `|stm@s` was found by decoding `fHN0bUBz` in `{URL}` (downloading a redirect html!)
- **Flag Suffix:** `_ctf_challenge}` was found by assembling the 3 javascripts in `{URL}/js/payloadA.js`, `{URL}/js/payloadB.js` & `{URL}/js/core.js`. Final script can be found [here](scripts/javascript.js)

The full base64
```bash
TkMze2Mw enlfY2hy fHN0bUBz X2N0Zl9j aGFsbGVu Z2V9

TkMze2MwenlfY2hyfHN0bUBzX2N0Zl9jaGFsbGVuZ2V9
```

## Flag

```text
NC3{c0zy_chr|stm@s_ctf_challenge}
```

## Reflections and Learnings
This challenge highlighted the importance of interpreting hints and context carefully when direct extraction of flag components is not straightforward. Sometimes, guessing based on strong contextual clues is necessary when faced with ambiguity in code obfuscation.
