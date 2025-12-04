+++
title = 'Nissens Juleshop'
categories = ['Kom godt i gang']
date = 2023-12-01T10:11:50+01:00
scrollToTop = true
+++

## Challenge Name:

Nissens Juleshop

## Category:

Kom godt i gang

## Challenge Description:

Nissen har lige åbnet sin årlige juleshop, har han mon noget spændende at købe?

Forbind til opgaven med nc juleshop.nc3 2674.

Note: Opgaven var tilgængelig via Haaukins under CTFen

## Approach

### Enumeration

This is one of the few "dynamic" introduction challenges, in which we need to connect to a lab in Haaukins and connect to a remote machine.

Upon connecting to the server with the netcat command

```bash
nc juleshop.nc3 2674
```

We are greeted by the following

```bash
Velkommen til Nissens Juleshop!

Du har i øjeblikket 1000 JULESNE på din konto
Hvad vil du købe?
        1) Julelys (85 JULESNE)
        2) Gavepapir (40 JULESNE)
        3) Sneskovl (230 JULESNE)
        4) Juletræ (760 JULESNE)
        5) Flag (1000000 JULESNE)
>
```

Which translated from Danish reads:

```bash
Welcome to Nissens Chistmas Shop!

You currently have 1000 CHRISTMAS-SNOW on your account
What would you like to purchase?
        1) Chistmas candles (85 CHRISTMAS-SNOW)
        2) Gift wrapping paper (40 CHRISTMAS-SNOW)
        3) Snow shovel (230 CHRISTMAS-SNOW)
        4) Chistmas tree (760 CHRISTMAS-SNOW)
        5) Flag (1000000 CHRISTMAS-SNOW)
>
```

If we choose a product we are asked how many we would like to purchase, after which the price is deducted from the total balance on our account!

If we try to purchase a product we can't afford, we get the following error message:

```bash
> 5
Den går ikke, du har ikke engang råd til 1x Flag
```

Which translated from Danish reads:

```bash
> 5
That won't do, you can't even afford 1x Flag
```

### Exploiting

There is a great old joke about a software tester who walks into a bar, which goes something like

```text
A software tester walks into a bar.

Walks into a bar
Runs into a bar.

Crawls into a bar.

Dances into a bar.

Flies into a bar.

Jumps into a bar.

And orders:

a beer.

2 beers.

0 beers.

99999999 beers.

a lizard in a beer glass.

-1 beer.

"qwertyuiop" beers.

Testing complete.

A real customer walks into the bar and asks where the bathroom is.

The bar goes up in flames.
```

The "moral of the story" is that whenever executing quality assurance on software, it is usually a good idea to provide unexpected input!

When we think about the challenge at hand, let's see what happens if we provide a negative amount!

```bash
Du har i øjeblikket 1000 JULESNE på din konto
Hvad vil du købe?
        1) Julelys (85 JULESNE)
        2) Gavepapir (40 JULESNE)
        3) Sneskovl (230 JULESNE)
        4) Juletræ (760 JULESNE)
        5) Flag (1000000 JULESNE)
> 4

Hvor mange vil du købe?
> -100000

Du har købt -100000 stk. Juletræ for i alt -76000000 JULESNE

Du har i øjeblikket 76001000 JULESNE på din konto
```

Which translated from Danish reads:

```bash
You currently have 1000 CHRISTMAS-SNOW on your account
What would you like to purchase?
        1) Chistmas candles (85 CHRISTMAS-SNOW)
        2) Gift wrapping paper (40 CHRISTMAS-SNOW)
        3) Snow shovel (230 CHRISTMAS-SNOW)
        4) Chistmas tree (760 CHRISTMAS-SNOW)
        5) Flag (1000000 CHRISTMAS-SNOW)
> 4

How many would you like to purchase?
> -100000

You bought -100000 Chistmas tree for a total of -76000000 CHISTMAS-SNOW

Your balance is currently 76001000 CHISTMAS-SNOW
```

Suddenly we have a wealth of "CHISTMAS-SNOW" at our disposal and the flag can easily be purchased!

```bash
> 5
Du har købt flaget for 1000000 JULESNE:
NC3{hv4d_sk3t3_d3r_4lt_bl3v_uds0lg7_på_10_m1n?!?}
```

Which translated from Danish reads:

```bash
> 5
You bought the flag for a total of 1000000 CHISTMAS-SNOW:
NC3{hv4d_sk3t3_d3r_4lt_bl3v_uds0lg7_på_10_m1n?!?}
```

## Flag

```text
NC3{hv4d_sk3t3_d3r_4lt_bl3v_uds0lg7_på_10_m1n?!?}
```

## Reflections and Learnings

The "Nissens Juleshop" challenge was a fun and educational exercise in thinking outside the box and testing the boundaries of a system. This challenge reinforced the importance of considering edge cases and unusual inputs when interacting with any system, especially one that processes numerical inputs like an online shop.

One of the key learnings from this challenge was the significance of input validation. The challenge exploited the lack of input validation for negative numbers, allowing for an interesting and unconventional solution. It highlighted a common vulnerability in many systems where developers might not anticipate or properly handle unexpected inputs. This is a crucial aspect in the field of cybersecurity and software development, where robust input validation can prevent many exploits and security issues.

Furthermore, this challenge was a great reminder of the classic principle in hacking and cybersecurity: "Think like an attacker." Approaching the challenge from an attacker's perspective, looking for ways to break the system or use it in unintended ways, led to the discovery of the vulnerability and the successful completion of the challenge. This mindset is invaluable in both offensive and defensive cybersecurity roles.
