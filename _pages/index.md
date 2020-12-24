---
layout: defaults/page
permalink: index.html
narrow: true
title: Welcome to The Termi(0) !
---

# Who Am I?

Glad you're interested, My name is Vandan Rohatgi and currently an engineering student in the field of Information Technology. 
You can probably tell that I am into the technical stuff like linux (*hence the name*) , Cyber Security or ethical "hacking" (expect a rant about this later). [Know more about me!]({{ site.baseurl}}{% link _pages/about.md %})

# What is it?

The Termi(0) is the name of my weekly blog where I intend to post blogs about my daily learnings sprinkled with bits and pieces of my opinions and information that may look interesting but is actually useless irl. 

## WHY?!
Because my memory is terrible and there are too many things that I learn so I just write it down to make it last longer. Think of this site as a glorified notepad.

## WHAT?!
You can expect content on topics such as Technology, Web application attacks, Networking, CTFs, Reverse Engineering, Walkthroughs or whatever I am feeling like.
So you are basically at the mercy of my whims(*muahahaha*). Just kidding, Please do suggest me topics that you want to see.

## WHEN?!
While the content can be a bit irregular in terms of topics, what you **can** rely on is that I am going to do my best at releasing a blog per week .

<hr />

### Recent Posts

{% for post in site.posts limit:3 %}
{% include components/post-card.html %}
{% endfor %}


