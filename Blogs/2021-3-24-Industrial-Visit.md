---
title: Industrial Visit to Network Bulls
tags: technology
image: /images/indvis/index.jpeg
---

So my college just organized an industrial visit which revolved around networking. We went to [Network bulls](https://www.networkbulls.com/) for the visit. It is a training facility which has courses for networking. One of my primary concerns during the visit was that, since it is a training institute this visit was probably going to be just one big advertising. Well I was wrong.

<!--more-->

<img src="/images/indvis/index.jpeg">

There were two parts to the visit. First we took some basic networking theory like IP addressing, OSI model, Switches and routers etc. And then some practical where we saw actual switches and routers and then created a network of switches,routers, PCs, servers and then configured them. We used [student packet tracer](https://www.netacad.com/courses/packet-tracer) for that stuff.  

Might as well turn this blog into a basics of networking blog. So I will just list out the stuff I learnt there (and more).

# Theory

What are IP addresses & why do we need them?

IP addresses are used to identify devices on a network and yada yada... But why do we need IP addresses when all the devices in the world already have a unique identifier (MAC addresses)? Well, IF you ever noticed when you connected to the wifi on your device you are assigned an IP. Then you use internet based services which make use of your IP address to find you. One thing about network is that IP address assigned to you one day may not be available the next time you connect to a network. Then how will the services find you or continue from the previous time you used them? 

Well your IP address may change but your MAC address won't change. SO the service may remember your MAC address and then look at the IP address associated with it. Then why do we not just use MAC for all the identification? Thats because MAC address are only used for physical identification. There is no standard format or hierarchy like the IP system. Also, different devices work on different layers of OSI model. For example routers work on the layer 3 i.e the network layer which makes use of IP addresses.
Switches use layer 2 i.e data link layer which makes use of MAC addresses.

DA heck is a "OSI Model"?!

Take it as a standard/reference which all other protocols must follow. Other protocols such as TCP/IP, HTTP, SMTP, FTP etc must follow a standard so that all the other devices in the world are able to understand them. Think of OSI model as a common language like english that many people understand (I know it's not that good of an example). 

The OSI model consists of layers and each has its own function. Lets go through them real quick.

<img src="/images/indvis/osilayer.gif">

The layers are numbered from the viewpoint of the receiver.

I think this gif really explains it all! 
- Layer 7: Application

  The interface with which the user interacts and generates/receives data. Example: your browser.
- Layer 6: Presentation

  Performs encoding/decoding, cipher/decipher of data. Basically handles how the data is formatted.
- Layer 5: Session

Performs session management.
- Layer 4: Transportation

  The basic operation is to slice down the data into smaller size segments so that further processing can take place and the transportation of data is easier.
- Layer 3: Network

  Finds the most optimal path to the destination of the data using IP addresses.
- Layer 2: Data link

  Also works to send and receive data. Along with error management.
- Layer 1: Physical

  Conversion of data from/to bits.

Each layer performs some action on the data and then the data is sent. The device which receives the data also use the OSI model to decode and handle the received data. 

Now, I know I am not doing justice by just writing one line about a topic that has entire books written on. But I think It has been explained very well already. I am just listing what happened over at my industrial visit.

IP Classes and sub-netting

I think everyone knows the standard classes:

Class A: Net ID ranging from 0-127 

Class B: Net ID ranging from 128-191 

Class C: Net ID ranging from 192-223 

Among these there are private IPs such as 10(2^24 IP addresses), 172(2^16 IP addresses) and 192 (2^8 IP addresses)

You have probably noticed that we use class C IP inside our household LAN. Because IP addresses are a limited resources we should be efficient in its usage and hence home networks mainly use small networks. As we go upwards towards Class B and A we see exponential increase in number of IP addresses we can use. You also probably noticed that these IPs are used by big corporations. (Ever seen the IP addresses assigned by HackTheBox? They all have net id of 10)

The sub-net masks for them are 255.0.0.0, 255.255.0.0, 255.255.255.0

Sub-net masks are patterns which when XORed with the IP address give us the Net ID(ex:The '192' in 192.1.1.2) and Host ID(ex: The '1.1.2' in 192.1.1.2).

Net id helps us identify a network and host id helps us identify a device on that network.

# Practical

The practical part was a bit underwhelming because you know... I expected (shouldn't have) that we will be getting our hand dirty and making connections from routers and switches and work on real PCs and servers to configure them. We used a software for all of that. So my hands didn't even leave the keyboard is what I am saying. 

So the software was just a drag and drop kind of thing. We dragged and dropped various routers, switches, PCs, servers etc and then connected them. Then we started the router using some command line instructions and setup a remote access profile. We assigned IP addresses to each of them. After that we checked the connections using ping. Finally we accessed the router from other PCs using telnet.

I am not blaming anyone though. If I was in their place, I would also not hand my expensive equipment in hands of bunch of barely evolved apes. All in all I was able to experience something new and that was my objective for the visit.