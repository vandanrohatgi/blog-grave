---
title: HackTheBox Traceback Write-Up
tags: 
- writeup
- hackthebox
image: /images/traceback/traceback.png
---

First write-up hype! I am still at noob level in hackthebox so I will be mainly posting easy-medium level machines. Traceback had components like OSINT, Web and security misconfigurations. Doing traceback took me a few days because I am not one of those monsters who rooted it in like 15 minutes **yet**.  

<!--more-->
<img src="/images/traceback/traceback.png" height="400" />

# Lets start!

So IP given to us is 10.10.10.181. Starting with basic nmap scan I don't use any special flags in the command, I just use defaults and set number of threads to 4 like

```

nmap -T4 10.10.10.181

Starting Nmap 7.60 ( https://nmap.org ) at 2020-08-15 10:03 IST
Nmap scan report for 10.10.10.181
Host is up (0.19s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 32.46 seconds

```

and now we can focus on scanning all the information about these two ports only

```

nmap -T4 -A -p22,80 10.10.10.181

Starting Nmap 7.60 ( https://nmap.org ) at 2020-08-15 10:05 IST
Nmap scan report for 10.10.10.181
Host is up (0.33s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 96:25:51:8e:6c:83:07:48:ce:11:4b:1f:e5:6d:8a:28 (RSA)
|   256 54:bd:46:71:14:bd:b2:42:a1:b6:b0:2d:94:14:3b:0d (ECDSA)
|_  256 4d:c3:f8:52:b8:85:ec:9c:3e:4d:57:2c:4a:82:fd:86 (EdDSA)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Help us
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.96 seconds

```

I like doing my scans this way because I think it is the most efficient as I can do my work side-by-side without waiting for scans to finish. We can see two ports open one is port 80(http) and other is 22(ssh). So now we know it is going to be something like either exploiting web server and getting shell directly or exploiting web server to get ssh keys. We browse to the web page and see a message.

<img src="/images/traceback/website.png" height="400" width="1000" />

Well looks like someone got here before us! The web-page has been defaced and looks like the hacker was kind enough to leave a backdoor for us. Now if only we had a clue about what it was... we can see the name of the hacker XH4H and upon further inspection we found another clue! 

<img src="/images/traceback/hint.png" height="600" />

Just googling these exact words we can see a twitter post with name that looks like that of the hacker who left the backdoor. 

<img src="/images/traceback/twitter.png" height="400" />

Following the link we fall upon a github repository full of [web shells](https://en.wikipedia.org/wiki/Web_shell). All thats left to do is just sit there and check for each and every shell in the web page of target. 

<img src="/images/traceback/shells.png" height="600" />

<img src="https://media.giphy.com/media/3o6wNNnyPHmruIClO0/giphy.gif" />

Bing! Bing! Bing! We got a hit on a shell named smevk.php

<img src="/images/traceback/login.png" height="600" />

Reading about the the shell from the github repository we find the credentials admin:admin (*ha! who would've thought*)

<img src="/images/traceback/smevk.png" height="600" width="1000" />

**optional read start**

Now here is when I started messing up because as you see there are a some files with the name php-reverse-shell. I thought that must be the intended way and looked up php-reverse-shells confident that this is what I need to do. So I git one from github (*I am not sorry*), enter my IP and port, upload it to the web server using the upload functionality in smevk shell, start a netcat listener and browse to my reverse-php-shell. Yay! I got a shell. Then I went and looked around in the home directory of webadmin and a file named authorized_keys in the .ssh folder. I cat it see there are a bunch of public ssh keys, I ignored them and went ahead to try and escalate my privileges to sysadmin(another user on the machine). And I was able to do it too but something didn't feel right because , to get to the sysadmin shell I had to perform all the above steps again and again. The ssh part which I ignored kept bugging me so I read up on usage of ssh and GUESS WHAT?! I was right! I didn't need any reverse shell or anything. More on that part below.

**end**

So I go to looked around the home directory of webadmin and found .ssh folder with a file name authorized_keys. I [generated my own ssh keys](https://docs.rightscale.com/faq/How_Do_I_Generate_My_Own_SSH_Key_Pair.html) and copy the contents of my id_rsa.pub and paste it at the end of other ssh keys present in authorized_keys.

Sure enough I am able to ssh into the machine now.
<img src="/images/traceback/webadminlogin.png" width="1000" />

I started to look into every readbale file in the dirstory and see a note.txt in webadmin which says 

```
- sysadmin -
I have left a tool to practice Lua.
I'm sure you know where to find it.
Contact me if you have any question.
```

Also I found a some clues in .bash_history 

```
ls -la
sudo -l
nano privesc.lua
sudo -u sysadmin /home/sysadmin/luvit privesc.lua 
rm privesc.lua
logout
```

I used  `sudo -l`  to see my privileges and found that I am able to execute a binary name luvit as the user sysadmin. Now it was clear that I had to make script to spawn a shell written in lua. It took me a quick google search and I made a file with content `os.execute('/bin/bash')` and then just use the command I found in .bash_history to execute it as the user sysadmin.

```

sudo -u sysadmin /home/sysadmin/luvit privesc.lua
```

And I am greeted with the sysadmin shell. I change into the home directory of Sysadmin and get the user flag. Now Here is the part I got stuck because I suck more than a vaccum cleaner at hackthebox and had to head on over to HTB forums for hints. I saw someone mention [pspy](https://github.com/DominicBreuker/pspy) and I was off to transfering it using my [preferred way](/2020/08/13/Python-and-how-I-useit.html#server). 

Once pspy was on the machine I executed it and saw something that was occuring quite frequently.

<img src="/images/traceback/pspy.png" width="1000" />

So I search what motd is and I quote manpages of ubuntu:

`UNIX/Linux system  adminstrators  often  communicate important information to console and remote users by maintaining text  in  the  file  /etc/motd,  which  is  displayed  by  the pam_motd(8) module on interactive shell logins.`

Very well I head on over to /var/backup/.update-motd.d/ to see if I can write anything to it but I didn't have the write permissions to it so I go to second best place i.e the motd directory in etc/. And I am going to just confess that I saw this technique somewhere else and just remembered how I can use it here.

<img src="/images/traceback/edit.png">

So I change into /etc/update-motd.d directory and see a bunch of scripts which had the privileges of root user :)

Well then I just added a line `cat /root/root.txt` at the end of the 00-header script.

<img src="/images/traceback/00-header.png">
Logged out of sysadmin and logged in again to be greeted wth contents of the root.txt.

<img src="/images/traceback/root.png">

Hope you learned something and as always I will post updates for new stuff on linkedin. Don't be shy to connect with me on linkedin :)

(Almost forgot... the location of the secret in previous blog is in the HTML of web page)
