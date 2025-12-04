import re
import base64
import bz2
import subprocess
import shutil
import sys
import os

def solve():
    filename = "julemors_opskrift.jpg"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return

    b64_string = None

    # Method 1: Try using exiftool (preferred, matches writeup)
    if shutil.which("exiftool"):
        print("[*] exiftool found, extracting XPComment...")
        try:
            result = subprocess.run(
                ["exiftool", "-XPComment", "-s3", filename], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                candidate = result.stdout.strip()
                if "Qlpo" in candidate:
                    print("[*] Found candidate string in XPComment.")
                    match = re.search(r"Qlpo[a-zA-Z0-9+/=]+", candidate)
                    if match:
                        b64_string = match.group(0)
        except Exception as e:
            print(f"[!] Error running exiftool: {e}")

    # Method 2: Fallback to raw file search (Regex)
    if not b64_string:
        print("[*] Attempting raw file search for 'Qlpo' pattern...")
        try:
            with open(filename, "rb") as f:
                data = f.read()
            
            # 2a. Try ASCII Pattern
            pattern_ascii = b"Qlpo[a-zA-Z0-9+/=]+"
            match = re.search(pattern_ascii, data)
            
            if match:
                b64_string = match.group(0).decode('ascii')
                print(f"[*] Found ASCII regex match in file content (length {len(b64_string)}).")
            else:
                # 2b. Try UTF-16LE Pattern (common for XPComment)
                # Qlpo in UTF-16LE is Q\x00l\x00p\x00o\x00
                # We look for the pattern where each char is followed by \x00
                # Constructing a regex for UTF-16LE base64 is a bit verbose but possible.
                # Simpler: Search for the header, then grab a chunk and filter nulls to verify.
                
                header_utf16 = b"Q\x00l\x00p\x00o\x00"
                start_idx = data.find(header_utf16)
                
                if start_idx != -1:
                    print(f"[*] Found UTF-16LE header at offset {start_idx}.")
                    # Extract a reasonable chunk to process (e.g., until null terminator or non-base64 char)
                    # Since we don't know the exact length, let's grab enough bytes.
                    # The encoded text is likely long.
                    
                    # Start scanning from start_idx
                    # We expect pairs: [char, \x00]
                    extracted_bytes = bytearray()
                    i = start_idx
                    while i < len(data) - 1:
                        char_byte = data[i]
                        null_byte = data[i+1]
                        
                        if null_byte != 0:
                            # End of UTF-16LE string or invalid format
                            break
                        
                        # Check if char_byte is valid base64 char
                        if chr(char_byte).isalnum() or chr(char_byte) in "+/=":
                             extracted_bytes.append(char_byte)
                             i += 2
                        else:
                            break
                    
                    if extracted_bytes:
                        b64_string = extracted_bytes.decode('ascii')
                        print(f"[*] Extracted UTF-16LE string (length {len(b64_string)}).")

        except Exception as e:
            print(f"[!] Error reading file: {e}")

    if not b64_string:
        print("[!] Could not find the encoded string.")
        return

    # Decoding Steps
    print("[*] Decoding data...")
    try:
        # 1. Base64 Decode
        raw_data = base64.b64decode(b64_string)
        
        # 2. Bzip2 Decompress
        decompressed_data = bz2.decompress(raw_data)
        
        # 3. Text Decode (latin-1)
        decoded_text = decompressed_data.decode('latin-1')
        
        print("\n" + "="*40)
        print("DECODED RECIPE CONTENT")
        print("="*40)
        print(decoded_text)
        print("="*40 + "\n")
        
        # Extract Flag
        flag_match = re.search(r"NC3\{.*?\}", decoded_text)
        if flag_match:
            flag = flag_match.group(0)
            print(f"[+] FLAG FOUND: {flag}")
            
            with open("flag.txt", "w") as f:
                f.write(flag)
            print("[+] Flag saved to flag.txt")
        else:
            print("[-] No flag pattern (NC3{...}) found in decoded text.")

    except Exception as e:
        print(f"[!] Decoding failed: {e}")

if __name__ == "__main__":
    solve()