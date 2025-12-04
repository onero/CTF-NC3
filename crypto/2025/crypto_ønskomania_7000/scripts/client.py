import os
import json
import sys
from pathlib import Path

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from pwn import *

from helpers import thrift_encode_int


context.log_level = 'error'

# Generate shared secret:
santa_public_key = serialization.load_pem_public_key(
    Path("keys/santa_public_key.pem").read_bytes()
)

hacker_private_key = serialization.load_pem_private_key(
    Path("keys/hacker_private_key.pem").read_bytes(),
    password=None
)

shared_secret = hacker_private_key.exchange(santa_public_key)
assert isinstance(shared_secret, bytes), "Shared secret skal være bytes"
assert len(shared_secret) == 32, f"Shared secret skal være 32 bytes, fik {len(shared_secret)}"

# Sizes
AES_KEY_LEN = 32   # 256-bit AES key
GCM_NONCE_LEN = 12
HKDF_SALT_LEN = 16


def derive_aes_key(shared_secret: bytes, salt: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
    )
    return hkdf.derive(shared_secret)


def aesgcm_encrypt_with_shared(
    key: bytes,
    plaintext: bytes,
    aad: bytes | None = None
) -> bytes: # Returns: salt(16) || nonce(12) || ciphertext||tag
    aesgcm = AESGCM(key)
    
    counter_file = Path("nonce_local_to_julemanden.txt")
    try:
        counter = int(counter_file.read_text())
    except (FileNotFoundError, ValueError):
        counter = 1
    counter_file.write_text(str(counter + 1))

    encoded_counter = thrift_encode_int(counter)   
    counter_bytes = encoded_counter.ljust(8, b"\x00")[:8]
    random_tail = os.urandom(4)

    nonce = counter_bytes + random_tail
    assert len(nonce) == 12

    ct_and_tag = aesgcm.encrypt(nonce, plaintext, aad)

    return nonce + ct_and_tag


def aesgcm_decrypt_with_shared(
    key: bytes, 
    blob: bytes,
    aad: bytes | None = None
) -> bytes:
    if len(blob) < GCM_NONCE_LEN + 16:  # minimal sanity: nonce + tag
        raise ValueError("ciphertext blob for kort")

    aesgcm = AESGCM(key)
    nonce = blob[:GCM_NONCE_LEN]
    ct_and_tag = blob[GCM_NONCE_LEN:]
    return aesgcm.decrypt(nonce, ct_and_tag, aad)                      


def encrypt_wish_for_santa(wish: str):
    SantaID = 1

    plaintext = bytearray(wish.encode())
    aad_struct = {
        "to_": SantaID
    }
    aad = bytearray(json.dumps(aad_struct, separators=(',', ':')).encode())
    aad_len_bytes = len(aad).to_bytes(2, "big")
    salt = os.urandom(16)
    key = derive_aes_key(shared_secret, salt)
    encrypted = aesgcm_encrypt_with_shared(key, plaintext, aad)
    final_message = aad_len_bytes + aad + salt + encrypted
    
    return final_message


def main():
    HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    with remote(HOST, 1337) as io:
        print(io.recvline().decode())

        while True:
            try:
                wish = input("🎁 Juleønske: ").strip()
            except KeyboardInterrupt:
                print("👋 Farvel!")
                break

            if wish:
                ct = encrypt_wish_for_santa(wish)
                io.sendlineafter(b"> ", ct.hex().encode())
                response = io.recvline().decode()
                print(response)
            else:
                io.sendlineafter(b"> ", b"")
                print(io.recvline().decode())
                break


if __name__ == "__main__":
    main()
