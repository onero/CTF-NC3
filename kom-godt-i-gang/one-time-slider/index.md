+++
title = 'One Time Slider'
categories = ['Kom godt i gang']
date = 2023-12-01T10:05:14+01:00
+++

## Challenge Name:

One Time Slider

## Category:

kom godt i gang

## Challenge Description:

Kryptonissen har læst op på One Time Pads og er kommet frem til en endnu mere sikker kryptering:

Hvis man nu slider en OTP henover hele ciphertexten, bliver hver plaintext byte krypteret mange gange - det må være bedre end én!

Han har krypteret en besked til dig:

```bash
e9e494dcd1c2c9d3f8d1c6d5f8c3c2d3f8c3d2cad3f8c6d3f8ffe8f5f8c6cbcbc2f8c5ded3c2d4f8cac2c3f8cfd1c2d5f8ccc2def8c5ded3c2989898da
```

[onetimeslider.py](scripts/onetimeslider.py)

## Approach

The Kryptonite has heard about One Time Pads (OTPs) and devised his own little smart encryption method, building upon it in an attempt to improve security. However, he hasn't studied enough! An OTP is a key of completely random bytes, the same length as the message to be encrypted. It should only be used once, hence the name.

An OTP provides real perfect encryption but is not practical because a key as long as the message needs to be generated, secretly distributed to the recipient, and never reused.

But what has the Kryptonite done? Well, the Kryptonite has generated an OTP and then "slid" it over the message's bytes, as illustrated here with 4 bytes (bX are message bytes and kX are key bytes):

```bash
k0 k1 k2 k3 ->
         b0 b1 b2 b3

   k0 k1 k2 k3 ->
         b0 b1 b2 b3

      k0 k1 k2 k3 ->
         b0 b1 b2 b3

         k0 k1 k2 k3 ->
         b0 b1 b2 b3

            k0 k1 k2 k3 ->
         b0 b1 b2 b3

               k0 k1 k2 k3 ->
         b0 b1 b2 b3

                  k0 k1 k2 k3 ->
         b0 b1 b2 b3
```

For each position, all message bytes are encrypted with a simple XOR with the key byte currently slid over it.

What does this mean in practice? Well, it means that all bytes in the message have been XORed with all bytes in the key. This implies that every single byte in the message is encrypted with the same key byte, namely k1 ^ k2 ^ ... ^ kN.

Therefore, we can just try all 256 possible byte values as the key and see if we get something that resembles a flag! Or we can be even smarter: We know the first bytes, NC3{, and since ct = pt ^ key, it also holds that key = pt ^ ct, so we can just XOR the first 4 bytes of the encrypted text with NC3{:

```python
import secrets

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

hex_message = "e9e494dcd1c2c9d3f8d1c6d5f8c3c2d3f8c3d2cad3f8c6d3f8ffe8f5f8c6cbcbc2f8c5ded3c2d4f8cac2c3f8cfd1c2d5f8ccc2def8c5ded3c2989898da"
encrypted_message = bytes.fromhex(hex_message)

n = len(encrypted_message)
otp = secrets.token_bytes(n)

# Convert bytes to a list of integers
encrypted_list = list(encrypted_message)

# Slide OTP over ciphertext and XOR decrypt everything within its range
for i in range(2 * n + 1):
    encrypted_list[max(0, i - n):i] = xor(encrypted_list[max(0, i - n):i], otp[-i:])

# Convert the list of integers back to bytes
decrypted_message = bytes(encrypted_list)

print(decrypted_message.decode('utf-8'))

with open("decrypted_message.txt", "wb") as f:
    f.write(decrypted_message)

```

[Download script](scripts/solve-slider.py)

## Flag

```text
NC3{wait_was_it_dumb_to_XOR_all_bytes_with_each_key_byte???}
```

## Reflections and Learnings

Here are some key reflections and learnings from this challenge:

### The Essence of OTP:

One Time Pads (OTPs) are celebrated for their theoretical unbreakability when used correctly.
This challenge serves as a reminder that the strength of OTP lies in the randomness of the key and its single use. Any deviation from this principle, such as the Kryptonite's method of sliding the OTP across the ciphertext, undermines its security.

### Practicality vs. Security:

The Kryptonite's intention to enhance security by repeatedly encrypting each byte with multiple key bytes highlights a common dilemma in cryptography - balancing security with practicality. While this method appears to increase security, it actually introduces patterns that can be exploited, as demonstrated in the decryption process.

### Importance of Key Management:

This challenge reiterates the importance of key management in cryptography. The original principles of OTP - randomness, equal length to the plaintext, and never reusing the key - are fundamental. The Kryptonite’s attempt to reuse key bytes for multiple plaintext bytes violates the principle of not reusing the key, leading to vulnerabilities.

### XOR Vulnerabilities:

XOR is a simple yet powerful operation used in many cryptographic algorithms. However, this challenge illustrates that improper use of XOR, especially in a predictable manner like sliding across the ciphertext, can lead to easy reversibility of the encryption, thus compromising security.

### Algorithm Transparency vs. Security:

The Kryptonite's attempt at modifying the OTP method underscores that transparency in cryptographic algorithms does not inherently compromise security. It's the improper implementation of these algorithms that leads to vulnerabilities. Well-established cryptographic methods are often open and have undergone rigorous testing and scrutiny, which contributes to their reliability.
