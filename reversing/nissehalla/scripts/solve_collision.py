def get_visited_indices(length):
    # Initial parameters
    # r9 is initialized at 180b (Wait, r9 is used in 1808 'add r13, r9' BEFORE update?)
    # Let's check init of r9.
    # 180b: lea r9, [r9 + 4*r9 + 3] is in the loop.
    # Where is r9 set BEFORE the loop?
    # At 1608: lea r9, [rip+0xbc1] (SALT_BYTES).
    # Then loop 1640 uses r9.
    # Then loop 1760 uses r9.
    # AFTER those loops, before 1802:
    # 17a6: movabs rax, ...
    # ...
    # 17d1: sub r9, rax (Wait, r9 was r15 (len) in 17b0: mov r9, r15).
    # 17b0: mov r9, r15
    # ...
    # 17d4: add r9, 1
    # So initial r9 = (Calculated from length)
    
    # 17b3: mul r15 (rax = 0x2492492492492493 * len)
    # 17b6: mov rax, r15
    # 17b9: sub rax, rdx
    # 17bc: shr rax, 1
    # 17bf: add rdx, rax
    # 17c2: shr rdx, 2
    # rdx = len // 7  (0x249... is 1/7 approx fixed point)
    # 17c6: lea rax, [8*rdx]
    # 17ce: sub rax, rdx (rax = 7 * (len//7))
    # 17d1: sub r9, rax (r9 = len - 7*(len//7) = len % 7)
    # 17d4: add r9, 1  (r9 = (len % 7) + 1)
    
    step = (length % 7) + 1
    curr = 0
    visited = set()
    
    # Loop structure simulation
    # The code jumps to Body (1821) first.
    # Then updates (1808).
    
    while True:
        # Body (1821)
        visited.add(curr)
        
        # Check (18d2)
        if (curr & 3) == 0:
            # Inner loop logic
            # Accesses curr, curr+1, curr+2 (if < length)
            # Logic:
            # r14 starts at curr
            # It loops 3 times (r12d=0,1,2)
            # But inside:
            # cmp r14, length; jae update_block
            # add r14, 1
            # access input[r14] (Wait, input[r14] AFTER increment?)
            # Re-read:
            # 18eb: mov rax, r14
            # 18f0: add r14, 1
            # 18f4: div r15 (rdx = rax % r15 = old_r14 % length)
            # Wait, div uses RDX:RAX.
            # 18ee: xor edx, edx
            # So RDX:RAX is 0:old_r14.
            # rdx becomes old_r14 % length.
            # 18f7: access input[rdx]
            # So it accesses input[old_r14].
            # Iter 0: old_r14 = curr. Access input[curr]. (Already visited)
            # Iter 1: old_r14 = curr+1. Access input[curr+1].
            # Iter 2: old_r14 = curr+2. Access input[curr+2].
            
            # The Bounds Check 18e2: cmp r14, r15; jae update_block.
            # Iter 0: r14=curr. Safe (curr < length).
            # Iter 1: r14=curr+1. Check bounds. If >= length, abort inner loop.
            # Iter 2: r14=curr+2. Check bounds. If >= length, abort.
            
            if curr + 1 < length:
                visited.add(curr + 1)
                if curr + 2 < length:
                    visited.add(curr + 2)
        
        # Update Block (1808)
        curr += step
        
        # Update step (r9)
        # 180b: lea r9, [r9 + 4*r9 + 3] -> r9 = 5*r9 + 3
        # 1810: and r9d, 7
        # 1814: add r9, 1
        step = ((5 * step + 3) & 7) + 1
        
        if curr >= length:
            break
            
    return visited

def find_collision():
    print("Searching for lengths with unused bytes...")
    for l in range(10, 300):
        visited = get_visited_indices(l)
        if len(visited) < l:
            unused = sorted(list(set(range(l)) - visited))
            print(f"[!] FOUND! Length {l} has {len(unused)} unused bytes.")
            print(f"    Unused indices: {unused}")
            
            # Generate files
            # File A: all 'A's
            with open("coll_a", "wb") as f:
                f.write(b'A' * l)
                
            # File B: all 'A's, but change unused byte
            with open("coll_b", "wb") as f:
                data = bytearray(b'A' * l)
                data[unused[0]] = ord('B')
                f.write(data)
                
            print(f"[+] Generated 'coll_a' and 'coll_b' (length {l}).")
            return
            
    print("[-] No unused bytes found in range 10-300.")

if __name__ == "__main__":
    find_collision()
