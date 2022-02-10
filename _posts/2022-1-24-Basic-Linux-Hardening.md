---
title: Linux Web server Hardening
tags:
- technology
- blueteam
image: /images/hard/info.jpeg
---

In this one I will try and harden a basic linux web server running apache. Hardening for those who may be unfamiliar, is the process of enforcing best security practices and configurations to decrease attack surface and increase your life expectancy by 5 years (due to reduced stress). 

<!--more-->

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

# System Installation and Patching

## 1. If machine is a new install, protect it from hostile network traffic until the operating
system is installed and hardened

We don't need to do anything for this step since the container is not exposed to the internet. Also I have the host firewall turned on so no other device even on my network can access this server until I switch off the firewall. For linux you can do

![](https://i.imgur.com/GPq6zNw.png)

## 2. Use the latest version of the Operating System if possible

As you can see above I am using Ubuntu 20.04.1 which is pretty recent I would say. Other than that always having the latest release (say Ubuntu 21) can lead to changes and hassle that can interrupt your services due to unseen bugs and lesser support since its a new release.

My say on this would be, to have a correct balance. Not too old and not too new.

## 3. Create a separate volume with the nodev, nosuid, and noexec options set for /tmp.

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

## 4. Create separate volumes for /var, /var/log, and /home.

So just like the above check. We can create new volumes for /var , /var/log and /home and mounting them and finally editing their respective entries in fstab.

Like /tmp these directories are not usually world writable. So we only perform this check to protect system from resource exhaustion. For example /var/log getting too big and interrupting system functions by eating up all the space.

## 5. Set sticky bit on all worldwritable directories.

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

## 6. Ensure the system is configured to be able to receive software updates

So Ubuntu comes with the ability to get updates by default. Just do a quick `sudo apt update && apt upgrade` when you first install the system.

you can use [this guide](https://www.cyberciti.biz/faq/how-to-set-up-automatic-updates-for-ubuntu-linux-18-04/) to automatically install new updates. Be carefull while going through it. It also guides you to automatically reboot without any alert. It is more suited for servers and not daily drivers.

# OS Hardening

## 1. Restrict core dumps

Core dumps contain debug info about any crashes that might occur. As seen from out past experiences we know that debug logs can expose a lot of sensitive information (at least that's what the CTFs said). 

Again this rule only is for production Servers and not development environment or home labs. Core dumps are needed to debug and get a sense of what went wrong.

We can disable core dumps using `ulimit` command. It is used to set limits to resources that can be used by various functionas. For example set limit to concurrent user processes, maximum memory size etc. [Here's an awesome guide](https://www.geeksforgeeks.org/ulimit-soft-limits-and-hard-limits-in-linux/) along with [another good one](https://linuxhint.com/permanently_set_ulimit_value/).

Ulimit has 2 types of limits:
- soft: the actual limit that is used for processing
- hard: the upper bound (i.e maximum) of the soft limit

To persist these changes we have to edit the `/etc/security/limits.conf` and add something like 

`* soft core 0`

`* hard core 0`

![](https://i.imgur.com/0RxWWE2.png)

You can see after I changed "unlimited" to "0" the coredump was not created. (To see all limits, do `ulimit -a`)

# 2. Remove legacy services

Simple check to perform. Just run a command like:

`sudo apt-get --purge remove xinetd nis tftpd tftpd-hpa telnetd rsh-server rsh-redone-server ypserve ypbind-mt talk talkd`

# 3. Disable any services and applications started by xinetd or inetd that are not being utilized. Remove xinetd, if possible

We can include xinetd service in our previous check. I looked up xinetd and found an installation guide from 2007 so it is indeed pretty old. I did however find it interesting. It basically started the server whenever a request came in. If no requests arrive the server remains off.

# 4. Disable or remove server services that are not going to be utilized

(At this point I realized that the docker container is very different from a virtual machine environment, since many services are configured a lot differently. I decided to follow the rest of the checks with an Ubuntu VM.)

To perform this check you can first check for installed services using: `systemctl list-unit-files`

![](https://i.imgur.com/m98X8sj.png)

And remove services you don't need likewise.

# 5. Ensure syslog (rsyslog, syslog, syslog­ng) service is running.

Use Systemctl to check if (any of the above) rsyslog,syslog or syslogng are running or not. If not then use `systemctl start rsyslog`

![](https://i.imgur.com/5w6mcVS.png)

# 6. Enable an Network Time Protocol (NTP) service to ensure clock accuracy

I was unsure about how this one was related to security. Then i read further and saw that it is indeed very important to have the right time. It helps in analyzing log files in case of any incident.

[Here is the guide I followed](https://linuxconfig.org/ubuntu-20-04-ntp-server)

Pretty straight forward. Install ntp, configure it according to your use and run using systemctl.

To configure, just add the region closest to you. for example:

server 0.in.pool.ntp.org
server 1.in.pool.ntp.org
server 2.in.pool.ntp.org
server 3.in.pool.ntp.org

add this to /etc/ntp.conf and restart the service.

![](https://i.imgur.com/HoKsuBl.png)

# 7. Restrict the use of the *cron* and *at* services

Since these scheduling services can run commands which we have seen from numerous HTB machines. We should restict the use for these only for accounts that need it.

[Another great guide](https://www.cyberciti.biz/faq/howto-restrict-at-cron-command-to-authorized-users/) by cyberciti.biz 

Basically we just need to edit the cron.allow to define users that can modify/create cron jobs. If the user is not listed in cron.allow then he/she can run that cron job but not modify it. cron.allow only defines access to the crontab command which is used to create/modify jobs. Similarly we can define users for *at*.

![](https://i.imgur.com/lAroZv4.png)

Before making the changes I was able to create cronjobs for my user "sandbox". But after I added just the user "root" to cron.allow I was not able to create anymore jobs. Take note that I can still run jobs with the privileges of user "sandbox" but to create that job I will need to use the user "root".

# User Access and Passwords

## 1. Create an account for each user who should access the system

Makes sense. Sharing accounts is going to make incident response and debugging a living hell. Also a quick one if you have groups already made, So you can just create a user and add them to the respective groups to provide needed privileges.

`useradd -m sandbox2` (add -m only if you want to create a home directory for that user)
`gpasswd -a sanbox2 sudo` (add sandbox2 user to sudo group)

![](https://i.imgur.com/tLnEb5M.png)

![](https://i.imgur.com/3LHXcQL.png)

[Here's a full guide](https://linuxize.com/post/how-to-create-users-in-linux-using-the-useradd-command/)

## 2. Enforce the use of strong passwords

To perform this check we have install a package "pwquality". It helps enforce password policies in linux. The guide I provide below is very staright forward. Just do as it says. Only doubt you may have would be that why are we assigning negative numbers like `ocredit=-2` in password policy. 

That is because this will do 2 things. one is that it will enforce minimum number of symbols in password to 2. Second it will make sure that the 2 symbols do not count towards the minimum length. So the effect minimum length is 10 if minimum length is 8 and minimum symbols is 2.

[Here is the awesome guide](https://linuxhint.com/secure_password_policies_ubuntu/)

![](https://i.imgur.com/7zoZDeB.png)

## 3. Use sudo to delegate admin access

We just added a user to a sudo group in the the first check of this section.

To add:

`gpasswd -a sandbox2 sudo`

To remove:

`gpasswd -d sandbox2 sudo`


# Network Security & Remote Access

## 1. Limit connections to services running on the host to authorized users of the service via firewalls and other access control technologies

In this check we will configure a basic Firewall. "UFW" (uncomplicated firewall) can be found in many GNU systems. Lets do some basic rule config.

First let us see the current rules of the firewall.

[As always, here is what I followed](https://www.cyberciti.biz/faq/how-to-configure-firewall-with-ufw-on-ubuntu-20-04-lts/)

![](https://i.imgur.com/WNKbyNW.png)

Apache is allowed to be accessed from anywhere. Makes sense if you want a public web server. 

Next let's add a rule so that connections from only specific IP addresses can access our SSH server.

![](https://i.imgur.com/5rR7LYH.png)

Now suppose we just got IOC (indicator of compromise) from Threat intel team and they advised us to block traffic from IP from `10.10.12.2`

![](https://i.imgur.com/zYKHZK6.png)

Now let's add a final rule to rate limit the connections on Apache to deny connections from attackers who brute forcing for credentials or secrets.

![](https://i.imgur.com/WS68vup.png)

We just made the world a safer place. Let's move to the next check.

## Disable IP forwarding,packet redirect... Enable Broadcast request ignore, TCP/SYN cookies...

### Disable

- IP Forwarding: Done when the linux server is acting as a router or a border devices and is needed to forward packets to other devices. To be disabled to stop bandwidth wastage and remove excess features that may come in handy for a threat actor.

note: All the changes in this rule will be done in /etc/sysctl.conf

`net.ipv4.ip_forward=0`

- Redirects: ICMP redirect can lead to Mitm attacks. [Here is a good read](https://blog.zimperium.com/doubledirect-zimperium-discovers-full-duplex-icmp-redirect-attacks-in-the-wild/)

net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.all.send_redirects=0

![](https://i.imgur.com/0V5dWJt.png)

- Source routed packet acceptance: source based packets use a list of all IPs to go via to reach a final destination. You can tell this can be used to exploit some fom of trust relationship in a network. 

net.ipv4.conf.all.accept_source_route=0

- ICMP redirect: we already disabled this in the above check.

### Enable

- Ignore Broadcast requests: Basically remember when we try to ping an entire subnet for alive hosts during HTB machines? To stop machines from responding to that, we can enable this option. 

net.ipv4.icmp_echo_ignore_broadcasts = 1

- Bad error message protection: Alerts about all the bad/unusual error messages in network

net.ipv4.icmp_ignore_bogus_error_responses = 1

- TCP/SYN cookies: these cookies are used to protect from syn flood attacks. Basically anytime a syn packet comes in no connection is established. Only when ACK is received from client the connection is put in a queue, and hence the queue is not filled up with half connections.

[read in detail here](https://www.geeksforgeeks.org/how-syn-cookies-are-used-to-preventing-syn-flood-attack/)

net.ipv4.tcp_syncookies=1

## 3. In the SSH server configuration ensure that:

These configs are enabled by default when ssh is installed. Let's just go over their rationale quickly.

- Protocol version is set to 2

When we do a `ssh -v localhost` it displays all the debug info. And we can see we already have ssh v2 by default.

![](https://i.imgur.com/j3h1qbW.png)

- LogLevel is set to INFO

To get as much detailed info as from logs as possible. Inside `/etc/ssh/sshd_config` set:

LogLevel INFO

- PermitEmptyPasswords is set to No

To prevent unauthorized access. For example if any user is having empty password anyone can login to that user without any password on that system.

Inside `/etc/ssh/sshd_config`:

PermitEmptyPasswords no

## 4. Disable root login over SSH

Pretty straightforward. Allowing login to root is always bad. even if someone doesn't know the password they can always brute force it or steal required authentication material. Use sudo for root access always.

Inside `/etc/ssh/sshd_config`:

PermitRootLogin no

## 5. Deploy an Intrusion Prevention System (IPS) such as fail2ban

fail2ban is linux tool to handle bruteforce attacks on servies like ftp,ssh,smtp... [I used this guide to install and configure fail2ban](https://linuxize.com/post/install-configure-fail2ban-on-ubuntu-20-04/).

We used UFW to rate-limit our apache server. Lets use f2b to secure our ssh server. (fail2ban has a lot of options like sending mail alert,contacting cloudfare,customization etc for many services like apache,squid,smtp etc. Be sure to explore!)

Here is what I configured for my ssh:

{%highlight text%}
[sshd]
enabled=true
maxretry=3
findtime=5m
bantime=4w
{%endhighlight%}

maxretry is amount of times failure is allowed. you can set it according to real world experience like what is the typical amount of times an average Joe takes to login.  

findtime is time in which failures occured. This is very critical. If its too less then threat may just rate-limit their brute force. If It is too less, then normal brute force is not going to be stopped.

I didn't chose to ignore any IP because well... what if the threat is already inside our network and is just trying to move laterally.

And bantime is self explainotary. (pardon my spelling btw)

You can also use fail2ban-client to set these rules. Another use for it is to unban legitimate users if you work in the IT dept.

# Apache Webserver (HTTPD)

## 1. Always run apache with a dedicated non admin account

This is done by default. Apache runs as user "www-data" which is compliant with the check. The user for apache can be changed with `/etc/apache2/envvars`

export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data

## 2. Disable any modules not required

[guide](https://www.simplified.guide/apache/enable-disable-module)

Simple enough. apache uses modules to extend its functionality. Lets see if I have any unnecessary modules loaded.

`apachectl -M`

![](https://i.imgur.com/KPutCG8.png)

OH! how did that get there. (certainly not me, must be dave from IT) Let's disable it.

![](https://i.imgur.com/x7AfXrv.png)

Similarly, you can disable any other module that you don't need.

## 3. Disable HTTP Trace: TraceEnable 

Te 'trace' header basically reflects the entire request back to the client for debugging purposes. You can see how that can leead to a quick and easy XSS. By default this option is now disabled.

![](https://i.imgur.com/7Mz9X7U.png)

## 4. Configure Apache not to advertise the software/OS versions

[guide](https://www.tecmint.com/hide-apache-web-server-version-information/)

before:

![](https://i.imgur.com/4d3nBub.png)

after:

![](https://i.imgur.com/BxGrXuZ.png)

## 5. Deny access to files by default ­ only allow access to designated directories.

Last and final check of this blog. I created an example file on server and now lets restrict access to it.

![](https://i.imgur.com/KshO5D0.png)

![](https://i.imgur.com/v09iQdh.png)

{%highlight text%}
<Files ~ "\.txt$">
    Order allow,deny
    Deny from all
</Files>
{%endhighlight%}

Similarly access can be delegated for any file/directory. First we define order to process the allow and deny rules and then we deny access from all.

And that is about it for this one. We finally have a pretty secure machine. Ofcourse nothing is ever fully secure but you can always do your best :)