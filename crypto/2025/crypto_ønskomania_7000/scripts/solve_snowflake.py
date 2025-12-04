import socket
import os
import json
import sys
from pathlib import Path
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization

# ---- CRYPTO SETUP ----

KEYS_DIR = Path("keys")
SANTA_PUB_KEY_PATH = KEYS_DIR / "santa_public_key.pem"
HACKER_PRIV_KEY_PATH = KEYS_DIR / "hacker_private_key.pem"

if not SANTA_PUB_KEY_PATH.exists():
    print(f"Error: {SANTA_PUB_KEY_PATH} not found.")
    # Try absolute path fallback if running from root
    base = Path("loot/Crypto/crypto_ønskomania_7000")
    SANTA_PUB_KEY_PATH = base / "keys/santa_public_key.pem"
    HACKER_PRIV_KEY_PATH = base / "keys/hacker_private_key.pem"
    
    if not SANTA_PUB_KEY_PATH.exists():
        print("Could not find keys.")
        sys.exit(1)

santa_public_key = serialization.load_pem_public_key(
    SANTA_PUB_KEY_PATH.read_bytes()
)

hacker_private_key = serialization.load_pem_private_key(
    HACKER_PRIV_KEY_PATH.read_bytes(),
    password=None
)

shared_secret = hacker_private_key.exchange(santa_public_key)

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
    
    # WE NEED NONCE SUCH THAT:
    # counter = nonce[:8]
    # int.from_bytes(counter[1:], "little") IS ODD
    # So nonce[1] must be odd.
    
    # Let's construct a nonce manually.
    # byte 0 can be anything. byte 1 must be odd (e.g. 1).
    # rest can be anything.
    
    nonce = bytearray(12)
    nonce[1] = 1 
    # nonce is now 00 01 00 ... 00
    
    nonce = bytes(nonce)
    
    ct_and_tag = aesgcm.encrypt(nonce, plaintext, aad)

    return nonce + ct_and_tag

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

# ---- NETWORK ----

def recv_until(s, match_str):
    buffer = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            buffer += chunk
            print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
            if match_str.encode() in buffer:
                return buffer.decode('utf-8', errors='ignore')
        except socket.timeout:
            break
    return buffer.decode('utf-8', errors='ignore')

def solve():
    HOST = "10.82.130.242"
    PORT = 1337
    
    print(f"[*] Connecting to {HOST}:{PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, PORT))
    
    # Read banner
    recv_until(s, "Juleønske i hex (INGEN GENTAGELSER!):")
    
    # 1. Send a "snowflake" wish
    wish_str = "Snowflake wish!"
    print(f"[*] Sending snowflake wish: {wish_str}")
    encrypted_msg = encrypt_wish_for_santa(wish_str)
    hex_msg = encrypted_msg.hex()
    
    s.sendall(hex_msg.encode() + b"\n")
    
    # Receive response
    recv_until(s, "Juleønske i hex (INGEN GENTAGELSER!):")
    
    # 2. Send the SAME wish again (replay)
    print(f"[*] Sending REPLAY wish...")
    s.sendall(hex_msg.encode() + b"\n")
    
    # Receive response (hopefully containing flag)
    # The server logic: if data == last_message: if snowflake: print flag.
    
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk: break
            print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
        except socket.timeout:
            break
            
    s.close()

if __name__ == "__main__":
    solve()
