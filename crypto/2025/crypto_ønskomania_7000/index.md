+++
title = 'Ønskomania 7000'
categories = ['Crypto']
date = 2025-12-02T10:04:59+01:00
scrollToTop = true
+++

## Challenge Name:

Ønskomania 7000

## Category:

Crypto

## Challenge Description:

Julemanden er ved at være træt af gentagelser! BitNisse har fået en opsang, og serveren er nu blevet smart nok til, at den kan stoppe gentagelser! Men måske ikke helt smart nok?

Start server på TryHackMe og forbind med det udleverede client script eller direkte med
nc <IP> 1337

https://tryhackme.com/jr/oensk0m4n1a7000

This is a follow-up to Ønskomania 6000. The server claims to stop repetitions.
The server introduces a "snowflake" check.

## Approach

We analyzed [server.py](scripts/server.py) and found the following logic:

```python
    # Inside santa_decrypt_wish
    counter = nonce[:8]
    encoded_int = int.from_bytes(counter[1:], "little")
    legit = (encoded_int >> 1) ^ -(encoded_int & 1) >= 0
    return ..., not legit

    # Inside main
    elif data == last_message:
        if snowflake:
            # Print flag
        else:
            print("🎅 Hohoho, prøver du nu at snyde igen?")
```

The server releases the flag only if we successfully replay a message (`data == last_message`) AND `snowflake` is True.
`snowflake` is True if `legit` is False.
`legit` is calculated using a ZigZag-like decoding check: `(n >> 1) ^ -(n & 1) >= 0`.
This expression evaluates to a non-negative number if `n` (the encoded integer) is even (decodes to positive).
It evaluates to a negative number if `n` is odd (decodes to negative).

So, to make `legit` False, we need `encoded_int` to be **odd**.
`encoded_int` is derived from the nonce: `int.from_bytes(nonce[1:8], "little")`.
To make this integer odd, we simply need the first byte of the slice (`nonce[1]`) to be odd.

We modified our client solver to manually construct a valid AES-GCM nonce where `nonce[1] = 1`.
We then encrypted a wish using this nonce, sent it, and immediately replayed it.
The server accepted the replay as a "snowflake" (special/non-legit counter) and released the flag.

### Solver Script

The solver [script](scripts/solve_snowflake.py) sets up the crypto keys, manually constructs the nonce, and performs the replay attack.

```python
def aesgcm_encrypt_with_shared(key, plaintext, aad):
    aesgcm = AESGCM(key)
    # Manual nonce construction to force "snowflake"
    nonce = bytearray(12)
    nonce[1] = 1  # Force odd integer interpretation
    nonce = bytes(nonce)
    return nonce + aesgcm.encrypt(nonce, plaintext, aad)
```

We can now move on to the final chapter [Ønskomaten_v24_12](/nc3/crypto/2025/crypto_ønskomaten_v24_12)!

## Flag

```text
NC3{G0tt4_l0v3_z1g-z4g_3nc0d1ng}
```

## Reflections and Learnings

The challenge relied on a specific implementation detail of how the server validated the "counter" embedded in the nonce. By understanding the bitwise logic (`ZigZag` decoding property), we could manipulate the nonce (which is chosen by the client) to bypass the protection and trigger the "snowflake" condition required to get the flag during a replay.
