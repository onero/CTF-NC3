+++
title = 'Haaukins Intro'
categories = ['Kom godt i gang']
date = 2023-12-01T10:02:14+01:00
scrollToTop = true
+++

## Challenge Name:

Haaukins Intro

## Category:

Kom godt i gang

## Challenge Description:

Dynamiske opgaver i NC3 CTF 2023 kører via CTF-platformen Haaukins.

Lab Setup:

Ved oprettelse af profil, får du adgang til egen instans på dit eget subnet. Du kan i øverste højre hjørne klikke Get a lab og vælge imellem VPN eller Browser. Dit lab er dit eget, og det er dermed kun dig, der har adgang til din egen instans.

Browser labbet giver dig adgang til en Kali Linux instans i din browser, hvorfra alle opgaver kan tilgås. VMen har en række værktøjer præinstalleret og har ikke internetadgang. Se FAQ i Haaukins for instruktion til copy+paste ind i boksen.

Vælges VPN skal du klikke Download VPN Config og hente Wireguard config fil ned. Se guide til installation i FAQ på Haaukins. På Linux kan med fordel bruges install_wireguard.sh til Wireguard installation og connectwireguard.py til opsætning med config filen:

sudo python connectwireguard.py ./wg-conf-1.conf
Challenge Access:

Challenges starter alle som Not running og skal startes individuelt, når man vil løse dem. Hvis en opgave stopper med at virke, kan den resettes fra forsiden. Labbet resetter helt hver 5. time automatisk, men du kan forlænge denne tid fra forsiden, når der er under en time igen.

Nogle challenges har et hostname, fx juletid.nc3 og kan tilgås gennem browser eller med netcat via dette. I Browser lab er det direkte tilgængeligt, i VPN skal du selv opdatere din hosts fil lokalt - se Hosts tab i Haaukins (husk at starte opgaven først).

I challenges uden hostname skal servicen findes med et nmap scan af dit lab subnet. I browser lab kan dit subnet findes med kommandoen ip a under eth0. I VPN står det i toppen af din downloadede config fil. Fremgangsmåden er beskrevet i opgaveteksten til Haaukins Intro på Haaukins.

Sanity Check:

Gav det mening? Så er det tid til et lille sanity check! Opret et lab på Haaukins, start opgaven Haaukins Intro og find den IP, der har en service kørende på port 6346. Forbind til servicen for at få flaget!

OBS: Alle flag skal submittes herinde på CTFd, ikke på Haaukins!

https://ncctf.haaukins.dk

## Approach

First of all a profile on Haaukins is needed to do any of the "dynamic" challenges.
Our team discovered that you could create AS MANY accounts as you wanted, which came in VERY handy for some of the challenges later on!...

As instructed we use the Netcat command to connect to the remote server. Upon establishing the connection we get a banner print, with a seemingly randomly placed character, which appears to be part of the final flag!

```bash
$ nc intro.nc3 6346
################################################
N
################################################
```

I originally crafted a script to establish connection and replace an array of '#' characters, but later learned that most of my communication handling could be shorthanded with the [pwntools Python library](https://github.com/Gallopsled/pwntools)!
This is the final version, utilising pwntools

```python
from pwn import *

context.log_level = "warn"

IP = "intro.nc3"

flag = [32] * len("################################################")
while 32 in flag:
    with remote(IP, 6346) as io:
        io.recvline()
        line = io.recvline()

    for i, c in enumerate(line):
        if c != 32:
            flag[i] = c
            print(bytes(flag).decode())
            break

```

[Download script](Haaukins_intro.py)

What is incredibly cool about the handling is that it will result in the following output #MatrixStyle

```bash
               _
               _                          4
               _              t           4
               _  _           t           4
               _  _3          t           4
             3 _  _3          t           4
   {         3 _  _3          t           4
   {         3 _  _3     k    t           4
   {         3 _  _3r    k    t           4
   {     f   3 _  _3r    k    t           4
   {     f   3 _  _3r    k   _t           4
   {     f   3 _  _3r    kl  _t           4
   {     f   3 _  _3r    kl  _t         y 4
   {     f   3 _  _3r d  kl  _t         y 4
   {     f   3 _n _3r d  kl  _t         y 4
   {     f   3 _n _3r_d  kl  _t         y 4
   {     f   3 _n _3r_d  kl  _t         y 4m
   { 0   f   3 _n _3r_d  kl  _t         y 4m
   {g0   f   3 _n _3r_d  kl  _t         y 4m
   {g0 t f   3 _n _3r_d  kl  _t         y 4m
   {g0 t f   3t_n _3r_d  kl  _t         y 4m
   {g0 t f   3t_nu_3r_d  kl  _t         y 4m
   {g0 t f   3t_nu_3r_d  kl  _t     r   y 4m
   {g0 t f   3t_nu_3r_d  kl  _t1    r   y 4m
   {g0 t f   3t_nu_3r_d  kl  _t1    r   y 4m  !
   {g0 t_f   3t_nu_3r_d  kl  _t1    r   y 4m  !
   {g0 t_f   3t_nu_3r_d  kl  _t1    r   y 4m  !}
   {g0 t_f   3t_nu_3r_d  kl  _t1    r3  y 4m  !}
   {g0 t_f   3t_nu_3r_d  kl  _t1    r3_ y 4m  !}
   {g0 t_f   3t_nu_3r_d  kl4 _t1    r3_ y 4m  !}
   {g0 t_f   3t_nu_3r_d  kl4 _t1    r3_dy 4m  !}
   {g0 t_f n 3t_nu_3r_d  kl4 _t1    r3_dy 4m  !}
   {g0 t_f n 3t_nu_3r_d  kl4 _t1    r3_dy 4m1 !}
   {g0 t_f n 3t_nu_3r_d  kl4 _t1 _  r3_dy 4m1 !}
 C {g0 t_f n 3t_nu_3r_d  kl4 _t1 _  r3_dy 4m1 !}
NC {g0 t_f n 3t_nu_3r_d  kl4 _t1 _  r3_dy 4m1 !}
NC {g0 t_f n 3t_nu_3r_d  kl4 _t1 _  r3_dyn4m1 !}
NC {g0 t_f n 3t_nu_3r_d  kl4 _t1 _m r3_dyn4m1 !}
NC {g0 t_fun 3t_nu_3r_d  kl4 _t1 _m r3_dyn4m1 !}
NC {g0dt_fun 3t_nu_3r_d  kl4 _t1 _m r3_dyn4m1 !}
NC {g0dt_fun 3t_nu_3r_d  kl4r_t1 _m r3_dyn4m1 !}
NC {g0dt_fun 3t_nu_3r_d _kl4r_t1 _m r3_dyn4m1 !}
NC {g0dt_fun 3t_nu_3r_du_kl4r_t1 _m r3_dyn4m1 !}
NC {g0dt_fun 3t_nu_3r_du_kl4r_t1l_m r3_dyn4m1 !}
NC {g0dt_fund3t_nu_3r_du_kl4r_t1l_m r3_dyn4m1 !}
NC {g0dt_fund3t_nu_3r_du_kl4r_t1l_m3r3_dyn4m1 !}
NC3{g0dt_fund3t_nu_3r_du_kl4r_t1l_m3r3_dyn4m1 !}
NC3{g0dt_fund3t_nu_3r_du_kl4r_t1l_m3r3_dyn4m1k!}
```

## Flag

```text
NC3{g0dt_fund3t_nu_3r_du_kl4r_t1l_m3r3_dyn4m1k!}
```

## Reflections and Learnings

Getting to know pwntools was a VERY big learning from this challenge and is for sure a useful tool for the Python tool belt!
