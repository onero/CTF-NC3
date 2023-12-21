+++
title = 'Cyberkok Eksklusiv opskrift'
categories = ['Kom godt i gang']
date = 2023-12-01T10:05:00+01:00
scrollToTop = true
+++

## Challenge Name:

Cyberkok Eksklusiv opskrift

## Category:

Kom godt i gang

## Challenge Description:

Vi tror, at vores berømte cyberkok har været lidt for dybt i julesnapsen.

Vi har i hvert fald modtaget følgende besked, men vi kan slet ikke tyde den:

```bash
Nu er det jul igen! Her er en meget EKSKLUSIV opskrift!
XOXOXO

+----------------------+
|       JULEMAD        |
+----------------------+
| 04 16 7f 3e 2c 29 69 |
| 2e 30 22 68 2a 2d 25 |
| 2e 30 61 2f 38 2d 21 |
| 3e 3c 28 68 20 20 2a |
| 67 37 20 2c 3b 24 36 |
| 67 26 a9 68 2a 2d 25 |
| 2e 74 31             |
+----------------------+
```

## Approach

So yet again the "Cyberchef" has tried out some new cipher "recipe"...
As described in [Cyberkok Hekseri](/nc3/kom-godt-i-gang/cyberkok-hekseri) it is a good idea to pay close attention to both the title and the description.
"Ekslusiv opskrift", translated from Danish means "Exclusive recipe", where exclusive might illude to the concept of [XOR](https://en.wikipedia.org/wiki/Exclusive_or), which is short for "Exclusive or"!

Seeing as the input is hexadecimals and we know that the expected flag output is text, we just need the key, which should be used for the XOR operation.

If we pay close attention to the calendar, we see in the top, where one would expect the month to be stated, that the word "JULEMAD" (meaning Christmas food) is written, which seems a bit "out of place".
Working of the notion that every bit of information can be important we try out the key JULEMAD as our XOR key.

Using the following [Cyberchef recipe](<https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'UTF8','string':'JULEMAD'%7D,'Standard',false)&input=MDQgMTYgN2YgM2UgMmMgMjkgNjkgMmUgMzAgMjIgNjggMmEgMmQgMjUgMmUgMzAgNjEgMmYgMzggMmQgMjEgM2UgM2MgMjggNjggMjAgMjAgMmEgNjcgMzcgMjAgMmMgM2IgMjQgMzYgNjcgMjYgYTkgNjggMmEgMmQgMjUgMmUgNzQgMzE>) we manage to get the flag!

## Flag

```text
NC3{ah-den-glade-juletid-man-bliver-så-glad!}
```
