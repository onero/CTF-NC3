#!/usr/bin/env python3
from config import N, e, d, flag
from string import printable

CHARACTERS = printable + "æøåÆØÅ"

def encrypt(m: int) -> int:
    return pow(m, e, N)

def decrypt(c: int) -> int:
    return pow(c, d, N)

def print_banner():
    print("=== 🎄 NISSELANDS ØNSKOMAT v12.24 🎄 ===")
    print()
    print("Velkommen til Nisselands Ønskekrypteringsstation!")
    print("Alle juleønsker skal krypteres før afsendelse til Julemandens postkontor,")
    print("i henhold til det nye NISS3-direktiv.")
    print()
    print("🎅 Julemandens offentlige nøgle: 🎅")
    print()
    print(f"  e = {e}")
    print(f"  N = {N}")
    print()
    print("Indtast dine ønsker ét af gangen, så krypteres de af Ønskomaten.")
    print()
    print("Tryk ENTER uden tekst for at afslutte.")
    print()

def main():
    print_banner()

    # Julemandens hemmelige ønskeforstærkere
    mid = len(flag) // 2
    a = int.from_bytes(flag[:mid])
    b = int.from_bytes(flag[mid:])

    while True:
        wish = input("🎁 Juleønske: ").strip()
        if not wish:
            print("\n⛄ Ønskomaten lukker ned. Glædelig jul! 🎄")
            break
        
        if set(wish) - set(CHARACTERS):
            print("🚨 Ugyldigt ønske! Ønskomaten supporterer endnu ikke de tegn!\n")
            continue

        m = int.from_bytes(wish.encode("latin-1"))
        c = encrypt(a * m + b)

        print(f"✨ Krypteret: {hex(c)[2:]}\n")

if __name__ == "__main__":
    main()
