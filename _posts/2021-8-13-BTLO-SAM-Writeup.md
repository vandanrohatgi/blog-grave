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

Starting from the top. I tried looking around for any suspicious activity inside the sysmon logs, pcap files and memory dump. While going through the PCAP file I decided to look at the all the objects from the HTTP protocol and I found an enumeration script.

<img src="/images/sam/jawsenum.png" width="700">

Along with it, I also got a possible IP address. After that I decided to go on a hunt for activity from this IP. While going though the sysmon logs I finally found the reverse shell activity.

<img src="/images/sam/sysmonreverseshell.png" width="700">

Next we need to find the malware that initiated this reverse shell. We can see that the process ID of reverse shell is 5056. So we just need to find its parent process ID so that we can get the file that spawned that process. 

<img src="/images/sam/payload.png" width="700">

So now we search for the process ID 3888. Also we have found the powershell payload along the way.

<img src="/images/sam/parentprocess.png" width="700">

Now the scenario is starting to become clearer. The user downloaded a malicious file and made the mistake of opening it. A double click was all it took to run the malicious ".hta" file and spawn a powershell to run further commands and give the attacker a reverse shell. Now we have the malicious file too. 

".hta" files are automatically run using the "mshta.exe" program. It is very convenient for attackers as mshta.exe is a binary that is signed by microsoft hence reducing suspicion. 

To find how this payload was generated we can do a quick google search if we don't have much idea about msf-venom. In this case the flag "hta-psh" was used to create a malicious hta file that will spawn powershell. Moving on we can answer the next question by either reading the fully decrypted payload or doing a quick google search again.

TO extract the payload I did some bash-fu and then decrypted it using Cyberchef. 
 
<img src="/images/sam/extractPayload.png" width="700">

<img src="/images/sam/decodedpayload.png" width="700">

[This helped](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.processstartinfo?view=net-5.0)

And for the compression stream used we can again refer to the decoded payload and look for a stream name. Now we need to give the number of hashes that were stolen form victim. I could have tried to find the SAM files in wireshark but I took the lazy way out and just listed all the hashes using volatility.

<img src="/images/sam/hashes.png" width="700">

Now we need to crack the hash for user SAM and Admin. Again I could have used cyberchef but there are better ways to crack hashes available online. I used [hashes.com](https://hashes.com/en/decrypt/hash). 

Finally we need to find what the adversary did using the passwords. I already knew the IP so I again looked for it in the sysmon logs.

<img src="/images/sam/ssh.png" width="700">

So the adversary just logged into the victim machine using SSH in the end. For the final question we need to give the name of any other scripts that were run. We already found out the name for this script in the beginning.

This was a really fun Investigation. 
I have tried not to give straight up answers because that is no fun. 
It took me about 3-4 weeks of distributed time to get this done. 
And I will see you in the next one!
