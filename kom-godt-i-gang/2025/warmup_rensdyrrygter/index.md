+++
date = "2025-12-01"
title = "Rensdyrrygter"
categories = ['Kom godt i gang']
slug = "warmup_rensdyrrygter"
tags = ["CTF", "NC3", "Crypto", "Diffie-Hellman", "AES"]
author = "Onero"
+++

## Description
Springer og Lyn eeelsker at sladre til hinanden på Snissnap om de andre rensdyr, men nu vil Julemanden indføre chatkontrol og holde øje med dem. Men det er intet problem, de krypterer bare deres beskeder manuelt først for at omgå det.

Springer siger, de bare skal bruge "Diffie-Hellman" protokollen, og begge rensdyr har brugt et program til at danne et nøglepar. De har sendt deres offentlige nøgler til hinanden, og Springer er allerede begyndt at sende beskeder - men Lyn fatter altså stadig ikke, hvordan det virker.

```bash
Parametre
p: 0xAB359AA76A6773ED7A93B214DB0C25D0160817B8A893C001C761E198A3694509EBE87A5313E0349D95083E5412C9FC815BFD61F95DDECE43376550FDC624E92FF38A415783B97261204E05D65731BBA1CCFF0E84C8CD2097B75FECA1029261AE19A389A2E15D2939314B184AEF707B82EB94412065181D23E04BF065F4AC413F
g: 2
Lyns private nøgle: 0x486F762064752C20646574206865722065722062617265204C796E732070726976617465206B6579202D206875736B20696B6B652061742064656C652064656E206D6564206E6F67656E21
Lyns offentlige nøgle: 0x9A152AFABF57B00BDB6DD3E3AA68BCCB43628E6498F4357F9A89B13CEB0467C233DFCDDBD1BFF5C40AD1FE0663B0A5BB207DFA93BB8F6E0E1CAF78C674CF19636CD360A1C67B86CF45BC34C010FF37311ABF1F076A12F56C0E79906DE8BB1BE7B39CA981ED0D5C21C1402170E16A4BBD2A6FAB0F933F14DDE9F28EE599AB235C
Springers offentlige nøgle: 0x39E22730E9F0B9F9039A2FB9F1C665DA1A05717400682946BC445093C3DF8D6164C5319C37E5EF688D346CA46168EE025E0675756EB1CE63F84BAA3B159545159EE621498F23BE036BD0037201E35D01E1FAFFBBD3C5A5AA3152114870430CDE4A7B48A822A4478FD9C443CFBC73C328C152409D1223F7ACA502F736B15019DC
```


We were given a Python script [rensdyrrygter.py](scripts/rensdyrrygter.py) and an encrypted text file [skjult_sladder.txt](skjult_sladder.txt). 
The challenge description described a scenario where two reindeer, Springer and Lyn, were using the Diffie-Hellman protocol to encrypt their messages to avoid "chat control".

We were provided with:
*   A large prime modulus `p`
*   A generator `g = 2`
*   Lyn's private key
*   Springer's public key

## Recon
The `rensdyrrygter.py` script outlined the decryption process:
1.  Calculate the Shared Secret using Diffie-Hellman.
2.  Derive an AES key by hashing the shared secret with SHA-256.
3.  Decrypt the messages in `skjult_sladder.txt` using AES in ECB mode.

## Solution
I implemented a [Python solver script](scripts/solve_rensdyr.py) to calculate the shared secret:
`Shared Secret = (Springer's Public Key ^ Lyn's Private Key) mod p`

Using Python's `pow(springer_pub, lyn_priv, p)`, we computed this large integer.

I then used `hashlib` to create the AES key:
`key = hashlib.sha256(long_to_bytes(shared_secret)).digest()`

Finally, I used `pycryptodome` to decrypt the lines in `skjult_sladder.txt`.

One of the decrypted messages contained the flag.

## Flag
`NC3{n0_w4y_h0rt3_l1g3_t0_n1ss3r_sn4kk3_0m_d3_l4v3r_4lt_d3r3s_l3g3t0j_m3d_AI_s3lv0m_Jull3_h4r_f0rbudt_d3t}`
