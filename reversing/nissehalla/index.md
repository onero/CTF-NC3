+++
title = 'Nissehalla'
categories = ['Reversing']
date = 2025-12-06T10:16:22+01:00
scrollToTop = true
+++

## Challenge Name:

Nissehalla

## Category:

Reversing

## Challenge Description:

Alle nisser drømmer om at få risengrød og gløgg i Nissehalla, find de to nøgler og luk porten op for de stakkels hungrende nisser.

Start server på TryHackMe og forbind med
nc <IP> 8080

https://tryhackme.com/jr/nissehalla2o25v1

## Approach

1.  **Reconnaissance**:
    - [Scanning](https://github.com/bee-san/RustScan) the target IP revealed port 8080 was open.
    - Visiting `http://10.82.175.234:8080` showed a "Nissehalla" access page with a form requiring two files (`fileA` and `fileB`).
    ![nissehalla](images/home.png)

2.  **Reverse Engineering**:
    - Analyzing the binary provided, in `objdump` / Ghidra revealed a custom hash function `weird_hash64`.
    - The hash function initializes a state and processes the input buffer.
    - Crucially, it processes the buffer by visiting indices in a pseudo-random order determined by a linear congruential generator (LCG)-like update: `step = ((5 * step + 3) & 7) + 1`.
    - The loop condition `test r13b, 0x3` controls an inner processing loop.
    - Maybe for certain file lengths, the traversal logic might *miss* some indices completely.

3.  **Vulnerability Analysis**:
    - I then wrote the script [solve_collision.py](scripts/solve_collision.py) to simulate the index visitation logic of the hash function.
    - The script checked lengths from 10 to 300.
    - It discovered that for **length 10**, the hash function *never reads* the bytes at indices **3, 7, 8, and 9**.
    - This means any changes to these bytes **do not affect the resulting hash**.

4.  **Exploitation**:
    - We generated two files of length 10:
        - [coll_a](scripts/coll_a): 10 bytes of 'A's.
        - [coll_b](scripts/coll_b): 10 bytes of 'A's, but index 3 changed to 'B'!
    - Since index 3 is unused, `Hash(coll_a) == Hash(coll_b)`.
    - We uploaded these files to the web service.
    - The server confirmed the collision and returned the flag.

## Flag

```text
NC3{!H45H_colLi5ION_m45T3R_2025!}
```

## Reflections and Learnings
- **Static Analysis pays off:** Ghidra and static analysis is hard... But instead of blindly fuzzing, understanding the code revealed a deterministic flaw.
- **Coverage matters:** The hash function failed to process the entire input for certain lengths, violating a core property of secure hashing.
- **Side Note:** The "Truncated hash" output from the server hinted at weakness, but the real flaw was in the *input processing* logic (skipping bytes) rather than just the output size.
