+++ title = 'Ønskomaten v24.12'
categories = ['Crypto']
date = 2025-12-03T06:50:08+01:00
scrollToTop = true
+++

## Challenge Name:

Ønskomaten v24.12

## Category:

Crypto

## Challenge Description:

Godt fundet - den kritiske sårbarhed i Ønskomaten v12.24 er nu lukket! Niscompany har udrullet en opdateret version: v24.12:

PATCH NOTES

🔐 Sikkerhed: Beskeder paddes nu til minimum 16 bytes for at forhindre det tidligere angreb.
🌐 Kompatibilitet: Fuld understøttelse af Unicode, så alle verdens børn kan sende ønsker på eget sprog (메리 크리스마스) og vigtigere med emojis (🎄💥).
⚡ Performance: Krypteringspipeline optimeret - hastighed øget ~300% efter massiv investering i Monster til krypteringsnisserne.
Start server på TryHackMe og forbind med
nc <IP> 1337

https://tryhackme.com/jr/onskomatenv2412

[This](scripts/ønskomaten_v24_12.py) is a patched version of the previous Ønskomaten challenge. The changes include:
- Padding messages to 16 bytes.
- Support for Unicode/Emojis.
- "Optimized" encryption pipeline.

The encryption logic is:
```python
m = int.from_bytes(pad(wish))
c = encrypt(a * m + b)
```
where `pad(m)` ensures the message is at least 16 bytes. $N$ and $e=3$ are provided.

## Approach

Although the message $m$ is now larger (due to padding), the transformation is still linear: $M = a \cdot m + b$.
The encryption is $c = (a \cdot m + b)^3 \pmod N$.

We can rewrite this as a polynomial in terms of the unknown coefficients $a$ and $b$:
$(am + b)^3 = a^3 m^3 + 3a^2b m^2 + 3ab^2 m + b^3 \pmod N$.

We can control $m$ by sending different wishes. Let $X = a^3, Y = a^2b, Z = ab^2, W = b^3$.
Then for each message $m_i$, we have a linear equation:
$m_i^3 X + 3m_i^2 Y + 3m_i Z + W = c_i \pmod N$.

Since there are 4 unknowns ($X, Y, Z, W$), we need 4 linearly independent equations. We can obtain these by sending 4 different wishes (e.g., "1", "2", "3", "4").

After solving the linear system for $X$ (which is $a^3$) and $W$ (which is $b^3$), we can recover $a$ and $b$ by taking the integer cube root. This works because $a$ and $b$ are derived from the flag and are small enough such that $a^3 < N$ and $b^3 < N$ (or at least, the modular reduction doesn't destroy the ability to recover them via roots, especially if $N$ is large enough compared to the flag size).

### Solver Script

The [solver](scripts/solve_final.py) implements the following steps:
1.  Connect to the server and parse $N$.
2.  Send 4 distinct wishes ("1", "2", "3", "4") and record the ciphertexts.
3.  Calculate the corresponding padded integer values $m_1, m_2, m_3, m_4$.
4.  Construct a $4 \times 4$ matrix where each row $i$ is $[m_i^3, 3m_i^2, 3m_i, 1]$ and the target vector is $[c_1, c_2, c_3, c_4]$.
5.  Solve the linear system modulo $N$ using Gaussian elimination.
6.  Extract $a^3$ and $b^3$ from the solution vector.
7.  Compute the integer cube roots to find $a$ and $b$.
8.  Convert $a$ and $b$ to bytes and concatenate them to reveal the flag.

## Flag

```text
NC3{fr4nkl1n_4nd_r31t3rs_m3ss4g3s_4r3_s0_r3l4t4bl3_m4n!}
```

## Reflections and Learnings

This challenge demonstrates that adding linear padding or simple linear transformations does not protect RSA with small exponents against linearization attacks. If the relationship between the plaintext and the ciphertext can be expressed as a system of linear equations with a small number of unknowns, the system can be solved efficiently. The "patch" failed to address the underlying vulnerability of using a small exponent with a linear relation.
