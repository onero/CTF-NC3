+++
title = 'Julemandens Gåde'
categories = ['Web']
date = 2025-12-05T14:24:47+01:00
scrollToTop = true
+++

## Challenge Name:

Julemandens Gåde

## Category:

Web

## Challenge Description:

Træd ind i julemandens gemakker og få dit største ønske opfyldt, men først skal du løse julemandens gåde.

https://tryhackme.com/jr/julemandensgaadeNC3CTF2o25

## Approach

The challenge was a PHP type juggling puzzle disguised as a number guessing game.
After finding the base number `24` via brute-force, the server revealed constraints:
1.  Must loose-equal 24.
2.  Must not strictly-equal 24.
3.  Must not start with '2'.
4.  Must not end with '4'.

The payload `024.0` satisfied all conditions.

## Flag

```text
NC3{Xm45_PhP_JUgGL1Ng_m3rry_2025}
```

## Reflections and Learnings
Classic PHP type juggling. Always check edge cases in input validation (floating point representations, leading/trailing zeros).