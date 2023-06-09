---
title: Internship Adventures Part 2
tags: 
- internshipAdventures
image: /images/internship1/info.jpeg
---

Well, here we are with the second part already. But this time I was actually able to find vulnerabilities that snuck past even my seniors. I know the second part took too long but my role in the internship is not only to test webapps, I also work on a project for the company in parallel. Anywho... the vulnerabilities I found were critical in nature and I learned a lot from them. That's right ya boi is finally able to find decent vulnerabilities!  

<!--more-->

<img src="/images/internship1/info.jpeg">

## Critical Information Disclosure

The target was a pretty big deal and was quite mature in terms of security. It had a quite a few subdomains and assets. There were a lot of login screens. After basic testing of those I moved on to some more recon. I found they had a github account but no luck there. The website was running an outdated version of wordpress(Informed by the trusty [wappalyzer extension](https://www.wappalyzer.com)) but it was patched and the known exploits didn't apply to our testing case. 

After further recon I tried some good ol google dorking (By the time I was done with it I had a few vulnerabilities and the suspicion of google that I am a robot). First thing I wanted was the subdomains indexed by google. So I did this...

`site:domain.com -site:www.domain.com`

See what I did there? I wanted the subdomains of the domain but didn't want the main webapp in my results. So the `site:domain.com` was to get all the results that included my desired domain. `-site:www.domain.com` was so that it doesn't give me the "www" subdomain that I didn't want. 

As expected I got a bunch of results and some were not even there in  my sub-domain enumeration. I manually visited them. In the last page of the results I found a sub-domain which sounded *very very* juicy. It had the url in the format "http://crm.staging.domain.com/". I tried opening the URL but it gave me "404 Not Found".

Hmm... They must have served only for a few moments or it was some sort of mistake. It was enough for google to index it before they took it down. I felt like something like that must have been cached somewhere if it had enough time to get indexed. The next dork I tried was:

`cache:http://crm.staging.domain.com`

*Well Well Well... Hello Beautiful*. The page **was** cached and to my luck it had all sorts of critical data. It had info about SMTP server, Logs, Credentials to their ios and android APIs, The whole structure of their tables as well the all the sql query formats and more such details such as software versions, open ports etc. Here is a sneak peak

<img src="/images/internship2/sql.png" width="1000"/>

<img src="/images/internship2/versions.png" width="1000">


Using the same technique as above I found even more ways to abuse this. I started searching for all the pages for that domain which had code 403(Permission Denied). If I saw one I just dorked for its cached version. And it started working. I found some of the templates used in their django webapps.

<img src="/images/internship2/template.png" width="1000">

I thought I could achieve some kind of SSTI (Server Side Template Injection) but decided to just focus more on the recon for this target. Next I also found directory listing which normally gave 403 but again using the "cache" dork I was able to bypass that.

<img src="/images/internship2/403.png">

<img src="/images/internship2/directories.png" width="1000">

And that about it of how I used the "cache" dork. Next up... more vulns from more recon.

## The Forgotten Content

This one's got a story with it. My mentor told me that there are times when big domains just forget about an asset and leave it online. Another tip was to use the copyright text at the bottom of the page to find more assets of that domain. I dorked something like:

`intext:copyright by domain limited 2020`

But the problem with this technique was that there were also a lot of garbage websites which I did not want in my search. Next I read up some articles( and forgot which one it was) and found out about [https://spyonweb.com](https://spyonweb.com). What this site does is find other sites that share the same IP address. And unless it is shared hosting, it has a chance of giving us related assets. It worked. 

It gave me 8 other domains which I didn't find with google but **were** assets of that domain none the less. I hit jackpot again. It was an old website with a vulnerable version of wordpress. After some looking around I found an open directory which contained hundreds of resume(s). I think that qualifies as PII leak. 

## Bucket Kicking 101

It was about time I found my first open S3 bucket. I was advised to use [slurp](https://github.com/0xbharath/slurp). 

PS: This is not the original slurp repo. It was forked from the original one. The creator of slurp deleted their account on github. I think it is safe as I read some of the source code, so building it should be fine. I can't take the guarantee for any future changes though.

Anyway... Back to the main topic. I really liked slurp because of its gigantic wordlist and it is written in GO. I run it with the basic command.

`slurp keyword -c 50 -p permutations.json -t keyword`

After a while it informed me about an open bucket. Time to check manually. You can check by just straight up visiting the URL in a browser. Another check is to use [aws commnd line utility](https://aws.amazon.com/cli/).

I already had an account so I just had to generate the key and the secret. After that I tried to list the contents of the bucket.

<img src="/images/internship2/awsls.png">

We can see all the content of the directories. So it has public Read permission on. Next we test write permission. I create an example.txt file and try to copy it to the bucket.

<img src="/images/internship2/awscp.png" width="1000">

So we have write permission too. Lastly we test delete permission.

<img src="/images/internship2/awsdel.png" width="1000">

We didn't have any delete permission. But the read and write was already an issue. 

That is about it for the second part. The recon was strong with this one. However I will try to find some proper vulns which require exploitation. My exams will be starting soon so I will be taking some time off. See ya! 


