---
title: Mistake of the Year!!! 
tags:
- technology
image: /images/moty/info.png
---

Hey Everyone! I am here today to document my journey of making the biggest mistake of year 2021 and how I fixed it. Hint: Don't drink and drive (Linux)

<!--more-->

So I was working on a cyber security themed hackathon pretty hard. By hard, I mean going at it the whole day and stopping only for sleep. It was a three day hackathon and it had three categories, Software designed radio, a hacking based CTF and lastly secure code design. I was tired of hacking based CTFs so I thought I would give Secure code design a try. (I'll upload my work on github soon)

There were 4 challenges in that section and the solution to be submitted had a lot of steps (zip and upload the code, make a video and upload the video etc.). I thought  "cool, I'll work on these for about 2.5 days and then spend the rest of time submitting my solution. 

It was 6:30 AM of the third day and I was still working. While creating a python environment, I messed up the command and the python environment files populated my working directory instead of the .venv directory that it should have.

![](/images/moty/pyenv.png)

Okay... I messed up the command. Let me delete the files it created and make the environment again. I did this:

`rm -r /bin include/ lib/ lib64/ pyenv.cfg share/`

It asked for sudo permissions. I was in a hurry and added a sudo and entered my password. After that, as usual I do a "ls" after every command and my terminal said: **"ls command not found"**. I thought to myself *hmm... weird.*

And then realization hit me like a truck. HOLY CRAP!!! I JUST DELETED MY ENTIRE /BIN DIRECTORY!!

I was about to have a panic attack. I realized my system is not down yet? I thought I must have some time window before it does decide to do so. I rushed over to my browser and hit my query. First link to pop up was fom askubuntu.

![](/images/moty/google.png)

(Yes I spelled accidentally wrong... you have to understand the panic I was going through)

[https://askubuntu.com/questions/906674/accidentally-removed-bin-how-do-i-restore-it](https://askubuntu.com/questions/906674/accidentally-removed-bin-how-do-i-restore-it)

The second answer suited my scenario. my system was still up so followed it as it said. I want to take this moment to thank the open source community and the forums. I was able to recover all the contents of my /bin and life was good. (For now...)

All my commands worked and I kept working happily. I decided to take a break and shut my system down. When I came back though, my system wouldn't boot. I was able to select ubuntu from my GRUB menu.

![](/images/moty/grub.png)

But after that it was just dark screen. To troubleshoot I pressed escape to see the boot processes and what was going on. I realized my problem was far from over. 

![](/images/moty/failed.png)

Okay so my display manager is not working. I thought maybe the /bin issue is not fixed yet so I went into recovery mode and tried the "dpkg" option to fix broken packages **but** I didn't have internet connection. When it rains it pours. Its just one problem after another. 

So to get the connection back and fix my /bin I decided to create a live USB and booted from it. 

[https://itectec.com/ubuntu/ubuntu-how-to-connect-to-internet-from-recovery-mode/](https://itectec.com/ubuntu/ubuntu-how-to-connect-to-internet-from-recovery-mode/)

I was able to access the internet from within my broken ubuntu file system via the live usb. Technology is amazing. I did "apt install --reinstall" "apt --fix-broken" and everything else to fix the broken packages.

After I was confident that everything was in order I unmounted my /dev/sda7 file system and rebooted. Only to be greeted by the same gdm3 problem. I was sure that its not my /bin problem anymore and a little bit of googling told me that gnome display manager is pain for many people. 

Now we have a new problem to fix. to fix that I decided to install lightdm. An alternative display manager. Also I found a way to get a shell with internet connection without having to boot from the live usb. First go into recovery mode and select the option "root" to drop into a root shell OR you can press alt+ctrl+F2 (or 3 or 4 or 5 or 6) to get a shell. I was connected to my LAN while doing this.

Next follow this article.

[https://askubuntu.com/questions/1049302/wired-ethernet-not-working-ubuntu-18-04](https://askubuntu.com/questions/1049302/wired-ethernet-not-working-ubuntu-18-04)

Next I installed lightdm with "apt install lightdm". Here is what I saw on reboot.

![](/images/moty/light.png)

Okay... so lightdm is also not working. I have been doing this for over a day now. I already lost my chance to participate in the hackathon. So it was getting a little frustrating now. 

I started looking for backup solutions to just take my important stuff with me and reinstall the OS. I had all sorts of ideas like make a backup and copy it to the windows partition. Or transfer them to my USB. Doing a quick "du -sh /home" Told me that a backup of whole thing would take 57 GBs. So the first option made sense.

But that was last resort. So I decided to try more options. I tried reinstalling ubuntu-desktop and gnome-shell. Didn't work. Next I installed XFCE which is an alternative desktop environment. This one didnt work either. 

I did all this till friday and decided to take the whole saturday off and do the backup and reinstalling on sunday. Sunday morning I open up my laptop and funny thing is I was so lost and empty on hope that I didn't even wait for the GUI to appear. I did ctrl+alt+F2 to go straight to the shell. To my surprise, It didn't work. 

I thought *hmm... so i'm not even going to get a shell now huh?* And I was greeted by the XFCE login screen!!! And here I am with documenting this whole thing.

My knowledge of linux/GNU internals and commands increased exponentially in these few days. But the most important lesson I learned was

**Sometimes all we need is a break!**
