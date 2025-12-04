import hashlib

# Imports kommer fra pakken pycryptodome, der er meget brugt i kryptografi, du kan installere den med
# python -m pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes


# Hmm, hvordan finder jeg vores shared secret???
shared_secret = ...


### DU BEHØVER IKKE ÆNDRE NOGET I DEKRYPTERINGSKODEN HERUNDER ###

# Brug hash af shared secret som nøgle
key = hashlib.sha256(long_to_bytes(shared_secret)).digest()

# Læs krypterede beskeder ind fra filen
with open("skjult_sladder.txt") as f:
    encrypted_messages = [bytes.fromhex(line) for line in f if line.strip()]

# Dekrypter og print hver besked
for ciphertext in encrypted_messages:
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print(plaintext.decode())
