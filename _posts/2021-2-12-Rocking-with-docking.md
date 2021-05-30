---
title: Rocking with Docking
image: /images/docker/docker.png
tag: technology
---

Hello there! Are you also an aspiring penetration tester/red teamer using a budget pc that can't run bulky VMs to complete your daily tasks while still maintaining some amount of security and cleanliness? Well...  Thats the case with me anyway.

<!--more-->

### Update!

I created a [Dockerfile and some scripts](https://github.com/vandanrohatgi/Pentest-with-docker) to spin up new kali docker images on the fly which have essential software already installed. Credits to [this article](https://codefresh.io/docker-tutorial/build-docker-image-dockerfiles/). I also definitely recommend [this website](http://play-with-docker.com) to learn all about dockers!

<img src="/images/docker/docker.png">

Many of the people I have seen in the security field usually use either a VM or dual boot a separate OS for their security tools, testing environments etc. Mainly this is done to keep things organized and most importantly for example if they ran a malicious script they found on internet with root privileges their main system will be safe. 

Now, I am all for either using a VM or multi booting my pc(dual booted) but as I already stated, **budget pc**. Just for some insight, I still run 4GB RAM. I leave the rest to your imagination. Till now I was managing with an ubuntu VM but it just started freezing, crashing and its size easily grew to 20+ GB even with minimal software.

Enter... Docker. ****sobbing**** It's so beautiful. I fell in love for the first time in my life. Lets talk about how I started using docker.

*Disclaimer: This post consists of ways in which docker was not meant to be used. Reader's discretion is advised.* 

## Setting Up

My aim of using docker is to have the whole pentest environment in one isolated package. While surfing the web I found a kind stranger who has already done most of what I needed to do. Here's [the article](https://amar-laksh.github.io/2019/08/24/Setting-up-Kali-docker-for-HackTheBox.html).
Main things I wanted was ability to use OpenVPN (for HTB and THM stuff) and a way to run GUI applications (firefox, ZAP). 

First I pulled a [Kali image](https://hub.docker.com/r/kalilinux/kali-rolling) from the official kali repository on docker hub.

{%highlight text%}
docker pull kalilinux/kali-rolling
{%endhighlight%}

First lets explain Images and Containers: 
- Image: Think of this as the setup.exe file. It consists all the information about the container that needs to be made.
- Container: Think of this as the application that is installed after you run the setup.exe file. It uses the information from the image and produces an isolated system which you can interact with using the terminal.

Now the pulled kali image is fully bareback. It does not consist of any tool... And I love it! It gives me the freedom of installing what I want without the annoying bloatware. 

Now to run the newly pulled kali image.

{%highlight text%}
docker run -it kalilinux/kali-rolling
{%endhighlight%}

`-it` flags are used to give us an interactive terminal for the newly created container.

<img src="/images/docker/term.png">

I chose a kali image due to 2 main reasons:
- It has all the tools and stuff I want in the the kali repositories.
- It looks cool as hell.

## Networking

We have a basic container but if we try to connect to any vpn through it, you will get few errors like "tun0 not available". Refer back to the article from the beginning we can solve this by adding 

{%highlight text%}
--cap-add=NET_ADMIN --device /dev/net/tun  --sysctl net.ipv6.conf.all.disable_ipv6=0
{%endhighlight%}

Lets break it down.

`--cap-add=NET_ADMIN` : The "cap-add" is used to give the container special privileges(capabilities) and the "NET_ADMIN" is used to allow the container to make network related changes to the host. Now, we could just done "--privileged" flag and call it a day, but as you can probably tell, giving your container root privileges is not a great idea if you are keeping the security posture in mind.

`--device /dev/net/tun` : "device" flag is used to add a device from host to the container. the device "tun" stands for "tunnel" is just another network interface that all the VPN softwares use. So we provide that device to the container.

`--sysctl net.ipv6.conf.all.disable_ipv6=0` : This just enables IPv6 addressing.

And now you should be able to connect to VPN from inside the container.

## GUI

Now for this I could have just used the browser present on my host but that would require me to setup traffic forwarding through the container using IPtables and proxies on my browser which, I just didn't want to go through. Before attaching the host display to the container we need to do `xhost +` on the host to allow all connections to connect to the display.

{%highlight text%}
-e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix
{%endhighlight%}

`-e DISPLAY=:0` : The 'e' flag is used to set environment variables for the container. We set the "Display" variable to 0. We set it to 0 because that is the index of the current display used by the host. (Number increases with increasing displays such as multiple monitors)

`-v /tmp/.X11-unix:/tmp/.X11-unix` : The 'v' flag is used to attach volumes to the container. And from what I understand the X11 server uses this volume to connect with displays.

Now you can use browsers and stuff from inside the container. I used firefox-esr because it was directly available to install from the kali repo.

## Workflow

Now that you have the initial command to run your docker container:

{%highlight text%}
docker run -ti --cap-add=NET_ADMIN --device /dev/net/tun --sysctl net.ipv6.conf.all.disable_ipv6=0 -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix -v ~/data:/data kalilinux/kali-rolling /bin/bash
{%endhighlight%}


Here is how to work with it.
- You can install tools and stuff using `apt install toolname` or just search for them in the kali repo using `apt search toolname`.
- This is a very important step. When you exit your container using `exit` or just Ctrl+D, your changes won't be saved. After you have installed the tools and setup your environment you need to save those changes. What you can do is create a new image from your modified container and then use this image as a base for any future containers you fire up.

{%highlight text%}
┌──(root💀082ac707a478)-[/]
└─# 
exit
$ docker ps -a
CONTAINER ID   IMAGE          COMMAND       CREATED             STATUS                     PORTS     NAMES
082ac707a478   newadditions   "bash"        About an hour ago   Up About a minute                    adoring_chaum

$ docker commit adoring_chaum newbase
sha256:06c3948de8b72b5aee54d71b4227cb56a0d6bae3b9fca434b2d95a22aeb09f1b

$ docker images
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
newbase        latest    06c3948de8b7   56 seconds ago   1.19GB
{%endhighlight%}

After you exit the docker you can view the container that you just exited using `docker ps -a`. Now we can commit the changes so that you wont have to install the tools every time you create a container. Use `docker commit container-name new-image-name`.

After that we can run see this image using `docker images`. Next time just fire up the container with everything already setup.

#### Resuming

You must be thinking that do I have to create a new image every time I make small change to the container. No. You only make a new image if you want that change to persist. This is a great feature if you like experimenting with new tools and settings. Also if you don't want to make a new image you can just reuse the container that you just exited. It will have all the changes still intact. Reusing the container also saves you the trouble of making use of long docker run commands. 

{%highlight text%}
docker ps -a
CONTAINER ID   IMAGE          COMMAND       CREATED             STATUS                      PORTS     NAMES
082ac707a478   newadditions   "bash"        About an hour ago   Exited (0) 59 minutes ago             adoring_chaum

$ docker start adoring_chaum 
adoring_chaum
$ docker exec -it adoring_chaum bash
┌──(root💀082ac707a478)-[/]

{%endhighlight%}

you can get the name of previous container using `docker ps -a` and then restart that container using `docker start container_name` and finally get a shell to that container using `docker exec -it container_name bash`.

#### Volumes

If you downloaded a file and want to save that file you can make use of Volumes. Volumes are just directories that you can mount to the container and then that directory will appear inside you container file system.

{%highlight text%}
$ mkdir data
$ docker run -it -v ~/data:/data kalilinux/kali-rolling

┌──(root💀082ac707a478)-[/]
└─# ls
bin  boot  data  dev  etc  home  htb.ovpn  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  thm.ovpn  tmp  tools  usr  var
{%endhighlight%}

Now if you want move any files for future or transfer to the host you can just transfer that file to that directory.

#### Multiple shells

You can get multiple shells on the same container. Just open another terminal and use `docker exec -it container_name bash`. "exec" is used to run a command inside a running container. 

**Update** I recently experimented with using tmux (terminal multiplexer). You may have already heard of it since it is pretty popular. It allows you to split your terminal into many parts. I found it really good, since I don't have to go back and forth between multiple terminals. 

You can just install it using `sudo apt install tmux`. One thing I did find annoying was the default configurations on it. [Here's the fix for that](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/)

Follow the above guide and you are golden!

#### Cleaning 

You can delete any containers or images that you don't need.

{%highlight text%}
docker ps -a
CONTAINER ID   IMAGE          COMMAND       CREATED        STATUS                       PORTS     NAMES
082ac707a478   newadditions   "bash"        2 hours ago    Exited (137) 6 minutes ago             adoring_chaum

$ docker rm adoring_chaum 
adoring_chaum

$ docker images
REPOSITORY     TAG       IMAGE ID       CREATED          SIZE
newbase        latest    06c3948de8b7   23 minutes ago   1.19GB

$ docker rmi newbase:latest 
Untagged: newbase:latest
Deleted: sha256:06c3948de8b72b5aee54d71b4227cb56a0d6bae3b9fca434b2d95a22aeb09f1b
Deleted: sha256:832ca0646407155214d25a1becf3d904e1391a46a6a69dd63d948d523bec062d

{%endhighlight%}

Use the "rm" command to delete a container and "rmi" to delete an image. Finally you can also do `docker system prune` to remove any dangling or unwanted images, containers, resources etc.

#### Additional security measures

- Create a new user on the host and add them to the docker group so that you can run docker as a non root user. [Here is how](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)  
- When inside the container the default user is root. You can further create a new user inside the container and then use that user as default.
- Avoid using "--privileged" flag. You can use the "--cap-add" flag instead and give specific and limited access to the container instead of all the privileges.
- This goes without saying but be careful of what you do inside the container too.

## Conclusion

I know that this is a lot of work compared to a VM, but that is something I leave up to you to decide if it is worth it. As for me docker is currently perfect for all my needs. Did I mention I learned lots of new stuff doing this? Hopefulliy this will help me If I ever encounter a docker while hunting. Huge thanks to [Amar Laksh](https://github.com/amar-laksh), as a docker noob I definitely wouldn't have been able to do all this alone.