import socket
import re

def iroot(n, k):
    """Integer k-th root of n."""
    if n == 0: return 0
    u, s = n, n + 1
    while u < s:
        s = u
        t = (k - 1) * s + n // pow(s, k - 1)
        u = t // k
    return s

def recv_until(s, match_str):
    buffer = b""
    while True:
        chunk = s.recv(4096)
        if not chunk: break
        buffer += chunk
        if match_str.encode() in buffer:
            return buffer.decode('utf-8', errors='ignore')
    return buffer.decode('utf-8', errors='ignore')

def solve():
    host = "10.82.141.55"
    port = 1337
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # Read banner for N
    data = recv_until(s, "Juleønske:")
    n_match = re.search(r"N = (\d+)", data)
    N = int(n_match.group(1))

    # Send '1'
    s.send(b"1\n")
    data = recv_until(s, "Juleønske:")
    c1 = int(re.search(r"Krypteret: ([0-9a-f]+)", data).group(1), 16)

    # Send '2'
    s.send(b"2\n")
    data = recv_until(s, "Juleønske:")
    c2 = int(re.search(r"Krypteret: ([0-9a-f]+)", data).group(1), 16)
    
    s.close()

    # Cube roots
    v1 = iroot(c1, 3)
    v2 = iroot(c2, 3)

    # Solve linear system
    a = v2 - v1
    b = v1 - 49 * a
    
    # Decode
    len_a = (a.bit_length() + 7) // 8
    len_b = (b.bit_length() + 7) // 8
    flag = a.to_bytes(len_a, 'big') + b.to_bytes(len_b, 'big')
    print(flag.decode('latin-1'))

if __name__ == "__main__":
    solve()