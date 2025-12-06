+++
date = "2025-12-01T10:21:26+01:00"
title = "Snissnap"
categories = ['Kom godt i gang']
tags = ["CTF", "NC3", "Crypto", "Encoding"]
author = "Onero"
+++

## Challenge Name:

Warmup: Snissnap

## Category:

Kom godt i gang

## Description

I 2025 er det slut med at sende breve. Post Nordpolen kan ikke klare det mere. De opfordrer til at bruge deres nye app Snissnap med ny ekstrem nissesikker kryptering. Så kan man snissnappe en besked og sende til Julemanden.

De interne alarmer gik på denne loggede besked. Hvorfor dog det? Er alle børn ikke artige når de skriver til julemanden?

We were given a file [snissnap_besked.txt](snissnap_besked.txt) containing a sequence of hexadecimal values. The challenge description hinted at a "Warmup" task.

## Recon

The file content looked like this:
`MWEgMDQgNGQgMDQgNDAgMDQgMzUgMDQgMjAgMDAgMmUgMDQg...`

This appeared to be base64 encoded data. [Decoding the base64](https://gchq.github.io/CyberChef/) revealed a sequence of hex bytes:
`1a 04 4d 04 40 04 ...`

Analyzing the hex bytes, we noticed a pattern of `XX 04` and `YY 00`, which strongly suggested [UTF-16 Little Endian encoding](https://en.wikipedia.org/wiki/UTF-16), where `04` is the high byte for Cyrillic characters and `00` is for Basic Latin.

## Solution

We decoded the hex string as UTF-16LE, which produced the following text in Cyrillic:

> Кэре Юлеман.
> мит навн р Нисся.
> ...
> НC3{юл*мэд*кыриллиск}

The text was phonetically Danish written in Cyrillic characters (e.g., "Кэре Юлеман" = "Kære Julemand"). The hint "Husk at danskere kun kan læse latin" (Remember that Danes can only read Latin) instructed us to transliterate the Cyrillic back to the Latin alphabet.

The flag part `НC3{юл_мэд_кыриллиск}` transliterated to `NC3{jul_med_kyrillisk}`.

We verified this by checking the MD5 hash provided in the decoded text: `838b3074845c0140971dab8a815e1480`.

## Flag

`NC3{jul_med_kyrillisk}`
