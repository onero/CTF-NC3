+++
title = 'Nissehalla'
categories = ['Reversing']
date = 2025-12-06T10:16:22+01:00
scrollToTop = true
+++

## Challenge Name:

Nissehalla

## Category:

Web

## Challenge Description:

Alle nisser drømmer om at få risengrød og gløgg i Nissehalla, find de to nøgler og luk porten op for de stakkels hungrende nisser.

Start server på TryHackMe og forbind med
nc <IP> 8080

https://tryhackme.com/jr/nissehalla2o25v1

## Approach

1.  **Reconnaissance**:
    - [Scanning](https://github.com/bee-san/RustScan) the target IP revealed port 8080 was open.
    - Visiting `http://10.82.175.234:8080` showed a "Nissehalla" access page with a form requiring two files (`fileA` and `fileB`).

2.  **Exploitation**:
    - I attempted to upload two simple text files with slightly different content:
        - `fileA`: "test content 1"
        - `fileB`: "test content 2"
    - The server response indicated a "Truncated hash" and "Collision detected!".
    - It seems the server compares the hashes of the two files, but truncates them significantly (likely to 6 bytes/48 bits based on the output `0xa360b6409474`).
    - By pure chance (or because the hash function is extremely weak/non-cryptographic), these two inputs resulted in the same truncated hash.
    - The server returned the flag.

## Flag

```text
NC3{!H45H_colLi5ION_m45T3R_2025!}
```

## Reflections and Learnings
- Sometimes "random" testing works instantly.
- Truncated hashes drastically reduce collision resistance.
