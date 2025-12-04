+++
title = 'Cyberkok Hekseri'
categories = ['Kom godt i gang']
date = 2023-12-01T10:04:59+01:00
scrollToTop = true
+++

## Challenge Name:

Cyberkok Hekseri

## Category:

Kom godt i gang

## Challenge Description:

Vi har modtaget følgende kalender fra vores verdensberømte cyberkok. Han har bagt kage og hekset julegodter frem for blandt andre GCHQ.

```bash
+ -------------------- +
|       DECEMBER       |
+ -------------------- +
|  M  T  O  T  F  L  S |
+ -------------------- +
| 4e 43 33 7b 6e 75 20 |
| 65 72 20 64 65 74 20 |
| 6a 75 6c 65 74 69 64 |
| 20 69 67 65 6e 21 20 |
| 3c 33 7d             |
+ -------------------- +
```

## Approach

This looks like a cipher challenge, seeing as none of the characters seem recognizable!
We even seem to get a bit of help from the title, seeing as "Cyberkok" is Danish for [Cyberchef](https://gchq.github.io/CyberChef/), which is a very handy tool for Cryptography!

If we try to identify the individual calendar day entries like 4e, 43, 33, etc we find that these are axually "hex" values, which yet again could be a hint in the title "Hekseri", which translated to English actually means witchcraft, but the Danish words contains "heks", which illudes to "hex values".

If we run all the calendar entries trough [Cyberchef with Hex selected](<https://cyberchef.org/#recipe=From_Hex('Auto')&input=NGUgNDMgMzMgN2IgNmUgNzUgMjAgNjUgNzIgMjAgNjQgNjUgNzQgMjAgNmEgNzUgNmMgNjUgNzQgNjkgNjQgMjAgNjkgNjcgNjUgNmUgMjEgMjAgM2MgMzMgN2Q>), we get the flag!

## Flag

```text
NC3{nu er det juletid igen! <3}
```

## Reflections and Learnings

Especially in introduction tasks the title can be a good hint for what to try out!
