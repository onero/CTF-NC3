import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

# Parameters from the challenge
p_hex = "AB359AA76A6773ED7A93B214DB0C25D0160817B8A893C001C761E198A3694509EBE87A5313E0349D95083E5412C9FC815BFD61F95DDECE43376550FDC624E92FF38A415783B97261204E05D65731BBA1CCFF0E84C8CD2097B75FECA1029261AE19A389A2E15D2939314B184AEF707B82EB94412065181D23E04BF065F4AC413F"
g = 2
lyn_priv_hex = "486F762064752C20646574206865722065722062617265204C796E732070726976617465206B6579202D206875736B20696B6B652061742064656C652064656E206D6564206E6F67656E21"
springer_pub_hex = "39E22730E9F0B9F9039A2FB9F1C665DA1A05717400682946BC445093C3DF8D6164C5319C37E5EF688D346CA46168EE025E0675756EB1CE63F84BAA3B159545159EE621498F23BE036BD0037201E35D01E1FAFFBBD3C5A5AA3152114870430CDE4A7B48A822A4478FD9C443CFBC73C328C152409D1223F7ACA502F736B15019DC"

# Convert hex strings to integers
p = int(p_hex, 16)
lyn_priv = int(lyn_priv_hex, 16)
springer_pub = int(springer_pub_hex, 16)

# Calculate Shared Secret: s = B^a mod p
# shared_secret = (Springer_Public ^ Lyn_Private) % p
shared_secret = pow(springer_pub, lyn_priv, p)

print(f"Shared Secret calculated: {shared_secret}")

# Derive key
key = hashlib.sha256(long_to_bytes(shared_secret)).digest()

# Decrypt messages
try:
    with open("skjult_sladder.txt") as f:
        encrypted_messages = [bytes.fromhex(line) for line in f if line.strip()]

    print("\n--- Decrypted Messages ---")
    for i, ciphertext in enumerate(encrypted_messages):
        try:
            cipher = AES.new(key, AES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            print(f"[{i}] {plaintext.decode()}")
        except Exception as e:
            print(f"[{i}] Error decrypting: {e}")

except FileNotFoundError:
    print("Error: skjult_sladder.txt not found.")
