+++
title = 'Nisseportalen 4'
categories = ['Boot2Root']
date = 2024-12-15T13:36:38+01:00
scrollToTop = true
+++

## Challenge Name:

Nisseportalen 4

## Category:

Boot2Root

## Challenge Description:

Nissernes største ønske er en portal til deling af alle deres AI-genererede billeder aka Nisseportalen. Projektet er dog i fare efter Nissedevs utallige fiaskoer med både Dangerzone og Nissezonen.

Praktikantnissen har fået til opgave at redde Nisseportalen og få ryddet op i Nissedevs rod. Kan du hjælpe med at redde Nisseportalen og finde alle de sårbarheder, der må være, så projektet endelig kan blive gjort færdigt?

Men vær beredt, det er ikke til at sige hvad Nissedev har haft gang i...

[https://tryhackme.com/jr/nisseportalen2o24](https://tryhackme.com/jr/nisseportalen2o24)

## Approach

### Enumeration

### Exploitation

### Getting foothold on the server

Favorite revshell generator page [Revshells](https://www.revshells.com/)

![Reverse shell upload](images/reverse-shell.png)

```bash
nc -lvnp 1337
Listening on 0.0.0.0 1337
Connection received on 10.10.20.207 38504
Linux dangerzone 5.10.0-25-amd64 #1 SMP Debian 5.10.191-1 (2023-08-16) x86_64 GNU/Linux
23:47:57 up 1:25, 0 users, load average: 0.00, 0.00, 0.00
USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### Getting fourth flag

Thanks to "" we can submit the fourth flag and move on to the final challenge [Nisseportalen 5](/nc3/boot2root/nisseportalen-5)!

## Flag

```text
NC3{Flag4:DU_3R_jo_3N_54Nd_cy83Rni523}
```

## Reflections and Learnings
