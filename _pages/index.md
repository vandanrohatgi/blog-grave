---
layout: defaults/page
permalink: index.html
narrow: true
title: Welcome to The Termi(0) !
---

## Who Am I?

Glad you're interested, My name is Vandan Rohatgi and currently an engineering student in the field of Information Technology. 
You can probably tell that I am into the technical stuff like linux (*hence the name*) , Cyber Security or ethical "hacking" (expect a rant about this later). 


## What is it?

The Termi(0) is the name of my weekly blog where I intend to post blogs about my daily learnings sprinkled with bits and pieces of my opinions and information 
that may look interesting but is actually useless irl. 

[To know more about this blog click me!]({{ site.baseurl}}{% link _pages/about.md %})


<hr />

### Recent Posts

{% for post in site.posts limit:3 %}
{% include components/post-card.html %}
{% endfor %}


