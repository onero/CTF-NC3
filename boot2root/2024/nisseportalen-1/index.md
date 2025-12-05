+++
title = 'Nisseportalen 1'
categories = ['Boot2Root']
date = 2024-12-15T13:33:38+01:00
scrollToTop = true
+++

## Challenge Name:

Nisseportalen 1

## Category:

Boot2Root

## Challenge Description:

Nissernes største ønske er en portal til deling af alle deres AI-genererede billeder aka Nisseportalen. Projektet er dog i fare efter Nissedevs utallige fiaskoer med både Dangerzone og Nissezonen.

Praktikantnissen har fået til opgave at redde Nisseportalen og få ryddet op i Nissedevs rod. Kan du hjælpe med at redde Nisseportalen og finde alle de sårbarheder, der må være, så projektet endelig kan blive gjort færdigt?

Men vær beredt, det er ikke til at sige hvad Nissedev har haft gang i...

[https://tryhackme.com/jr/nisseportalen2o24](https://tryhackme.com/jr/nisseportalen2o24)

## Approach

### Enumeration

We are to infiltrate the secret portal! As with the previous dynamic cgallenges, we start out with [the following nmap scan](https://explainshell.com/explain?cmd=sudo+nmap+-sC+-sV+-O+-p-).

```bash
Nmap scan report for ip-10-10-120-44.eu-west-1.compute.internal (10.10.120.44)
Host is up (0.00044s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.56 ((Debian))
|_http-server-header: Apache/2.4.56 (Debian)
|_http-title: Apache2 Debian Default Page: It works
MAC Address: 02:23:0A:F2:24:F7 (Unknown)
```

We find the portal server with two open ports and take note of port 22 (ssh) & 80 (http, usually a web app) being open!
This would ordinarily indicate that we need to exploit a webapp (often PHP-based) being hosted on an Apache server!

It is always a good idea to take a look at the webapp (even during scanning, as soon as we discover that port 80 is up!) to see if we can find any low-hanging fruit!

We are faced with the default Apache2 Debian page, which is not very helpful. We can try to run a [gobuster](https://tools.kali.org/web-applications/gobuster) scan to see if we can find any hidden directories.

![Apache2 Default Page](images/apache2.png)

```bash
gobuster dir -u http://nisseportalen.nc3 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt,bak,old

/.html                (Status: 403) [Size: 283]
/index.html           (Status: 200) [Size: 10701]
/.php                 (Status: 403) [Size: 283]
/portal               (Status: 301) [Size: 325] [--> http://nisseportalen.nc3/portal/]
/javascript           (Status: 301) [Size: 329] [--> http://nisseportalen.nc3/javascript/]
/.php                 (Status: 403) [Size: 283]
/.html                (Status: 403) [Size: 283]
/server-status        (Status: 403) [Size: 283]
```

We identify a `/portal` directory and navigate to it. We are greeted with a home page!

![Nisseportalen](images/portal.png)

### Getting first flag

Usually, the first flag is always hidden somewhere "simple", so it is always a good idea to check the source code of the page, /robots.txt, or any other hidden files.

We don't find anything in the source code, nor in the `/robots.txt` file, but something interesting about the /portal page is that we get redirected to index.php from a index.html!
When downloading the index.html file, we find the first flag in the comments!

```bash
wget -r -np -nd -A jpg,png,gif,php,html,txt http://nisseportalen.nc3/portal/
--2024-12-18 18:32:24--  http://nisseportalen.nc3/portal/
Resolving nisseportalen.nc3 (nisseportalen.nc3)... 10.10.58.96
Connecting to nisseportalen.nc3 (nisseportalen.nc3)|10.10.58.96|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 150 [text/html]
Saving to: \u2018index.html.1.tmp\u2019

index.html.1.tmp    100%[===================>]     150  --.-KB/s    in 0s

2024-12-18 18:32:24 (16.5 MB/s) - \u2018index.html.1.tmp\u2019 saved [150/150]

Removing index.html.1.tmp since it should be rejected.

FINISHED --2024-12-18 18:32:24--
Total wall clock time: 0.003s
Downloaded: 1 files, 150 in 0s (16.5 MB/s)
```

```html
<html>
  <head> </head>

  <body>
    <script>
      window.location.replace('index.php');
    </script>
    <p>NC3{Flag1:V3lkOmM3n_7IL_NI553POR74L3n}</p>
  </body>
</html>
```

Thanks to some simple enumeration, we can submit the first flag and move on to [Nisseportalen 2](/nc3/boot2root/2024/nisseportalen-2)!

## Flag

```text
NC3{Flag1:V3lkOmM3n_7IL_NI553POR74L3n}
```

## Reflections and Learnings

### Enumeration is Critical

This challenge underscored the importance of comprehensive enumeration in CTFs. Tools like nmap and gobuster proved essential for uncovering open ports, hidden directories, and sensitive files. Skipping enumeration can lead to missing straightforward solutions.

### HTML Source Inspection Pays Off

The ability to inspect and analyze HTML source code quickly led to uncovering the flag. This demonstrates that basic techniques, such as viewing page source, can sometimes yield valuable results without deeper exploitation.

### Think Like a Developer

Leaving a flag in a static HTML file highlights common mistakes developers make during testing or deployment. Identifying such oversights reinforces the value of thinking like a developer when probing for vulnerabilities.
