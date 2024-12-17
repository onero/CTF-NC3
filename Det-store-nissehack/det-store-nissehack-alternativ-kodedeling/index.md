+++
title = 'Det store nissehack: Alternativ Kodedeling'
categories = ['Det store nissehack']
date = 2024-12-17T18:40:25+01:00
scrollToTop = true
+++

## Challenge Name:

Det store nissehack: Alternativ Kodedeling

## Category:

Det store nissehack

## Challenge Description:

Du har fundet et interessant link på gerningsgnomens hjemmeside, men adgangen er beskyttet af en adgangskode, som du mangler.

Julens politi har en mistanke om, at nisserne har efterladt spor et sted på domænet, som kan lede dig til den nødvendige kode.

Kan du afsløre adgangskoden og låse op for sidste trin i efterforskningen?

## Approach

In the previous task, we ended up on this page, which revealed the flag:

![previous flag](images/previous-flag.png)

However, the page also included a URL to a PrivateBin instance:
```text
https://privatebin.net/?a5f7a035573705be#J5nBwc2LPLYTZKsy6prN32aHVxdMHjJfwbi4WaNcaSs8
```

Opening the link, it became evident that a password was required to unlock the content:

![private bin](images/privatebin.png)

### Identifying the Password

Revisiting the challenge description, the phrase "somewhere on the domain" stood out as unusual. It emphasized "the domain" rather than just the website. This hinted that additional information might be hidden in the domain-level records.

Lets look into the domain records for the site we found in earlier tasks, bitbibliotek.dk.

### Investigating DNS Records

DNS records can provide details about services, configurations, and hidden data associated with a domain. Tools like DNS Checker make this process simple.

https://dnschecker.org/all-dns-records-of-domain.php?query=bitbibliotek.dk&rtype=ALL&dns=google

![dns checker](images/dns-checker.png)

By searching for all DNS records for the domain bitbibliotek.dk, I found this [TXT record](https://www.cloudflare.com/learning/dns/dns-records/dns-txt-record/):

The TXT record, often used to store arbitrary text, appeared to contain the password in the format:
```text
delingmedKodetand:enjulehemmelighed1.jan
```

### Unlocking the PrivateBin

Using this string as the password, I returned to the PrivateBin link and entered it. Success! The PrivateBin content was unlocked, revealing the flag:

![flag](images/flag.png)

## Flag
NC3{d3L_1kK3_h3MmeL1gh3d3R_h3R}

## Reflections and Learnings

This challenge provided valuable lessons on thinking outside the box and exploring less conventional sources of information:

1. Revisiting Descriptions:
The emphasis on "domain" rather than "site" was subtle but critical. It highlighted the importance of reading the challenge description carefully to spot unusual hints.

2. Leveraging DNS Records:
DNS records, particularly TXT records, are often overlooked. This challenge showcased how DNS-based data can be intentionally hidden for challenges or other purposes like verification and configuration.

3. Tool Familiarity:
Tools like DNS Checker were crucial in efficiently inspecting the domain. Knowing which tools to use for tasks like DNS exploration saves time and effort.

4. Persistence and Structure:
The process of systematically narrowing down clues—from the URL to domain records—reinforced the importance of structured problem-solving in CTF challenges.

Overall, this challenge was a great reminder to broaden the investigative scope when tackling puzzles. Sometimes, the solution lies not on the surface but deeper in the infrastructure.