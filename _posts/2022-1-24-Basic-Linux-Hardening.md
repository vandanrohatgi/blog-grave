---
title: Linux Web server Hardening
tags:
- technology
- blueteam
image: /images/hard/info.jpeg
---

In this one I will try and harden a basic linux web server running apache. Hardening for those who may be unfamiliar, is the process of enforcing best security practices and configurations to decrease attack surface and increase your life expectancy by 5 years (due to reduced stress). 

Here is the [container I am using](https://hub.docker.com/_/httpd)

Specifications:

Server version: Apache/2.4.52 (Unix)

Linux d3bfa23f0b11 5.13.0-27-generic #29~20.04.1-Ubuntu SMP Fri Jan 14 00:32:30 UTC 2022 x86_64 GNU/Linux

I will be using [this checklist](https://www.ucd.ie/t4cms/UCD%20Linux%20Security%20Checklist.pdf). I found it has just the right amount of controls for me to experience how hardening a system goes about.

First I pulled a docker image of apache and deployed a basic webpage to it using:

{%highlight text%}
docker run -dit --name my-apache-app -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/ httpd:2.4
{%endhighlight%}

![](https://i.imgur.com/JHnquOt.png)

![](https://i.imgur.com/ftGMxmW.png)

Now you may wonder why? why did I make this page the way that I did? Because nothing is harder than Russian bass. Moving on...

We can now drop a shell on this docker container and start going through the checklist.

{%highlight text%}
docker exec -it my-apache-app bash

root@d3bfa23f0b11:/usr/local/apache2# ls
bin  build  cgi-bin  conf  error  htdocs  icons  include  logs	modules
root@d3bfa23f0b11:/usr/local/apache2# cd /
root@d3bfa23f0b11:/# ls
bin  boot  dev	etc  home  lib	lib64  media  mnt  opt	proc  root  run  sbin  srv  sys  tmp  usr  var
root@d3bfa23f0b11:/#
{%endhighlight%}

# 1. If machine is a new install, protect it from hostile network traffic until the operating
system is installed and hardened

We don't need to do anything for this step since the container is not exposed to the internet. Also I have the host firewall turned on so no other device even on my network can access this server until I switch off the firewall. For linux you can do

![](https://i.imgur.com/GPq6zNw.png)

# 2. Use the latest version of the Operating System if possible

As you can see above I am using Ubuntu 20.04.1 which is pretty recent I would say. Other than that always having the latest release (say Ubuntu 21) can lead to changes and hassle that can interrupt your services due to unseen bugs and lesser support since its a new release.

My say on this would be, to have a correct balance. Not too old and not too new.

# 3. Create a separate volume with the nodev, nosuid, and noexec options set for /tmp.

### Optional read start:
I feel like I should warn about the risk that comes with this rule. I followed [this guide](https://www.cyberciti.biz/faq/howto-mount-tmp-as-separate-filesystem-with-noexec-nosuid-nodev/) to perform this check. However, I did not try this on a real machine. I wasn't able to do it on a docker beacuse fstab(file system table) doesn't really work in the same way over there. So I tried on my wokring kali VM which was a huge mistake to say the least.

I made the changes as it said in the guide but when I rebooted the VM it said "Failed to mount /tmp". Now I know why this happened. I did mess with the /etc/fstab. Turns out, it is a very important file that is responsible to mount all the necessary volumes and the system does not boot without mounting /tmp. 

I then tried to recover my VM and found a good way to undo my changes. Basicaly mount the VM filesystem to my host and chroot into it. [Here is a pretty good guide](https://ubuntuhandbook.org/index.php/2021/05/mount-virtualbox-vdi-ubuntu/).

In the end I wasn't able to fix it but I was able to transfer the important stuff from it. 

### Optional read end.

This check basically creates a separate filesystem for /tmp to prevent it from filling up the whole current filesystem (resource exhaustion). The nodev prevents creating special files (that can be used to interact with the hardware), noexec prevents executing programs from /tmp (which may break some installation processes BUT the assumption here is that malicious actors only execute programs from /tmp) and nosuid prevents placing suid files in /tmp (SUID binaries can be used to escalate privileges).

I tried again with an ubuntu VM this time and only followed [this guide](https://www.cyberciti.biz/faq/howto-mount-tmp-as-separate-filesystem-with-noexec-nosuid-nodev/) till the part it says I have to edit the fstab file and it worked!!!

PS: I know the changes won't preserved If I don't change the fstab file but this is just a simulation of me hardening a server.

Here is me creating a script before making the changes:

![](https://i.imgur.com/Yam77B9.png)

And here is after I created a separate volume for /tmp and mounted with the noexec,nosuid and nodev permissions to it.

![](https://i.imgur.com/t3vrSw1.png)

# 4. Create separate volumes for /var, /var/log, and /home.

So just like the above check. We can create new volumes for /var , /var/log and /home and mounting them and finally editing their respective entries in fstab.

Like /tmp these directories are not usually world writable. So we only perform this check to protect system from resource exhaustion. For example /var/log getting too big and interrupting system functions by eating up all the space.

# 5. Set sticky bit on all worldwritable directories.

This check makes it so the directories where everyone has write access, cannot delete files owned by other users. We do this by adding the Sticky bit to those directories. Let's go over special permissions while we are at it:

1. SUID: when set on an executable, allows any user to execute that program with the privileges of owner user
2. SGID: when set on an executable, allows any user to execute that program with the privileges of the owner group
3. Sticky bit: When set on a directory, prevents any other user to modify that a file in that directory apart from root and the owner of a file.

Here is a scenario I created:
- I created two users test1 and test2.
- I made a world writable directory in test1 's home and created a file in it.
- test2 was able to delete this file.
- Now I added a sticky bit to it `chmod o+t /testdir`
- test2 was not able to modify the file in any way.

![](https://i.imgur.com/ej1UsZC.png)

![](https://i.imgur.com/tnTQsrn.png)

![](https://i.imgur.com/GfPWOfC.png)

![](https://i.imgur.com/7R01btl.png)

To be continued ...

