+++
title = 'In My Prime'
date = 2023-12-17T20:37:16+01:00
+++

## Challenge Name: In My Prime

## Category: Misc

## Challenge Description:

Du bliver givet et primtal `N` og skal inden for 3 sekunder udføre følgende tre beregninger og svare med summen af resultaterne:

1. For hvert 2. primtal fra `N` ned til 0: Udregn summen af det mest betydende og mindst betydende ciffer. Læg resultaterne sammen.
2. For hvert 3. primtal fra `N` ned til 0: Udregn tværsummen af primtallet i base 7. Læg resultaterne sammen.
3. For hvert 5. primtal fra `N` ned til 0: Lad `p1` være dette primtal og `p2` det nærmeste mindre primtal. Udregn `(p1 * p2) mod 31337` og tæl antallet af ulige cifre. Læg resultaterne sammen.

**Eksempel:**

```python
Givet N = 23:

primtal = [2,  3,  5,  7, 11, 13, 17, 19, 23]

1) [23, 17, 11, 5, 2]   - Hvert 2. primtal
2) [23, 13, 5]          - Hvert 3. primtal
3) [23, 7]              - Hvert 5. primtal


1) 2+3 + 1+7 + 1+1 + 5+5 + 2+2 = 29

2) base_7(23) = 32 -> 3 + 2  =  5
   base_7(13) = 16 -> 1 + 6  =  7
   base_7(5)  =  5 -> 5      =  5
                             -----
                               17

3) 23*19 mod 31337 = 437 -> 2
     7*5 mod 31337 =  35 -> 2
                     --------
                            4

Svaret er derfor: 29 + 17 + 4 = 50


      N |   Svar
--------+-------
     23 |     50
     97 |    178
    997 |   1434
 549979 | 509053
```

## Approach

- Within 3 seconds the 3 categories should be calculated and the results of all should be returned as the response...
- Implemented Solution in Python, but took 10 seconds to compute response... This indicates pre-calculation might be needed!
- Tested if question was truly randomly generated with another python script, but unfortunately it was... Seems to be between 70M and 100M numbers!
- Created a compute-all-solutions Rust script, which runs on a dedicated server, but this will take a very long time for appr 1,3M primes...
- Created "self-learning" python version, which calls to get a question and if it doesn't have it, it:
  - calculates it
  - responds with the answer (too late)
  - and adds the result to the cache.
    This way it will gradually build up a cache and increase the chance to hit a known question!

![Automagic Prime Solver](/automagic-prime-solver.png)

- After the cache of the self-leaning script reached 6K pre-calculated results I also created a "lucky_prime" script, which just
  - calls and checks if the question is in the cache
  - if not then it disconnects
  - Saves question for later sanity check of solution!
  - and then retries!

In the end first the lucky_prime solved the challenge and on attempt 8.876 the self-learning script also succeeded!

## Flag

```text
NC3{th3_numb3rs_wh4t_d0_th3y_m3an?}
```

## Reflections

<reflections ...>
