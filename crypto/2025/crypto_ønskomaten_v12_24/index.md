+++
title = 'Ønskomaten v12.24'
categories = ['Crypto']
date = 2025-12-02T17:12:45+01:00
scrollToTop = true
+++

## Challenge Name:

Ønskomaten v12.24

## Category:

Crypto

## Challenge Description:
Hele Nisseland er blevet underlagt det nye NISS3-direktiv, der stiller nye krav til datasikkerheden. Som følge heraf skal alle juleønsker nu krypteres inden afsendelse til Julemandens postkontor.

Nissitaliseringsstyrelsen har valgt Niscompany som vinder af udbuddet om at udvikle og implementere en løsning, og de blev på rekordtid klar med Ønskomaten v12.24 - men gik det mon lidt for hurtigt?

Start server på TryHackMe og forbind med
nc <IP> 1337

OBS: Opgaven åbner for en 2'er i serien, det er en af de skjulte under ???.

https://tryhackme.com/jr/onskomatv1224

We are presented with a "Wish Automaton" (Ønskomaten) running on a TCP server. We are provided with the source code [ønskomaten_v12_24.py](scripts/ønskomaten_v12_24.py). The service encrypts user input (wishes) using RSA. It displays the public key parameters $N$ and $e=3$.

The source code reveals how the flag is hidden:
```python
# Julemandens hemmelige ønskeforstærkere
mid = len(flag) // 2
a = int.from_bytes(flag[:mid])
b = int.from_bytes(flag[mid:])

# ... loop ...
m = int.from_bytes(wish.encode("latin-1"))
c = encrypt(a * m + b)
```
The encryption is performed as $c = (a \cdot m + b)^e \pmod N$.
We can interact with the service to send arbitrary wishes $m$ and receive the corresponding ciphertext $c$.

## Approach

The public exponent $e=3$ is very small. This often hints at attacks involving small message sizes or lack of padding.

We can model the encryption as:
$c = (a \cdot m + b)^3 \pmod N$

We can send two chosen messages, for example, the characters '1' and '2'.
In ASCII/Latin-1:
- '1' is 49.
- '2' is 50.

So we send $m_1 = 49$ and $m_2 = 50$ to get:
1. $c_1 = (49a + b)^3 \pmod N$
2. $c_2 = (50a + b)^3 \pmod N$

Let $v_1 = 49a + b$ and $v_2 = 50a + b$.
The values $v_1$ and $v_2$ might be small enough that $v_1^3 < N$ and $v_2^3 < N$. If so, the modular reduction never happens (or happens very few times), and we can simply take the integer cube root of $c_1$ and $c_2$ to recover $v_1$ and $v_2$.

We verified this hypothesis by taking the integer cube root of the received ciphertexts. They were indeed perfect cubes.

Having recovered $v_1$ and $v_2$, we have a system of two linear equations:
1. $v_1 = 49a + b$
2. $v_2 = 50a + b$

Subtracting (1) from (2):
$v_2 - v_1 = (50a + b) - (49a + b) = a$

Once we have $a$, we can find $b$:
$b = v_1 - 49a$

Finally, we convert the integers $a$ and $b$ back to bytes and concatenate them to form the flag.

Final solving script can be seen [here](scripts/solve.py)

We can now move on to [Ønskomania 6000](/nc3/crypto/2025/crypto_ønskomania_6000)!

## Flag

```text
NC3{f4st_cub3r00t_d3crypt10n_1s_4_f34tur3_n07_4_bug}
```

## Reflections and Learnings

The challenge highlights the dangers of using small public exponents ($e=3$) without proper padding (like OAEP). Even though the message was transformed ($a \cdot m + b$), the linearity of the transformation combined with the ability to choose $m$ and the small exponent allowed us to treat the RSA encryption as a simple polynomial equation over the integers rather than a modular one. This is a variant of the "Low Public Exponent Attack".
