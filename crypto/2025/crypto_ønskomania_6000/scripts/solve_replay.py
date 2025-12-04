import os
import json
import sys
import socket
import time
from pathlib import Path

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization

from thrift.protocol.TCompactProtocol import TCompactProtocol
from thrift.transport.TTransport import TMemoryBuffer
from thrift.Thrift import TType

# ---- THRIFT HELPER (from helpers.py) ----
def thrift_encode_int(n: int) -> bytes:
    buf = TMemoryBuffer()
    proto = TCompactProtocol(buf)

    proto.writeStructBegin("N")
    proto.writeFieldBegin("v", TType.I32, 1)
    proto.writeI32(n)
    proto.writeFieldEnd()
    proto.writeFieldStop()
    proto.writeStructEnd()

    return buf.getvalue()

# ---- CRYPTO SETUP ----

KEYS_DIR = Path("keys")
SANTA_PUB_KEY_PATH = KEYS_DIR / "santa_public_key.pem"
HACKER_PRIV_KEY_PATH = KEYS_DIR / "hacker_private_key.pem"

if not SANTA_PUB_KEY_PATH.exists():
    print(f"Error: {SANTA_PUB_KEY_PATH} not found.")
    sys.exit(1)
if not HACKER_PRIV_KEY_PATH.exists():
    print(f"Error: {HACKER_PRIV_KEY_PATH} not found.")
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
    
    # Use a fixed counter for reproducibility in this exploit
    counter = 1337
    encoded_counter = thrift_encode_int(counter)   
    counter_bytes = encoded_counter.ljust(8, b"\x00")[:8]
    random_tail = os.urandom(4)

    nonce = counter_bytes + random_tail
    # nonce length must be 12
    
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
    HOST = "10.82.128.188"
    PORT = 1337
    
    print(f"[*] Connecting to {HOST}:{PORT}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, PORT))
    
    # Read banner
    recv_until(s, "Juleønske i hex (INGEN GENTAGELSER!):")
    
    # 1. Send a wish
    wish_str = "I want a flag!"
    print(f"\n[*] Sending wish: {wish_str}")
    encrypted_msg = encrypt_wish_for_santa(wish_str)
    hex_msg = encrypted_msg.hex()
    
    s.sendall(hex_msg.encode() + b"\n")
    
    # Receive response
    response = recv_until(s, "Juleønske i hex (INGEN GENTAGELSER!):")
    
    # 2. Send the SAME wish again
    print(f"\n[*] Sending REPLAY wish...")
    s.sendall(hex_msg.encode() + b"\n")
    
    # Receive response (hopefully containing flag)
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
