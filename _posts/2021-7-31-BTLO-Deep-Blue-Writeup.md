---
title: BTLO Deep Blue Writeup
tags:
- blueteam
image: /images/deep-blue/info_blue.png
---

Hey there stranger! Long time no see. **Now ensues the part where I describe why I haven't been posting. Skip to the next heading if you don't care**. So Now I work as a SOC Analyst intern. Now, I wanted to do a blog where I document all the things that I do at work like, how I respond to alerts, How I make decisions, Some example cases etc. (I had already started doing that) But then I thought that the information would probably count as sensitive and I shouldn't disclose it. Like any malicious adversary can just read up my blog and find ways around it to attack the client infrastructure. 

<!--more-->

And hence I decided to just discard that idea. But since now I do the defensive stuff I can always do writeups about investigating, forensics challenges etc. Which brings us to the topic of today's blog. Blue Team Labs is just like a blue version of Hackthebox. It has challenges and Investigations. So Let's start with the Investigation named "Deep Blue".

## Deep Blue

The investigation is named so because we need to use a tool name ["Deep blue"](https://github.com/sans-blue-team/DeepBlueCLI) which analyzes windows event logs and automatically detects suspicious activities. So when we start an investigation we are faced with a in-browser desktop which has all the tools we need. 

Lets start with the scenario given to us:

*A Windows workstation was recently compromised, and evidence suggests it was an attack against internet-facing RDP, then Meterpreter was deployed to conduct 'Actions on Objectives'. Can you verify these findings?
You have been provided with the Security.evtx and System.evtx log exports from the compromised system - you should analyze these, NOT the Windows logs generated by the lab machine (when using DeepBlueCLI ensure you're providing the path to these files, stored inside \Desktop\Investigation\.*

<img src="/images/deep-blue/desktop-blue.png" width="500">

Lets look at the files provided.

<img src="/images/deep-blue/folder.png" width="500">

So a bunch of logs and tools. Now we need to use these to answer some questions which can be thought of flags that we used to submit.

<img src="/images/deep-blue/ques.png" width="700">

Let's start with looking at our files.

<img src="/images/deep-blue/readme.png" width="500">

It gives us a small introduction to what we need to do. Starting with the question in order we first need to use deep-blue to find who ran the file `GoogleUpdate.exe`.

<img src="/images/deep-blue/1.png" width="1000">

We can do that by just looking at the output of deep-blue or we can use a windows alternative to "grep" in linux.

<img src="/images/deep-blue/select-string.png" width="1000">

A little more complex than linux but it worked. Moving to next we need to find meterpreter activity from the logs. This was quite easy too since deep-blue just does that for us.

<img src="/images/deep-blue/2.png" width="700">

I took this chance to finally learn how the "get system" command works in metasploit. Usually it is done after you have a foothold on the victim machine and try to elevate your privileges to the "Administrator". [From Here](https://docs.rapid7.com/metasploit/meterpreter-getsystem/#:~:text=In%20this%20technique%2C%20Meterpreter%20creates,makes%20you%20the%20SYSTEM%20administrator.) I can understand that Windows uses pipes as a means of communication between processes. What metasploit does is try to create a new named pipe and communicate with the cmd.exe process. Now since all the pipes in windows run with admin privilege we can try and impersonate an admin by sending data to cmd.exe through named pipes.

And hence deep-blue caught the command that metasploit uses to create a named pipes. 

<img src="/images/deep-blue/3.png">

Moving to next question we need to give the name of malicious file that probably started all this. This time we use the event viewer which shows all the logs in a GUI. We will also need to apply time based filters to narrow down our search. 

<img src="/images/deep-blue/eventviwer.png" width="500">

<img src="/images/deep-blue/filter1.png" width="500">

It was quite easy to find since a file named "serviceupdate.exe" just doesn't fit right, especially when its located in the Downloads folder. 

<img src="/images/deep-blue/4.png" width="700">

In the same way we need to find the account that was created to maintain persistance on the machine using time filters.

<img src="/images/deep-blue/5.png" width="700">

Finally we need the name of groups that the user was added to to complete persistance.

<img src="/images/deep-blue/6.1.png" width="700">

<img src="/images/deep-blue/6.2.png" width="700">

And we are greeted with the celebration screen. It was a nice break from doing all the red team stuff. I will try and post more when I am able to figure out the next investigation that I'm working on. See ya!



