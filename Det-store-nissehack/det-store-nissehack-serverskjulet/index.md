+++
title = 'Det store nissehack: Serverskjulet'
categories = ['Forensic']
date = 2024-12-17T18:40:25+01:00
scrollToTop = true
+++

## Challenge Name:

Det store nissehack: Serverskjulet

## Category:

Det store nissehack

## Challenge Description:

Julens politi formoder, at gerningsgnomen har etableret en skjult server og et tilknyttet domæne for at skjule sine spor.

Kan du bruge den fundne IP-adresse til at finde serveren og domænet, hvor yderligere spor om gerningsgnomen kan afsløres?

## Approach

After completing the first task, we obtained the IP address: 209.38.243.124. The next step was to investigate this address and uncover further clues.

#### Exploring the IP

The natural first step was to open the IP address in a web browser. Upon doing so, we encountered a redirection to a domain, followed by an `ERR_CERT_AUTHORITY_INVALID` error.

![invalid cert authority](images/site-invalid-cert.png)

Instead of ignoring the error, we inspected the SSL certificate more closely to understand what might be wrong. This is a common tactic, as unexpected certificates can often hide useful information.

#### Inspecting the Certificate

![checking certificate](images/certificate-check.png)

By examining the certificate, we quickly noticed something unusual. Hidden within the certificate's details, we found the next flag:
![flag](images/flag.png)

## Flag
NC3{1nfiL7rAti0n_0g_3xf1ltr4t1on}

## Reflections and Learnings

This challenge served as an excellent reminder of the importance of thoroughly investigating every error or warning presented during reconnaissance. Security warnings, like certificate errors, are often overlooked, but they can provide significant clues in CTF challenges or real-world scenarios.

Key Takeaways:
1. **Pay Attention to Errors**: Error messages like ERR_CERT_AUTHORITY_INVALID may seem routine, but they often indicate something unusual. Always check what caused the error.
2. **Inspect Everything**: When facing unexpected results, explore all details — whether it’s certificates, metadata, or HTTP headers.
3. **Think Outside the Box**: CTF challenges often test your ability to look beyond the obvious. In this case, the flag was cleverly hidden in plain sight within the certificate.
By developing these habits, you not only improve your skills for CTF competitions but also build a mindset that’s critical for real-world penetration testing and security analysis.
