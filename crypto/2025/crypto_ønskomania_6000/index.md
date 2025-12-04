+++
title = 'Ønskomania 6000'
categories = ['Crypto']
date = 2025-12-02T10:03:59+01:00
scrollToTop = true
+++


## Challenge Name:

Ønskomania 6000

## Category:

Crypto

## Challenge Description:

Julemanden har ansat det nyeste IT-firma i byen, BitNisse, i håb om at kunne uddelegere hele processen med at modtage ønsker fra alle verdens børn til én besked app. For at få alle børn til at bruge appen, har Julemanden lovet, at hvert ønske et barn sender til ham forøger deres chance for at få ekstra gaver!

Da deadline for appen var 1. december, blev den kryptografiske protokol lidt halvfærdig, og nogle kryptografer er bange for, at tekniske hackerbørn kan få deres ønske registreret flere gange.

Start server på TryHackMe og forbind med det udleverede client script eller direkte med
nc <IP> 1337

OBS: Opgaven åbner for en 2'er i serien, det er en af de skjulte under ???.

https://tryhackme.com/jr/oenskomania6000

Santa has hired a new IT company, BitNisse, to handle wishes via a new app. The protocol is "half-finished" and there's a concern that users can register their wishes multiple times. We are given the server source code, client source code, and keys. The goal is to exploit the protocol to register a wish multiple times.

## Approach

We analyzed [server.py](scripts/server.py) and [client.py](scripts/client.py).
The server uses a static Diffie-Hellman shared secret (derived from keys loaded from files) to derive session keys using a salt provided by the client.
The encryption is AES-GCM.

The server logic has a specific check for "repeated messages":
```python
        if last_message is None:
            print("🎄 Mange tak for dit første juleønske!")
        elif ciphertext == last_message:
            flag = Path("flag.txt")
            if flag.exists():
                print(flag.read_text().strip())
            # ...
            break
```
This logic explicitly releases the flag if the *exact same ciphertext* is received twice in a row (`ciphertext == last_message`).
While the prompt says "INGEN GENTAGELSER!" (No Repetitions), the code actually rewards it.

To exploit this, we simply needed to:
1.  Construct a valid encrypted wish message using the provided keys and the client logic.
2.  Send the wish to the server.
3.  Send the exact same wish (replay) immediately after.

We wrote a python script [solve_replay.py](scripts/solve_replay.py) that implements the client encryption (using the provided keys) and performs the replay attack.

## Flag

```text
NC3{Mag1c_c0py_p4st3}
```

## Reflections and Learnings

This challenge demonstrates a classic Replay Attack vulnerability. The server failed to enforce uniqueness or freshness (e.g., by checking nonces against a history or ensuring the message content hasn't been processed before in a way that prevents replays). Instead, the server logic specifically checked for a replay and released the flag, likely simulating a "debug" backdoor or a logic error where the condition for "detecting an attack" was wired to "reward the attacker". In a real secure system, a replay should be rejected (or ignored idempotent-ly) without side effects.
