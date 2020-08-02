---
title: Py-IDS
---

## About

This is the infamous "second" project which was responsible for affecting and effectivly messing up my first project. But I would be lying if I said that it is not a good one. [Have A look!](https://github.com/vandanrohatgi/Py-IDS)

<img src="/images/attack_detect.gif" />
 
So Py-IDS stands for Python Intrusion Detection System (*mouthfull isn't it?*). As the the name suggests it is an intrusion detection system made with python which can be used to alert the user incase any type of network attack is launched against them. I will admit that it is not perfect and gives out false positives time to time but I still like it because It reeks of my time and effort (*you are entitled to your opinion though*). The fact that I made something and it works (even if not perfectly) is a joy in its own right to me. I may not sound like it **but** trust me when I say that I am 21 years old, you judging potato!

## Tech Stack
- Python3
- Scapy

## What did I learn?
- Python3
- Scapy
- OSI Model
- TCP/IP, ICMP, UDP protocols
- Object Oriented Programming
- Whole bunch of network attack vectors and how to detect them

## Testing And other Details

So to see if my modules actually detect any attacks or not what I did was boot up a kali virtual machine, note the IP addresses and launch the attacks from kali onto the guest( ubuntu ). Majority of the modules worked fine but few didn't (like the smurf attack) because I guess the routers have already installed patches for those attacks and was just straight up blocking my packets.
