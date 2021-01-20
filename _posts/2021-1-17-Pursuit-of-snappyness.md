---
title: Pursuit of Snappy-ness
image: /images/snappyness/info.jpeg
tags: technology
---

When you live in a 3rd world country and can't take anything for granted, you try to make use of everything you've got. This blog will be aimed at one of those burning requirements of today. The Internet. I consider a fast internet connection; an incredible privilege to have. Just the amount of possibilities that unlock when you have access to internet is mind boggling. 

<!--more-->

<img src="/images/snappyness/info.jpeg" width="1000">

(this image seemed a lot more hilarious in my mind)

Lets take a scenario where your ISP promissed you 40mbps speed and you get something like 2-3. Well you can kiss any internet based meeting goodbye. Unless you don't have anger issues, speeds like this requires a will of steel to work with. Now before you just pick up your phone and start taking your frustrations out on the ISP help center, lets try doing what you can on your own part.

After some research (googling) I found that there are factors that may affect your internet signal. A quick google landed me on some articles that seemed to know what they were talking about (I may have lost the link. oops...). I decide to have a crack at them.

In my case, my problem was that many times the speed would drop to its knees and barely anything would load. Other times it was as fast as the ISP promised. Also I really wanted to mess with the router. With the problem and free time at hand I started the experiments.

First I used app to check the internet signal strength in my room using [Amped's wifi analyzer](https://play.google.com/store/apps/details?id=com.pinapps.amped).

Here are all the things I did.

### Lesson 1: Keep it in the Line of Sight

The physical location of the router can bring about very significant changes in signal strength. 

<img src="/images/snappyness/signal.png" height="500">

Well that is... very average. Signal strength is measured in decibels. Lower the decibel better the signal. I read that the signals from router are susceptible to being blocked and absorbed by walls and doors. And I was a few walls and doors away from the router so it makes sense.  

Going near the router with the app open resulted in a increase in signal and now was at about `-33 db`. The boost was double in strength. Well that confirms tip I read. It said to keep the router where you work OR just in the center of the house. As long as the router is in line of sight, it should work well. Keeping the router above the ground and away from electronics may be a good idea.

I also read about the position of the antenna of the router. Keeping the them horizontal leads to better upwards signal (floors) and vertical position leads to better horizontal coverage. So I made one antenna horizontal and the other one vertical. Just to get maximum coverage. 

Just doing this improved my signal strength by a few decibels.

### Lesson 2: Channel your Power!

All routers communicate with devices on a particular channel. For example my router is 2.4 Ghz so it has 11 channels through which it can network. Think of channels as a particular route for the communication. When there are many routers in an area some of them may choose the same channel to work on which may lead to crowding.

When a channel gets crowded it decreases the speed at which the data transfer take place. Hence we should choose a channel which is least used.The router selects a new channel each time it turns on (Most of the time it selects the best one). 

<img src="/images/snappyness/channel.png" height="500">

We can see that my current channel is in a good state. But performace can be increased if I change it to something like 4 or 5. Now depending on your router, you may be able to change it to your liking (Or not).

Open the admin interface of your router. It varies from router to router, so you should check the back of the router or the internet for yours. For me it was `192.168.1.1`

Next you will see a login page. Enter the creds. Again this varies from router to router so maybe look at the back of the router or call your ISP.

<img src="/images/snappyness/wlan.png" width="1000">

We can see lots of information here. Lets go one by one:

- Check in "Band" opttion if there is a 5 Ghz option. 5Ghz is mainly for high speeds but low coverage. The 2.4 Ghz option is to cover more area but lesser speeds. In my case I only had 2.4Ghz available.
- The "chanel width" is what it sounds like. Lower the width of the channel, more stable it is because it will interfere less with other channels. Higher the channel width better the performance. In my case it already had the best option selected.
- Next we move to channel number. We can see that the firmware on my router does not allow me to change it. If yours does, then you can change it to a better one according to the wifi analyzer app.

Since my router did not allow me to change the channel manually, I found that a simply restarting the router forced it to choose the best channel for me. 

### Lesson 3: Domain Name Servers...

If web pages are loading slowly it can be caused by two factors. The DNS which is provided by your ISP or the internet speed. While the latter may not be in your control, making some changes to the DNS may bring some relief. 

The DNS provided by your ISP is probably not the best one. Lets take an example:

{%highlight text%}
dig vandan.tech

;; Query time: 849 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Sun Jan 17 17:53:33 IST 2021
;; MSG SIZE  rcvd: 104
{%endhighlight%}

Compare that to a faster DNS like 1.1.1.1(cloudfare)

{%highlight text%}
dig @1.1.1.1 vandan.tech

;; Query time: 22 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Sun Jan 17 17:53:59 IST 2021
;; MSG SIZE  rcvd: 104
{%endhighlight%}

Thats better. Now shaving off a few milliseconds may not bring about huge changes in your life but hey each and every drop counts.

<img src="/images/snappyness/dns.png" width="1000">

As you can see, we can also change the DNS from the router itself. If you are like me and the firmware does not allow you to change the DNS from the router, you can change it on the device you are working from. The difference would be just that changing the DNS from router will apply that to all connected devices and changing it on the device will only work for that particular device.

You can find more from [this link](https://www.lifewire.com/free-and-public-dns-servers-2626062). I just used the dig command on all of them and found that the cloudfare DNS was the best for me.

### Lesson 4: Can you repeat that?

I was looking for ways to extend my wifi range. One of them caught my attention. Installing a repeater. I was obviously not going to spend money on a proper repeater. No, thats lame. I used an android phone I had lying around. I tried both rooted and unrooted methods. The rooted one didn't work. It made use of old rooted devices with an app called [fqrouter2](https://fqrouter2.en.uptodown.com/android). 

Second option was using an app called [netshare](https://play.google.com/store/apps/details?id=kha.prog.mikrotik). I was able to get it setup and put the phone right in the middle of the router and my pc but the internet speed was soo...sloww...

The range was extended but the speed issue was a major pain. Well it was a good observation and can be used in future. 

### Bonus Section For those who broke their routers

After making these small tweaks I finally managed to blow up my perfectly fine connection and now was getting ready to be yelled at by my local customer care. While I was thinking about which country I should flee to, I thought of trying to fix the connection myself.

First thing I saw was that all the light were "on", so that means that the connection is fine and I just changed something. But I didn't know jack about the settings. I tried changing the settings on the WLAN because I use the WLAN only right? Well... yes and no. While we use a WLAN to connect to the router, what about the router? how does it connect to the ISP?

I found that routers use WAN (Wide Area Network) to connect to ISPs. And then we use WLAN(Wireless Local Area Network) to connect to the router. While looking around WAN configurations I found the problem. I had reset the WAN configuration while I was busy with my shenanigans. 

<img src="/images/snappyness/wan.png" width="1000">

When I found this table I had to do a lot of googling because I didn't understand anything on there. I found that PPPoE (point to point protocol over ethernet) was a protocol generally used for connecting to ISPs. So I selected the 4th option which already had a profile of configurations. I select it and applied changes hoping for the best. 

It didn't work. Looking further I found that there was the word "dsl" in my id I found on my internet bill. Okay... Then I got to know that to connect with DSL you need a unique username and password. You can get these by calling your ISP.

I enter the details and applied the changes. Voilla! I was able to get my connection back. Whew... Dodged that bullet. 

### Ending notes
These are all the things I did on my part. By just doing all this, I was able to get maximum speeds that I was promised and I was able to learn a lot from it (Remember that, just connecting to the LAN with an ethernet cable will almost always improve your internet speeds. Wired connection >> wireless connection). If you have done all that you can do and still are not getting the speeds that were promised, it is time have a very difficult conversation with your ISP or just change to another one. 

