---
title: SOC Stuff
tags: 
- blueteam
image: /images/soc/info.jpg
---

In this one I will write about some SOC work that I did using the ELK stash (Elasticsearch, kibana and beats client) without logstash. The purpose is to create a basic dashboard to monitor a single machine. We will extract common info which is needed to determine the security posture of a machine like hostname, IP, applications, antivirus etc. And try to make it look better with some graphs and charts.

<!--more-->

<img src="/images/soc/info.jpg">

First lets talk about the tools for this job:

#### 1. Elastic

Think of it as a nosql database. You can store and query data using elastic search. You can use Elastic in two ways. Either use a cloud based version which is maintained and free for 14 days Or download and setup Elastic in your own machine which is always free. For this I used the cloud one. Use whichever is convenient for you. You can [signup here](https://www.cloud.elastic.co) for it.

#### 2. Kibana

We use kibana to create visualizations and dashboards for all the data that we have collected. Again you can install a local version for use which is free. I used the one that comes with cloud instance of elastic. 

#### 3. Beats Client

This is the software that you install on the machine that you want to monitor. There are many types of beats clients for different purposes. For example to get the information about the file system of the machine we use Filebeats, To check if the machine is up or if a service is up or not we can use Heartbeats, to monitor network data we packetbeat and so on.

In this project I used heartbeats and auditbeat clients. Auditbeat is used to collect data like info about the installed packages,system, processes etc.

#### 4. Docker

I used a normal ubuntu docker image as a machine to monitor. 

## Set up

First I created a free ID at cloud.elastic.co and created a new deployment. Since I had no idea what I was doing, elastic was kind enough to offer a "General" deployment which has the features of all other types of deployments.

<img src="/images/soc/deploy.png" width="500">

<img src="/images/soc/dashboard.png" width="500">

We can then launch the kibana from the dashboard. Next we will fill the database with some data. Here is how to setup [heartbeat](https://www.elastic.co/guide/en/beats/heartbeat/current/heartbeat-installation-configuration.html) and [auditbeat](https://www.elastic.co/guide/en/beats/auditbeat/current/auditbeat-installation-configuration.html).

When you start the beat client they will automatically send the data to your cloud instance. Here is how I configured mine:

hearbeat.yml:

```
- type: icmp
  schedule: '*/5 * * * * * *' 
  hosts: ["172.17.0.2"]
  id: my-machine
  name: My Machine
```

(that is the ip of my docker container)

auditbeat.yml:

```
- module: system
  datasets:
    - package # Installed, updated, and removed packages

  period: 2m # The frequency at which the datasets check for changes

- module: system
  datasets:
    - host    # General host information, e.g. uptime, IPs
    - login   # User logins, logouts, and system boots.
    - process # Started and stopped processes
#    - socket  # Opened and closed sockets
    - user    # User information

  # How often datasets send state updates with the
  # current state of the system (e.g. all currently
  # running processes, all open sockets).
  state.period: 1h
```

I uploaded my configuration files [here](https://github.com/vandanrohatgi/Material/tree/main/soc). Just add a "#" In front of the metric you don't want to be sent to Elastic.

Now when you browse to the "Discover" section on the left hand side panel, you can see that data is present. If not, hit the refresh button.

<img src="/images/soc/kibana.png" width="700">

Now we will choose what data we want to display on the dashboard. Clicking on the "+" button on the right side of the attributes adds them to our area of interest. When we have selected all the attributes we can then click the save button. 

<img src="/images/soc/attributes.png" width="700">

Now we can import all the saves to create a new dashboard with all the information. I created some charts using the "Create panel" button with which we can create all kinds of visualizations. 

<img src="/images/soc/dash1.png" width="700">

<img src="/images/soc/dash2.png" width="700">

Most of the attributes were straight forward. I just added them. Some required filtering. For example to find the antivirus software installed on the system I had to use filters. 

Here is the filter I used to find all the antivirus related software on the machine.

```
{
  "query": {
    "wildcard": {
      "package.description": {
        "value": "*virus*",
        "boost": 1,
        "rewrite": "constant_score"
      }
    }
  }
}
```

What this does is looks at the description of the packages and looks for the pattern "Virus". I know this is a very hackey way of doing things but cut me some slack, I am still a beginner at this stuff. There are a lot of ways we can perform queries in Elastic like bools, filters etc. 

Another filter I used was the "exists" filter which just removes all the rows which didn't have any value for a particular column and only display the rows which do.

<img src="/images/soc/filter.png">

Finally I wrote a python script to try and query Elastic Search. I used the (elasticsearch](https://pypi.org/project/elasticsearch/) library. But this can easily be done using the request library too.

```
from elasticsearch import Elasticsearch

es=Elasticsearch(cloud_id="<cloud_id>",http_auth=('<username>','<password>'))
if(es.indices.exists(index="auditbeat-*")):
    print("Index exists. Checking for Antivitrus Software...")
data=es.search(index="auditbeat-*",body={"query": {"wildcard": {"package.description": {"value": "*virus*","boost": 1.0,"rewrite": "constant_score"}}},"fields":["package.name"],"_source":"false"})

if (data.get('_shards').get('successful')==1):
    print("Query was successfull. Checking for Entries...")
else:
    print("Query failed. Exiting...")
    exit()

try:
    print("Following Antivirus Software was found on machine")
    for x in data.get('hits').get('hits'):
        print(x.get('fields').get('package.name')[0])
except:
    print("Antivirus software was not found on machine")
```

There are still a lot of functionalities I wanted to add but can't figure out how to. I will update the blog when I do.
