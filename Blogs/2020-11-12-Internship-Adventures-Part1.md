---
title: Internship Adventures Part 1
tags: 
- internshipAdventures
image: /images/internship1/info.jpeg
---

Alright folks! I think I have enough content to write about my time as an intern. Apparently my profile is of a "security analyst intern" and I have absolutely no idea what I am doing. I will just write about different vulnerabilities or anything interesting really. In this one I will write about critical vulnerabilities I found on some web applications. Lets get done with this quickly because I got big backlog of HTB boxes I need to root.

<!--more-->

<img src="/images/internship1/info.jpeg">

## Git directory disclosure leading to SMTP server takeover

While performing the usual directory busting on the target using dirsearch I found a ".git" directory.

<img src="/images/internship1/git.png">

I tried to get the whole directory using recursive wget on the whole thing. It didn't work.

<img src="/images/internship1/pikachu.jpeg">

Ofcourse it didn't work because ".git" directories are not normal ones.You can't just wget them. Finally my mentor told me to use a special tool known as ["GiTools"](https://github.com/internetwache/GitTools) (surprise surprise...). 

Next I used the Dumper in the tool to dump the whole .git directory to my machine. 

<img src="/images/internship1/dumper.png">

Now we can start working on getting the source code back from the .git directory. 5 minutes of google search and I find that just doing `git checkout -- .` will be enough to give me the source code.

Just a little browsing around the source code I find credentials for mysql database and the SMTP server. I was ecstatic because I knew there were SQL and SMTP servers where I can try these creds (From my already performed Nmap scans). The SQL creds didn't work probably because remote login was disabled. Moving to SMTP creds. 

To test the SMTP creds I followed [this article](https://www.ndchost.com/wiki/mail/test-smtp-auth-telnet). Yeah... as you might have guessed that didn't work. Nothing works till there is a twist. My mentor came in clutch again and told me to try them using a email client like ThunderBird for linux. 

With some basic login configurations at the startup I was able to login to the company's official email account! Ever saw those emails that look like "noreply@company.com"? Yep. I was now able to send anyone any mail as the company itself!

That was my first ever critical vulnerability. The only catch was that the company was not very mature in terms of security and that was why a n00b like me was able to pull off those things. Moving on to the next vulnerability.

## Critical PII leak

So this one was not very technical and not as exciting. Just good ol' recon. This was found on another target. I was browsing around and something I always do is take a quick glance at the HTML source. I found a image tag loading an image from a directory that I haven't seen before. I browsed to the image folder and see a bunch of other directories. One of them named "employee" caught my eye.

When looked inside that directory I found tons of aadhar cards just waiting there to be found. For those who don't know what aadhar cards are, It acts as a unique identifier for citizens of India. 

## OTP Bypass

This one was found on the same target as the previous one. Basically I tried to login using mobile number and saw one of the requests was returning the otp and the javascript was performing the checks on client side. Bad move... Never do anything like that on client side. 

<img src="/images/internship1/otp1.png" width="1000">

## Miscellaneous Vulns

I found a time based SQL injection on one of the GET parameters in the request. Also There was a Reflected XSS on the simple search functionality. So what I am trying to say is that none of the targets were very mature so I had field trip finding those vulnerabilities one after another.

Ofcourse I must have probably have left out many and was just able to grab the low hanging fruit for now. Compared to my experience during Bug bounties where just one week was enough for me to leave it altogether and never coming back, It was quite the confidence booster.

Well thats about it of what I was able to collect in one month. Heres to many more to come!

