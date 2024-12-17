+++
title = 'Det store nissehack: Kodedepotets Hemmeligheder'
categories = ['Det store nissehack']
date = 2024-12-17T18:40:25+01:00
scrollToTop = true
+++

## Challenge Name:

Det store nissehack: Kodedepotets Hemmeligheder

## Category:

Det store nissehack

## Challenge Description:

Du har nu fundet gerningsgnomens hjemmeside, men dens indhold er kun overfladen. Julens politi mistænker, at yderligere information om eksfiltreret data kan gemme sig bag skjulte sider.

Brug OSINT-teknikker for at se, om du kan få adgang til disse skjulte sider og afsløre flere detaljer om, hvad der er blevet stjålet.

Kan du grave dybt nok til at finde den skjulte information?

## Approach

In our previous task, we found a bogus certificate:
![certificate](images/certifikat.png)

Let's extract any relevant information:
```text
$ openssl x509 -noout -text -in bitbibliotek.dk.crt
```

Output:
```text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            6c:ca:66:1e:35:25:49:d5:a9:f6:99:3e:5e:dc:0b:fe:22:ee:6d:8c
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = DK, ST = REGION SJAELLAND, L = Ringsted, O = Gnomerne Aps, OU = NC3{1nfiL7rAti0n_0g_3xf1ltr4t1on}, CN = bitbibliotek.dk, emailAddress = datagnasker@proton.me
```

The email address stands out as an interesting lead for an OSINT challenge.

#### Exploring the website

Before we dig into our `Datagnasker`, lets check out the [site](https://bitbibliotek.dk/) we found.

![bitbiblioteket](images/bitbilioteket.png)

Not much there, except some christmassy ASCII art.

Rather than attempting brute-force methods, I decided to focus on systematic OSINT investigation.

#### Following the threads

**1: Github**
A common first step in OSINT challenges is checking GitHub for user profiles. Searching for the email alias `datagnasker`
https://github.com/search?q=datagnasker&type=users

![Github](images/Github.png)

The user image matched our expectation – we’ve found the correct profile!

**2: Stack Overflow**
The GitHub profile lists a Stack ID. This led me to Stack Overflow:
https://stackoverflow.com/users/28085338/

![Stack overflow](images/stackoverflow.png)

There he is again.

**3: Twitter**
The Stack Overflow profile links back to GitHub and includes a Twitter reference:
https://x.com/BMadsen97204

![Twitter](images/Twitter.png)

This provided the user's real name, but the trail seemed to end there. I returned to GitHub to investigate further.

#### The github repository

The user only has a single repository: [web_test](https://github.com/datagnasker/web_test)

This repository seemed to contain a version of the site hosted at bitbibliotek.dk.

**Finding the Login Page**
Inspecting the [views.py file](https://github.com/datagnasker/web_test/blob/main/bitbibliotek/views.py#L20) revealed a potential login page - lets try that: https://bitbibliotek.dk/login

![Login](images/login.png)

#### Analyzing Commit History
A common technique for CTF challenges involving git repositories is to analyze commit history. The repository had 6 commits:
https://github.com/datagnasker/web_test/commits/main/

![Git commits](images/git-commits.png)

One commit titled "removed credentials" caught my attention:
https://github.com/datagnasker/web_test/commit/a21032da512c1a5852dd54297654dca64347d945

![Removed credentials](images/removed-credentials.png)

The commit revealed login credentials. I tested these on the live login page:

![Login with credentials](images/login2.png)

Success! Logging in revealed the flag:
![Flag](images/flag.png)

## Flag
NC3{g3m_4lDr1g_cR3d3nT1al5_i_g1T_r3P0}

## Reflections and Learnings

This challenge reinforced several key lessons about OSINT techniques and disciplined problem-solving:

1. Systematic Investigation: Brute-force attempts can be tempting, but following leads methodically often yields quicker and more reliable results.

2. Using GitHub search and commit history analysis provided clear, actionable paths.

3. Importance of Git Hygiene: Exposed credentials in a Git commit can lead to critical security breaches. Developers must ensure sensitive information is never committed to public repositories.

4. Leveraging Multiple Platforms: Combining information from GitHub, Stack Overflow, and Twitter emphasized the power of correlating data across platforms to uncover hidden insights.

5. Certificate Analysis: Extracting metadata, such as emails or organizational units, from certificates can provide valuable clues in OSINT-based challenges.

By approaching the task with patience and strategy, I successfully navigated through the clues to uncover the final flag. This challenge was an excellent reminder that effective OSINT relies on creativity, persistence, and attention to detail.