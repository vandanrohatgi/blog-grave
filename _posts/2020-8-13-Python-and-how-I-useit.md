---
title: Python... & How I Use It
tags:
  - programming
image: /images/python&howiuseit/python.png
---

Welcome to the first blog! I had a hard time figuring out what should my first blog be, then I just decided that lets just do something I am comfortable with. So the first thing that came to my mind was python but I didnt want to just write a giant tutorial documenting every data structure, every concept and every trick, no... 
<!--more-->
 that has already been done way too many times by way too many people. What **I** am going to do is tell you about how I use python in my daily life as a student aspiring to be a Programmer/ Penetration Tester/ Red Teamer/ Threat Hunter/ Ethical Hacker/ CTF player ... you get the idea.

<img src="/images/python&howiuseit/python.png" height="400" />

## My Experience

So I started programming in python 3 2 years ago (*expect these kind of silly wordplays at random spots*) i.e when I entered college. And what I have learned is that python can do **ANYTHING**. I have used it do web development, web scraping, automation, computer vision, machine learning, deep learning, etc. Heck you can even develop android apps with it. You want to do something? there is probably a module for it. It is so easy and powerful that I just feel straight up spoilt. But I can talk all day about that, So let us just jump right to the meat of this blog!

## Quick Prototyping

Python comes with a powerful interpreter which can be started just by typing python (you can specify the version like python3 or python2 to specify) in the terminal.The interpreter like the name suggests interprets each line you enter and gives the output right-away.

{% highlight bash %}
vandan@lenovo:~$ python3

Python 3.6.9 (default, Jul 17 2020, 12:50:27) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 

{% endhighlight %}

The python interpreter is great when you are not in the mood to write a script or test a code of something like less than 5 lines. An example of quick and dirty testing:-
{% highlight python %}
>>> import requests
>>> response=requests.get('https://google.com')
>>> if response.status_code==200:
...     print("you have successfully used a multi-million dollar search engine to check if your internet is up")
... else:
...     print("Now either your internet is down OR we are all doomed.")  
{% endhighlight%}

But that doesnt stop there... If you find need to do some calculations while your terminal is open and you are too lazy to open calculator app, you can just use the interpreter to do it.

{% highlight bash %}

>>> ((10-(2**3))+(15/3)*34)
172.0

{% endhighlight %}

When dealing with hex codes from binaries to calculate offsets or base64 encoded stuff from urls or ctf(s), it kinda becomes a necessity to be able to convert them on the fly and I use the interpreter just for that. An example would be:
{% highlight python %}

>>> int('0xdeadbeef',16)
3735928559
>>>int('0xffffea',16)-int('0xfff08a',16)
3936

>>>import base64
>>> base64.b64encode(b'nyan cat')
b'bnlhbiBjYXQ='

{% endhighlight%}

You can use online tools to do these conversions but I like doing it this way.

Lets say you installed a module and write a gigantic script making use of that module but when you run it you drown in a sea of errors. You can check if a module is installed properly by just importing the module and hitting enter, if you dont see any error you are golden. 

{% highlight python %}
>>> from scapy.all import *
{% endhighlight%}

Python comes with a package manager named PIP to help you take care of all your package management needs. Lets say I want to write a script with the scapy module but **Oh No!** I see the dredded module not found error. Worry not! For a hero named PIP is here to save the day! Just type "pip install [module name]" in the terminal and the module is installed, Its that easy. (Again Keep in mind that pip3 installs modules for python3 and pip2 installs for python2)

Ps: If you see errors like no distribution of that name is found, it is probably a good idea to head on over to the documentation of that module to get installation instructions.

## Project Work

If you haven't already stalked me on github yet, you will not be surprised to find that all my "projects" (I say it like that because most of them are just a  product of terrible ideas and even worse implementation) are written in python.

![](/images/python&howiuseit/projects.png)

 And I was able to make them because of comprehensive documentation and a large community devoted to python. Never have I ever needed to go and ask someone in person about something I didn't understand. And thats why I recommend python to beginners for any task they want to perform because python is so high level that you don't need to worry about minute details. When you reach a certain level of expertise and want to customize even more than python is able to provide then you can move on to something like C or C++. Although you can jump straight into the deep section and try low level languages but the learning curve might make you give up half-way and thats a *no bueno*. 

<h2><a id="server">A Basic Server</a></h2>

Many times it has happened that I had transfer something from my pc to something like my mobile phone or maybe deliver a payload to a machine I am hacking (*legally ofcourse*) so what do I do? Get up and search for my data cable? pfftt.. NO! Install or open a 3rd party software? Nahhh... wrong again! I just turn my pc into a basic web server and download the file I want to transfer wherever I want. Did I mention that it takes just one line in the terminal to do so? Here is how:-

Make sure that both the devices are on the same network. Before this command you should note down the IP address (use ipconfig for windows or ifconfig for linux) of your pc **and** change into the directory where the file you want to transfer is located.

{% highlight bash %}

vandan@lenovo:~$ python3 -m http.server 5555

OR 

vandan@lenovo:~$ python2 -m SimpleHTTPServer 5555

{% endhighlight %}

(-m is used to tell python to use this module, 5555 is the port, change it to anything you want if that port is occupied)
and then just start up the internet browser in your mobile and type the ip address of your pc and the port you chose in the command, something like

192.168.23.14:5555/

Now just click on the file you want. Same can be achieved with a command line using wget, just tack the name of file you want to download at the end of above address. 

## Generating patterns

There comes a time in man's life when he must generate "A" 100 times to test edge cases in code, find interesting behaviour by breaking the input mechanism or maybe just because of being bored... each to their own. You don't just sit there and type the characters one by one, you use big brain time and use python one liners once again! Do something like this:-

{% highlight bash %}

vandan@lenovo:~$ python3 -c "print('A'*100)"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

{% endhighlight %}

(-c is used to tell python to perform that command, you can use any command not just print)

Also be carefull with use of single quotes and double quotes. (*types while remembering embarassing past*)

## Pwn Tools!

So I am still fairly new to the field of cyber security and probably not able to utilize the full potential of Pwntools module. Here is how I have used it till now:

- Delivering payloads 

I have encountered way too many situations where I am doing a CTF and want to deliver my exploits to netcat connnection but piping it to the connection is not really cutting it or just not working as expected. It is the most frustrating thing when you know your payload is right but its not reaching the destination. Here pwntools comes into the picture by providing such a simple and elegant solution. Lets take look at an example:

{% highlight python %}
from pwn import *

payload="\xef\xbe\xad\xde"

connection=remote("ctfexample.com",1337)
connection.send(payload)
connection.interactive()

{% endhighlight %}

Now if your payload is working and it is meant to spawn a shell then you will see a shell when you run the script. No more nightmares :')

- Shell codes

As I stated earlier I still am quite the noob so I have to lookup shellcodes on the internet and it is especially difficult when you know very little about different architectures that are out there. Hence the shellcraft in pwntools really comes in handy.

## The End

Python has been a bane and boon to me. Boon because it is able to satisfy each and every bit of my requirements with minimal effort so that I can focus on the logic part rather than staring at the documentation for hours. But this advantage is also the reason for which I think it has stopped my growth since python can do so many things that I don't get a reason/motivation to try out new things like Golang. I tried Java **once** and it was enough to make a grown man cry. 

That is about all I can fit in one blog. Connect with me on linkedin for updates on my future blogs and maybe if enough people want it then I will setup a rss feed. See Ya!

(Good job if you were able to find the secret hidden in this blog! If not then I will reveal it's location in the next blog)
<!--You found this blog's secret! Have a cookie-->