import socket
import re
import sys
import time

# --- Utils ---
def iroot(n, k):
    """Integer k-th root of n."""
    if n == 0: return 0
    u, s = n, n + 1
    while u < s:
        s = u
        t = (k - 1) * s + n // pow(s, k - 1)
        u = t // k
    return s

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# --- Solver ---

def pad(m: str) -> int:
    # Re-implement server padding logic
    # m.encode(errors="surrogateescape").lstrip(b"\x00").ljust(16, b"=")
    b_str = m.encode('utf-8') 
    padded = b_str.lstrip(b"\x00").ljust(16, b"=")
    return int.from_bytes(padded, 'big')

def solve_linear_system(coeffs, constants, N):
    """
    Solve M * x = C mod N
    coeffs: 4x4 matrix (list of lists)
    constants: list of 4 values
    Returns list of 4 values
    """
    n = 4
    M = [row[:] for row in coeffs]
    C = constants[:]
    
    for i in range(n):
        pivot = M[i][i]
        if pivot == 0:
            for j in range(i+1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    C[i], C[j] = C[j], C[i]
                    pivot = M[i][i]
                    break
            if pivot == 0:
                raise Exception("Singular matrix")
        
        inv = modinv(pivot, N)
        for j in range(i, n):
            M[i][j] = (M[i][j] * inv) % N
        C[i] = (C[i] * inv) % N
        
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n):
                    M[k][j] = (M[k][j] - factor * M[i][j]) % N
                C[k] = (C[k] - factor * C[i]) % N
                
    return C

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

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <IP>")
        sys.exit(1)
        
    host = sys.argv[1]
    port = 1337
    
    print(f"[*] Connecting to {host}:{port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    
    # Read N
    print("[*] Reading banner...")
    data = recv_until(s, "Juleønske:")
    
    n_match = re.search(r"N = (\d+)", data)
    if not n_match:
        print("[-] Could not find N in banner")
        return
        
    N = int(n_match.group(1))
    print(f"[+] N = {N}")
    
    inputs = ["1", "2", "3", "4"]
    ms = [pad(x) for x in inputs]
    cs = []
    
    for i, inp in enumerate(inputs):
        print(f"[*] Sending wish: {inp}")
        s.sendall(inp.encode() + b"\n")
        
        data = recv_until(s, "Juleønske:")
        
        c_match = re.search(r"Krypteret: ([0-9a-f]+)", data)
        if c_match:
            c = int(c_match.group(1), 16)
            cs.append(c)
        else:
            print("[-] Failed to get ciphertext")
            return
                
    s.close()
    
    # Build Matrix
    # Coeffs of [a^3, a^2b, ab^2, b^3]
    # Row: [m^3, 3m^2, 3m, 1]
    
    matrix = []
    for m in ms:
        row = [
            pow(m, 3, N),
            (3 * pow(m, 2, N)) % N,
            (3 * m) % N,
            1
        ]
        matrix.append(row)
        
    print("[*] Solving linear system...")
    try:
        sol = solve_linear_system(matrix, cs, N)
        a3, a2b, ab2, b3 = sol
        
        print(f"[+] a^3 = {a3}")
        print(f"[+] b^3 = {b3}")
        
        # Try cube roots
        a = iroot(a3, 3)
        b = iroot(b3, 3)
        
        if pow(a, 3) == a3:
            print("[+] Found exact cube root for a!")
        else:
            print("[-] a^3 is not a perfect cube (modulo reduction occurred?)")
            
        if pow(b, 3) == b3:
            print("[+] Found exact cube root for b!")
        else:
            print("[-] b^3 is not a perfect cube (modulo reduction occurred?)")
            
        # Decode
        try:
            flag_a = a.to_bytes((a.bit_length() + 7) // 8, 'big')
            flag_b = b.to_bytes((b.bit_length() + 7) // 8, 'big')
            flag = flag_a + flag_b
            print(f"\n🎉 FLAG: {flag.decode('utf-8', errors='replace')}")
        except Exception as e:
            print(f"Error decoding: {e}")
            
    except Exception as e:
        print(f"[-] Solver failed: {e}")

if __name__ == "__main__":
    main()
