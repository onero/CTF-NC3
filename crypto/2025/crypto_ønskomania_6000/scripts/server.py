import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ======== Load Santa's private key from file ========
santa_private_key = serialization.load_pem_private_key(
    Path("keys/santa_private_key.pem").read_bytes(),
    password=None
)

# ======== Load Santa's public key from file ========
santa_public_key = serialization.load_pem_public_key(
    Path("keys/santa_public_key.pem").read_bytes()
)

# ======== Load Hackers's public key from file ========
hacker_public_key = serialization.load_pem_public_key(
    Path("keys/hacker_public_key.pem").read_bytes()
)

# ======== Perform ECDH to derive shared secret ========
shared_secret = santa_private_key.exchange(hacker_public_key)

# Sizes
AES_KEY_LEN = 32   # 256-bit AES key
GCM_NONCE_LEN = 12
HKDF_SALT_LEN = 16


def log(message: str):
    with Path("server.log").open("a") as f:
        f.write(f"{message}\n")
    print(message, file=sys.stderr)


def derive_aes_key(shared_secret: bytes, salt: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
    )
    return hkdf.derive(shared_secret)


def santa_decrypt_wish(
    key: bytes, 
    blob: bytes, #blob (nonce||ct||tag)
    aad: bytes | None = None
) -> bytes:
    if len(blob) < GCM_NONCE_LEN + 16:  # minimal sanity: nonce + tag
        raise ValueError("ciphertext blob for lille")

    aesgcm = AESGCM(key)
    nonce = blob[:GCM_NONCE_LEN]
    ct_and_tag = blob[GCM_NONCE_LEN:]
    return aesgcm.decrypt(nonce, ct_and_tag, aad)   


def main():
    # Ensure stdout is unbuffered for immediate output
    sys.stdout.reconfigure(line_buffering=True)
    
    log("🎅 Forbindelse modtaget")
    
    print("🎅 Velkommen til Julemandens ønskeservice!")
    
    last_message: bytes | None = None
    
    while True:
        print("\n🎁 Send et juleønske i hex (INGEN GENTAGELSER!):")
        try:
            ciphertext = bytes.fromhex(input("> "))
        except ValueError:
            print("Det er vist ikke korrekt hex, prøv igen")
            continue
        except (EOFError, KeyboardInterrupt):
            print("👋 Farvel, tak for dine ønsker!")
            break
        
        log(f"📥 Modtaget {len(ciphertext)} bytes")
        
        if len(ciphertext) == 0:
            print("👋 Farvel, tak for dine ønsker!")
            break

        aad_len = int.from_bytes(ciphertext[:2], "big")
        aad = ciphertext[2 : 2 + aad_len]
        salt = ciphertext[2 + aad_len : 2 + aad_len + 16]
        encrypted = ciphertext[2 + aad_len + 16 :]

        aeskey = derive_aes_key(shared_secret, salt)
        
        try:
            plaintext = santa_decrypt_wish(aeskey, encrypted, aad)
            log(plaintext)
        except Exception as e:
            print(f"🚨 Hov, det ønske kunne ikke dekrypteres: {e}")
            continue

        if last_message is None:
            print("🎄 Mange tak for dit første juleønske!")
        elif ciphertext == last_message:
            flag = Path("flag.txt")
            if flag.exists():
                print(flag.read_text().strip())
            else:
                print("Flaget er blevet væk!")
            break
        else:
            print("✨ Tak for endnu et nyt ønske")

        last_message = ciphertext


if __name__ == "__main__":
    main()
