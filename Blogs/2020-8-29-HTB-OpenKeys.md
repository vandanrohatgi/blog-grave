---
title: Hack the Box OpenKeys Writeup
tags:
- hackthebox
- writeup
image: /images/openkeys/info.png
---

Welcome to another writeup! You know I just read some other writeups today and... boy! my writeups are wayyy too informal and contain a lot of junk. Well it's not like anything's gonna change. If I start writing boring and to the point writeups like everyone else then that will probably my last blog. If I am not enjoying the process then I don't think there is any point in me even doing that thing. Steering the conversation to the machine OpenKeys, even if this was my first medium level machine... I didn't feel too out of place because it followed the same old hackthebox pattern. You will know what I am talking about in a minute.
<!--more-->

<img src="/images/openkeys/info.png" />

It was my first medium level as well as my first OpenBSD machine. But I didn't really feel any difference. Starting with basic nmap.

```
nmap -T4 -Pn 10.10.10.199

Nmap scan report for 10.10.10.199
Host is up (0.43s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 73.97 seconds
```

See what I was talking about? There is a web server and a ssh server...I wonder what I need to do. (*please pick up the sarcasm*). Browsing to the webpage.

<img src="/images/openkeys/website.png" width="1000" />

So we see a login form. So I tried little bit of sql injection and os command injection and did'n't get anything. Next I look at the source html and javascript.

Found nothing in the html but there was a lot of functionality like moment.js and much more stuff that didn't relate to a simple login form. Noted and moving on I fire up Dirbuster with common.txt.

<img src="/images/openkeys/dirb.png">

The folder `/includes` stood out to me and I was right! it had something interesting. 

<img src="/images/openkeys/includes.png" />

Browsing to auth.php did nothing so I tried to give it some random username and password parameters with the GET request. All I saw was an empty screen and a bleak future. 

But! Don't give up soldier! All is not lost yet! There was another file named auth.php.swp. I browse to it and see bunch of source code for auth.php

```
b0VIM 8.1
jennifer
openkeys.htb
/var/www/htdocs/includes/auth.php
3210
#"! 
    session_start();
    session_destroy();
    session_unset();
function close_session()
    $_SESSION["username"] = $_REQUEST['username'];
    $_SESSION["user_agent"] = $_SERVER['HTTP_USER_AGENT'];
    $_SESSION["remote_addr"] = $_SERVER['REMOTE_ADDR'];
    $_SESSION["last_activity"] = $_SERVER['REQUEST_TIME'];
    $_SESSION["login_time"] = $_SERVER['REQUEST_TIME'];
    $_SESSION["logged_in"] = True;
function init_session()
    }
        return False;
    {
    else
    }
        }
            return True;
            $_SESSION['last_activity'] = $time;
            // Session is active, update last activity time and return True
        {
        else
        }
            return False;
            close_session();
        {
            ($time - $_SESSION['last_activity']) > $session_timeout)
        if (isset($_SESSION['last_activity']) && 
        $time = $_SERVER['REQUEST_TIME'];
        // Has the session expired?
    {
    if(isset($_SESSION["logged_in"]))
    // Is the user logged in? 
    session_start();
    // Start the session
    $session_timeout = 300;
    // Session timeout in seconds
function is_active_session()
    return $retcode;
    system($cmd, $retcode);
    $cmd = escapeshellcmd("../auth_helpers/check_auth " . $username . " " . $password);
function authenticate($username, $password)
<?php
```


Also I found that .swp extension is used by the editor vim as probably a form of cache. We see that There is an interesting System() function in there. Smells like rce to me. But there was also a bitter escapeshellcmd() function in there too. Blehhk...

For those unfamilier [System](https://www.php.net/manual/en/function.system.php) function in php is used to execute commands and [escapeshellcmd](https://www.php.net/manual/en/function.escapeshellcmd) function is used to escape the characters in a given string that might be used to chain shell commands. It is used mostly before passing a string from user to System() function.

So that takes RCE out of the equation. Back to sqaure one. We also see a name "jennifer" in there which is going to be useful. Digging even deeper we see a binary with name check_auth and we can browse to it! browsing to `/auth_helpers/check_auth` we can download the binary. 

When we try to run it on a non OpenBSD system it doesn't work. We can still investigate it though. I fire up Cutter and tried to debug by decompiling it but the binary didn't have any functional code in there! It was just jibber jabber. Hmmm... There must be something. So I go back to simple techniques like running [strings](https://linux.die.net/man/1/strings) on the binary. 

```
/usr/libexec/ld.so
OpenBSD
libc.so.95.1
_csu_finish
exit
_Jv_RegisterClasses
atexit
auth_userokay
_end
AWAVAUATSH
t-E1
t7E1
ASAWAVAT
A\A^A_A[]
ASAWAVP
A^A_A[]L3
Linker: LLD 8.0.1
--snip--
```

Nothing stands out. Then I remember that the box was CVE based and we can see some stuff here with version number along them. I knew what I had to do...I put on my black hoodie, fire up the neon green terminal, switched off the lights and start googling all these with the word "exploit" after them.

And I do end up with good amount of articles with vulnerabilities related to authentication bypasses and local privilege escalations. And now starts the hardest part of this machine. Both the user and root took a CVE to be exploited. Finding the right one took me some time. Finally I [found one](https://www.secpod.com/blog/openbsd-authentication-bypass-and-local-privilege-escalation-vulnerabilities/). According to this article there was an authentication bypass vulnerability. When we used the username "-schallenge" we were able to login without a password.

Lets explain this CVE with an example:
I have binary name auth. auth takes arguements in the form of:

`auth -flag username password`

If we provide the username or password in the form of a flag like `auth -options -bypass password` we can pass an arguement to the binary and if the binary has some flag to skip the authentication then we are able to login without logging in!

So I do that on the original login form and try "-schallenge" as username and "anything" as password. It worked and we are able to log in.

<img src="/images/openkeys/keynotfound.png" />


Looking at this text triggered something inside me. Like I have done this before (I have played capture the flags before). So I take a look at  the cookie section. 

<img src="/images/openkeys/ocookie.png" />


Hmm... Lets try adding a cookie with value something like user:jennifer. After a few tries it really did work.

<img src="/images/openkeys/modcookie.png" />

Refreshing the page. Drum Roll please!......

<img src="/images/openkeys/sshkey.png" />

So now we have the ssh keys for jennifer. Trying to log in with those keys we are able to get a connection and we can see the flag in user.txt

Moving to escalating my privileges.

We can't use `sudo -l` because we don't know the password so I search for suid binaries. I find some like `chpass chsh` but they were not of any use. I remember that I saw lot of privilege escalation exploits while I was looking for exploits. Finding authentication bypass was hard but this was harder. Referring to this [article again](https://www.secpod.com/blog/openbsd-authentication-bypass-and-local-privilege-escalation-vulnerabilities/) I see 3 LPEs and one Authentication bypass that we already used. I try all three of them but to no success. 

We already know that we are dealing with OpenBSD 6.6 (I found it when I was searching about all the keywords from the output of `strings`).
So I start finding exploits for LPE again. I try [this](https://www.exploit-db.com/exploits/47780) exploit-db script but that wasn't it either. Finally I start searching on github and I [found something](https://github.com/bcoles/local-exploits/blob/15874c8d1e42bc49e9aef63f611b7fec866d5a79/CVE-2019-19520/openbsd-authroot). It is CVE-2019-19522 which finally worked for me. 

Using the script was simple. I just transferred it to the machine, ran it and entered the password which it told me to. Doing that got me to root. Not very exciting was it?

<img src="/images/openkeys/root.png" />

Lets try and understand what the script is doing as much as possible

- First of all... Looking at the [exploit script](https://github.com/bcoles/local-exploits/blob/15874c8d1e42bc49e9aef63f611b7fec866d5a79/CVE-2019-19520/openbsd-authroot) we see that we are not using one **but two CVEs** to get root access i.e CVE-2019-19520 and CVE-2019-19522.
- CVE-2019-19520 is used to exploit a vulnerability in the [xlock](https://man.openbsd.org/xlock) program found in OpenBSD. It is basically a locking system for OpenBSD systems. We use that CVE to get the privileges of the the group "auth". I tried reading the script for how it exploited this but didn't really get anything. So I decided to move on to the next part.
- But why do we need the privileges of group auth? Do we not need to get root? This is where the next CVE-2019-19522 comes in. We will use the vullnerability found in the [skey](https://man.openbsd.org/skey.1) program of OpenBSD.
- Skey is a OTP based authentication for OpenBSD. It can be used to login as any user as long as you know the one time password for it. And this is why we achieved the privileges of the auth group because auth group has the privilege to make a new password of our choice for any user.(yes even root) 
- So the script does exactly that, it makes a new password for the root user and tells us what the password is. Now all we need to do is use that password and login as user root.

So even if I didn't learn any fancy tricks in this box, I learned about OpenBSD, importance of taking notes because those articles were confusing as hell and I definitely liked reading about how those CVEs work. Hope you learned something too and I will see you in the next one. Peace out!