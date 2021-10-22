---
title: Microsoft Azure Fundamentals Notes
tags:
- blueteam
- technology
- notes
image: /images/azure/info.png
---

Hey everyone. I just realized that I don't use this blog space near enough to what I should be. So, I will now take notes of the courses I'm doing and post it here too. Starting with an Azure Cloud course I'm taking AZ-900 (Azure fundamentals). Lets start.

<!--more-->

# Introduction of Azure Fundamentals

So everyone knows what microsoft azure is. It's a cloud platform that provides various services (Saas, Paas and Iaas) like remote storage, database hosting, and centralized account management. Azure also offers new capabilities like AI and Internet of Things (IoT).

Starting with cloud computing. Which is basically you pay someone else to handle everything (resources, maintenance , backup, scaling etc) apart from the real work. (you want someone else to do that too don't you?) 

You also get the freedom of increasing and decreasing the resources you need to handle the budget better. For ex: your business is a seasonal business so now you can just decrease the resources and hence the cost of your infrastructure. Amazing right? Cloud provides two basic services: computational power and storage. Basically It's like renting a house but you don't have to take care of it.

Apart from these basic services you can also use services like Speech recognition, AI, software services provided by the cloud company.

## What is Azure?

Azure (of Microsoft) is one such cloud service we discussed above. It can do all the above things like Virtual machines, web hosting, remote data storage etc. It also has other features like event based application, container services, microsoft cosmos db, machine learning, bots (no not a bot net, more of a chat bot) etc. 

All these services can be used using Azure portal which is a web based interface. Azure uses virtualization to perform all these services. It basically has many VMs across the globe. Each rack of these machines contain a fabric controller which in turn is controls by an Orchestrator which is responsible for handling everything happening in azure like responding to user requests. 

<img src="/images/azure/portal.png">

Users make this request using the orchestrator's web api (basically the azure portal in layman terms). Advanced users can use this api using advanced technology which is not yet understood by the common human.

When a request made by the user the request is handled by the orchestrator which in turn manages all the resources and needs and sends this info to the best suitable machine rack. The fabric controller handles this request and creates the VM. 

## Azure Marketplace

This is basically and app store you find on your mobiles. It contains software from microsoft, startups and software vendors which is optimized to run on Azure. Users buy/use this software for their needs.

## Azure Services

Some commonly used services and examples:

- Compute: Azure Virtual Machines, Azure Virtual Machine Scale Sets, Azure Kubernetes Service, Azure Batch, Azure Container Instances, Azure Functions etc

- Networking: Azure Virtual Network, Azure Load Balancer, Azure DNS, Azure Content Delivery Network, Azure DDoS Protection, Azure Firewall etc

- Storage: Queue (store and relay messages between applications), files (file shares managed like a file server), blob (large objects like video files or bitmaps), tables(nosql data)

- Mobile: cross platform and native apps

- Databases: sql, cosmosdb, mysql, cache for redis(in-memory key-value database), data migration service etc.

- Web: web applications, APIs, Notification hub, cognitive search (search as a service), SignalR service (real time web services)

- Internet of Things (IoT): IOT central (Saas to connect, monitor, and manage iot devices), IOT hub (secure comm between millions of iot devices), IOT edge (push machine learning models directly to iot devices)

- Big data: Azure Synapse Analytics(Analyze and query petabytes of data on azure cloud), Azure HDInsight (manage massive amount of data using hadoop), Azure Databricks (spark based analytics)

- AI: machine learning service (develop, train, test, deploy, manage, and track machine learning models. It can auto-generate a model and auto-tune it for you), ML studio (build, test, and deploy machine learning solutions by using prebuilt machine learning algorithms and data-handling modules)

ML services: Vision, speech, add bing search to apps, knowledge mapping for intelligent suggestion, NLP

- DevOps: Azure Devops (high-performance pipelines, free private Git repositories, configurable Kanban boards, and extensive automated and cloud-based load testing), Azure DevTest Labs (create on-demand Windows and Linux environments to test or demo applications directly from deployment pipelines)

<img src="/images/azure/services.png">

An imaginary company named "Tailwind traders" will be used explain different concepts and services.

# Azure Fundamental Concepts

types of cloud:

- Public cloud: resources like servers and storage are provided by a third party and delivered over the internet
- Private cloud: All the resources are exclusively used by one organization and are present mostly on-premises 
- Hybrid cloud: a mixture of private and public cloud that allows data and application sharing between them.

<img src="/images/azure/models.png">

Advantages of cloud:
- High Availability (continuos user exp)
- Scalability (vertical:add more resources like RAM, CPUs and horizontal:add more instances)
- Elasticity (auto scaling according to needs of an application)
- Agility (Quick setup)
- Geo Distribution (ensuring less proximity to users and hence better performance)
- Disaster recovery (backups, data replication etc)
- Does not require Capital for setting up infrastructure
- Pay as you go model

## Cloud Service Model types

<img src="/images/azure/servicemodels.png">

IaaS: Infrastructure as a service is closest to managing physical servers. Cloud provider maintains the hardware but the user maintains everything else like OS and software.

Advantage:
- No Capital required
- agility
- shared responsibility of management
- consumption based model
- no deep technical skills req
- flexible

PaaS: Platform as service is when the cloud provider manages the resources such as VMs, networking etc (hardware and software) like in case of hosting web applications.

advantages:
- same as iaas

SaaS: Software as a Service is when everything is handled by the cloud provider and the user only needs to provide them with data. ex: office 365

advantage same as above

disadvantage: Since we don't have direct control over the software we may not be able to customize it


<img src handling.png>

## Serverless computing

This is like paas where developers use cloud to build and deploy applications. All the hardware and software are managed by cloud the developer only needs to focus on building the app. Since the infrastructure is taken care of automatically it is almost invisible to the developer and hence the name.

# Azure architectural components

<img src="/images/azure/resources.png">

- Resources: the instances of the services we create like sql database or VMS
- resource groups: these services are grouped together in a logical manner. i.e related resources are grouped together
- subscription: Group f user accounts and the resources used by them. Mainly used for monitoring and handling quotas of resources
- management groups: helps manage policies and compliance for various subscriptions

## Azure regions, availability zones, and region pairs

Azure is made of many data centers. These data centers around the globe contain resources which are used when you create a service like a database or a VM.

Azure Regions

A region is a geographical area on the planet that contains at least one but potentially multiple datacenters that are nearby and networked together with a low-latency network. 

`Some services or VM features are only available in certain regions, such as specific VM sizes or storage types. There are also some global Azure services that don't require you to select a particular region, such as Azure Active Directory, Azure Traffic Manager, and Azure DNS.`

<img src="/images/azure/regions.png">

Regions are important for improving performance by allocating the resources closest to the users. Global regions ensure that data backups are safe.

Special regions are also there for places like US where only US government related entities can use those azure resources. Another one is present in china where microsoft partners with another company to handle their data centers.


Availability zones

These are the zones present in a single region which are physically isolated and connected via high speed connections. Ensuring redundancy in case one of the zone go down.

<img src="/images/azure/zone.png">

Not all regions have this facility of availability zones.

Availability zones may cost extra to transfer your data between them. Critical applications are one use case of availability zones.

Three categories of azure services that support availability zones:
- zonal services:pin a resource/service (vm, managed disks etc) to specific zone
- zone-redundant services: automatic replication of resource across zones (Sql database)
- Non regional services:services always available and not prone to region wide outages

## region pairs

Each region contains minimum three zones. Region pairs are also present that protect services if whole region goes down. These region pairs are present in same geo position but at least 300 miles away.Services automatically fall to the other region if any disaster affects the first region.

<img src="/images/azure/pair.png">

Updates are rolled out in a region-wise manner to ensure services are always up.

## Azure resources and Azure Resource Manager

Resources and resource groups defined above. Each resource should be present in only one group and must be present in a group. Resources can be transferred to other groups. resource groups cannot be nested.

If a resource group is deleted all the resources within it are also deleted. Making it easy for testing and removing multiple resources at once. 

Resource groups are a use case for role based access control where you can limit access to only whats needed.

Resource Manager

A service in azure to create, update, and delete resources in your Azure account along with access control, locks, and tags to secure and organize your resources after deployment.

<img src="/images/azure/manager.png">

Roles of resource manager:

- deploy, monitor, manage all the resources as a group
- manage your infrastructure through declarative templates rather than scripts.
- Define and deploy your infrastructure through the declarative syntax in Azure Resource Manager templates, rather than through imperative commands.

- prevent accidental deletion and changes by implementing read only access controls
- Implement role based access control. for ex: developers may have read only access, IT can have settings and admins have full control access
- manage organization's billing

## Azure subscriptions and management groups

A subscription is needed to start using resources (Vms,databases etc). 

<img src="/images/azure/subs.png">

Azure subscriptions can be used to define boundaries around azure products, resources and services.

- billing boundary: determines how an azure account will be billed. you can separate billing for multiple subscriptions.
- access control boundary: access controls are applied a t a subscription level. so different departments can have different access controls.

Create additional Azure subscriptions

purpose for different subscriptions:

- Environments: create subscriptions for development, testing, security, compliance etc. this useful because access control is applied at subscription level

- reflect diff organizational structures. for ex limit a team to lower resource cost.

- Separated billing purposes: for ex one for production which will have higher budget than one subscription for testing and development.

<img src="/images/azure/billing.png">

Azure management groups

these groups are used when you need to manage large amount of subscriptions, resources, and management groups. Using this access, policies and compliance can be applied to all the components of a management group. 

For example, you can apply policies to a management group that limits the regions available for VM creation. This policy would be applied to all management groups, subscriptions, and resources under that management group by only allowing VMs to be created in that region.

<img src="/images/azure/mgmtgroup.png">

You can create a hierarchy that applies a policy. For example, you could limit VM locations to the US West Region in a group called Production. And then this policy will be inherited by all the members of that group. RBAC can also be applied in the same way.

Facts about management groups:

    10,000 management groups can be supported in a single directory.
    A management group tree can support up to six levels of depth. This limit doesn't include the root level or the subscription level.
    Each management group and subscription can support only one parent.
    Each management group can have many children.
    All subscriptions and management groups are within a single hierarchy in each directory.

## Exercise - Create a website hosted in Azure

In this one will finally get hands on nad do some stuff! 

PS: if you get troubles in activating the sandbox sign with your email instead of your phone number.

App Service

HTTP based service for building and hosting web apps without managing infrastructure. Applications developed in .NET, .NET Core, Java, Ruby, Node.js, PHP, or Python can run in and scale with ease on both Windows-based and Linux-based environments.

First thing we need to do when making a basic web application is creating a resource group to hold all our resources in one group such as database, server, network etc.

we finally start working on the azure portal. 

<img src="/images/azure/portal1.png">

# Azure Compute Services

Computing resources such as Vms, container services, app service, azure functions etc.

VMs can be used when:
- total control over OS is needed
- run custom software
- custom hosting configs
- testing and development
- running applications on cloud
- as an alternative while dealing with a disaster

Scaling

Lets talk scale. Azure provides two options to scale your VM instances:

- Scale sets
- Azure Batch

Scale sets: Helps in managing,configuring and updating a group of VMs. Automatically increase or decrease the number of VMs according to the demand. (PaaS)

Azure Batch: Provides compute resources to perform really big compute tasks. These tasks are computed/carried out on many VMs which are increased and decreased according to the task (IaaS)

## App Services

An alternative to VMs for your backend needs can be App services. They can help in hosting, mobile backend, background web jobs (tasks that run as a part of your web application), APIs etc. with automatic scaling and high availability. It supports collaboration using github, git or azure devOps. (Paas)

It also offers a free tier for small application with low traffic.

## Azure Container and Kubernetes Services

Container come in handy when we want to run multiple OS on single Vm. We can multiple instances of the same application on the same VM. Multiple containers can be orchestrated at the same time. There are two ways to manage containers in Azure:

- Azure Container instances: helps in running containers without worrying about Vms or any other services. Allows to upload our own containers. (Paas)
- Azure Kubernetes Service: Automates, manages and interacts with large number of containers.

Kubernetes: helps in managing containers on a large scale. Manage workload, automate tasks and container deployment. also helps in pod management (pod is group of one of more containers), reverting to previous state if something crashes, data storage and networking, capabilities like (network isolation, policies for network security, exposing pods to the internet etc).

Containers are a form of microservice architecture. When we break a solution into smaller and independent pieces. For example, you might split a website into a container hosting your front end, another hosting your back end, and a third for storage. This split allows you to separate portions of your app into logical sections that can be maintained, scaled, or updated independently.

for example if your backend has reached its max capacity but your frontend is till doing fine we can scale the backend accordingly because its a separate part of the application. so the backend, frontend and the database are all parts of one single micro service architecture. 

This helps in configuring and changing the parts of the same application without affecting the whole thing/ other services.

## Azure Functions

These are event driven actions. They can save money by performing action only when a certain event takes place and hence reducing resources taken while it is idle. Serverless computing is when all the infrastructure, scaling, allocation and de-allocation of resources is handled by cloud company. Since it is sort of invisible to the developer it s called serverless. (abstraction)

Components of serverless computing:

- Abstraction of server: No resources are reserved by you. all the scaling is done by the cloud.
- Event driven scale: The platform responds automatically to the rate of incoming requests and scales accordingly. It also contains time driven functions. for ex: perform a backup at 12:00 am everyday.
- Micro Billing: Traditionally if you allocate some resources for a website that has just 1 or 2 visitors a day, most of the resources you pay for aren't even being used and hence waste money. With micro billing the cost is incurred only when the code of your application runs. Amazing right?! So if your code/program runs for 5 minutes then you pay only for that 5 min computation time!

Two implementations of serverless computing:

- Azure Functions: Azure function which take the form of code (available in all popular languages). This code is run when a event like message from another service, timer, REST request occur. These function scale automatically and the billing is done only based on the amount of time/computational resources that were used while the function was running. For ex: a function responding to data from iot devices which may have high number of request during business hours. If you already have a code in place and want to push that automation system to azure cloud or you wan to write a custom automation program then functions are the way to go.

We can also define these functions as stateless (default, responds to each event as a new/fresh event) and stateful (durable functions, takes previous events in account to responds accordingly)

- Azure Logic Apps: remember scratch? the programming language for kids that had blocks? Similar to that logic app are the non-coding representation of azure functions. We can define workflow for when an event takes place. It has blocks like loops, if-then, switch etc. Custom block can also be written. If you don't have programming knowledge or some code isn't already available for automating a task logic apps are the way to go.

<img src="/images/azure/diff.png">

## Azure Virtual Desktop

This feature just became so much more relevant. As the name suggests, virtual desktop is when you can use the resources/ computers on the cloud as a working environment. For example a windows desktop that lives on the cloud and users can interact with it. Any OS (windows, Mac, ios, android ,linux etc) can be used as a virtual desktop through any device of the user's wish (phone, tablet, laptop, browser etc.) 

The cost of setting up new devices, managing them and shipping them to remote workers is costly. This feature comes a good alternative where none of the above problems are faced along with reducing costs to a minimum. Users can connect to Azure virtual desktop using a native app or a web client.

It has enhanced security though features like Active Directory, MFA, Role based access control. Since these desktops are separate from the hard drive, there is low risk of data being left on a personal device. 

`This service is more secure because no ports are opened for a protocol like RDP, instead a reverse connect technology is used`

I tried reading up on it but didn't get most of it. 

<img src="/images/azure/reverse.png">

Azure Virtual Desktop gives you options to load balance users on your VM host pools. Host pools are collections of VMs with the same configuration assigned to multiple users. For the best performance, you can configure load balancing to occur as users sign in (breadth mode). With breadth mode, users are sequentially allocated across the host pool for your workload. To save costs, you can configure your VMs for depth mode load balancing where users are fully allocated on one VM before moving to the next. Azure Virtual Desktop provides tools to automatically provision additional VMs when incoming demand exceeds a specified threshold.

(Yes that whole paragraph is taken from the course because it has many factual points)

It also has multi-session windows 10 deployment where many users can use a single VM. 

Azure virtual desktop comes along with the O365 license and you only need to pay for the resources used by the virtual desktops.

[11 Oct 2021]
# Azure Virtual Networking

Azure resources like Vms, web apps, databases can interact with each other, users on the internet or the on-premises infrastructure using azure virtual networking.

Isolation and segmentation

Azure networking can help in creating isolated networks to which you can assign IP addresses. Azure networks also provide name resolution services too for these networks.

Internet Communications

Azure VMs can connect to the internet by default.

Comm between Azure resources

This can take place in 2 ways:
- Virtual networks: Vms, app services,kubernetes services,virtual machine scale sets all can communicate with each other.
- Service endpoints: this feature provides and optimum route for communication to take place. resources can be provided private IPs.

Comm with on-premises resources

On-premises resources can be connected to azure resources. This can be done in three ways:

- Point-to-site vpn: in this setting aa computer outside the organization connects directly to the VPN of azure.
- Site-to-sie vpn: the on-premises vpn connects to a vpn on azure. devices in azure appear to be in on a local network.
- azure express route: a way to connect in which the connection is not over the internet. Its suitable for operations that need greater bandwidth and higher security.

Route network traffic

network between internet, subnets, premises networks can be achieved by:
- Route tables: defines a table to route traffic in a specific way.
- Border gateway protocol: BGP (remember the recent facebook downtime?) works with azure vpn or expressroute to connect on-premises network to azure virtual networks.

Filter network traffic

traffic filtering can take place in 2 ways:

- Network security groups: this is a resource in azure where you can write rules for inbound and outbound traffic to decide if we want o allow or deny that traffic.  (based on factors like port, source and destination IP etc)
- Network virtual appliance: a special VM that acts as a hardened network security device. It can be used to run firewalls or managing a WAN.

Connecting virtual networks

Different virtual networks can be connected to each other using peering. these virtual networks can be in separate regions. This allows us to create globally inter-connected networks through azure. 

UDR is user-defined Routing. UDR is a significant update to Azure’s Virtual Networks as this allows network admins to control the routing tables between subnets within a VNet, as well as between VNets, thereby allowing for greater control over network traffic flow.

<img src="/images/azure/vpn.png">

## Azure virtual network settings

Creating a virtual network:
- Network name: name of the network. one that descriptive of the purpose. Not necessary to be unique globally.
- Address space: We define the address space in Classless Inter-domain routing format (CIDR). for ex: 10.0.0.24 (24 here symbolizes that the only the first 24 bits are fixed and cannot be changed) hence the range will be 10.0.0.1 - 10.0.0.254. If you want to create more than one virtual network then they should not have any IP addresses that are common. 10.1.0.1/24 and 10.0.0.24 don't have anything in common.
- Subscription: Like any resource this needs a subscription.
- REsource group: again. all the resources need to be in a resource group. 
- Location
- Subnet: create one or more subnet within one network
- Ddos protection
- Service endpoints: Azure provides optimum/secure route to other azure resources like databases, storage etc.
- Network security groups 
- Route table

These networks can be configured using the portal, cloudshell or powershell.

## Azure VPN Gateway fundamentals (I didn't get some of it)

VPNs connect two networks over unidentified network that uses encryption to protect data. 

VPN gateway: its like a virtual network gateway. The gateway converts information, data or other communications from one protocol or format to another and sits between two networks. it connects on-premises datacenters to virtual networks, individual devices to a virtual network or connect two networks.

<img src="/images/azure/gateway.png">

In azure vpn gateways use pre-shared key as the method of authentication. It relies on IKE (internet key exchange) and IPsec (internet protocol security). IKE is used to set up a security association (an agreement of the encryption) between two endpoints. This association is then passed to the IPSec suite, which encrypts and decrypts data packets encapsulated in the VPN tunnel.

2 types of vpn gateways are:
- policy based vpn gateway
- route based vpn gateway

(Skipped most of the content after this)

## Azure ExpressRoute fundamentals

Expressroute helps in extending your on-premises network to azure cloud. These connections don't go over public internet offering more reliability, faster speeds, consistent latencies, and higher security than typical connections over the Internet.

<img src="/images/azure/express.png">

Layer 2 and 3 of the OSI model are used in this concept:
- L2: data link layer, node-to-node communication within a network
- L2: network layer, handles the routing and addressing between nodes

Features of expressroute:
- connects your on-premises network to azure cloud through connectivity partners.
- enables direct access to services like Office365, cosmosDB, azure VMs and other cloud services.
- consists of redundancies to provide high availability
- global connectivity to microsoft services. For ex: you have 2 datacenters in 2 diff geographical locations. if both of them are connected to expressroute then your datacenters can communicate through them. all the data will go through microsoft network.
- express route uses BGP.

connectivity models

<img src="/images/azure/expressmodel.png">

Expressroute has higher security because the data does not travel though public internet but the DNs queries, certificate list checking and azure CDN requests still take place over the internet.

# Azure Storage services

Blobs (unstructured data massive in size backups, videos, images), file storage (file shares), queue storage for messaging between apps, table storage for semi structured data, disk storage for VMs etc.

SSds and hard drives options are available. Pricing plans include Hot storage for frequently accessed data (images in a website), cold storage for lesser accessed data (retained for 30 days), archives for rarely accessed data (retained for 180 days)

To start using azure storage, a storage account is needed which will contain all the storage data (blobs, disks, files, etc)

## Disk Storage

Provides disks for Virtual machines which help in storing persistent data. disks come in SSds and HDDs.

## Blob Storage

Stores massive amounts of unstructured data. It can store any kind/format of data. Ideal for:

    Serving images or documents directly to a browser.
    Storing files for distributed access.
    Streaming video and audio.
    Storing data for backup and restore, disaster recovery, and archiving.
    Storing data for analysis by an on-premises or Azure-hosted service.
    Storing up to 8 TB of data for virtual machines.

Blobs are stored inside containers to help organize data.

<img src="/images/azure/blob.png">

## File storage

Azure files provide file shares which can be accessed via SMB and NFS protocols. These file shares can be accessed from anywhere in the world along with azure services that may require them to read data (by mounting the shares). Situations file storage comes in handy:

- on-premises applications that may use file share data.
- storing config files for multiple VMs so that all the machines are on the same page.
- Reading and writing data for analysis later on (crash dumps, monitor data etc)

Azure files can be accessed from anywhere in the world unlike on-premises file shares. To give access to private files for a specific period of time SAS(Shared Access signature) can be used. This is just a fancy way to say that you will be able to access a private resource using a special token for a little while.

<img src="/images/azure/sas.png">

# Azure Database and Analytics Services

## Cosmos DB

Azure Cosmos DB is flexible. At the lowest level, Azure Cosmos DB stores data in atom-record-sequence (ARS) format. The data is then abstracted and projected as an API, which you specify when you're creating your database. Your choices include SQL, MongoDB, Cassandra, Tables, and Gremlin. This level of flexibility means that as you migrate your company's databases to Azure Cosmos DB, your developers can stick with the API that they're the most comfortable with.

## Azure SQL Database

SQL is a relational database. Azure SQL Database is a Platform as a service model and handles most of the database management functions, such as upgrading, patching, backups, and monitoring, without user involvement.SQL Database is a fully managed service that has built-in high availability, backups, and other common maintenance operations. 

It provides easy migration service too where mostly everything is handled by the azure migration assistant and all you need to do is change the connection string in your app.

(PS: LAMP stack is linux, apache, mysql, php)

## Azure database for PostgreSQL

Like all databases it has high availability, automatic scaling, pay as you go, easy migration, automatic backups, monitoring, security and compliance etc.

It is available in two deployment options:

- Single server: consists of three pricing Basic, General Purpose, and Memory Optimized. This is the normal use case. nothing fancy.
- Hyper scale (citus): this option scales queries across multiple machines. often used for running queries on large databases. It is used for apps that require big scale and high performance. (data size >100 GB)


## Azure SQL Managed Service

This is another Paas like Azure SQL database. [difference between Azure SQL and Azure SQL Managed instance](https://docs.microsoft.com/en-us/azure/azure-sql/database/features-comparison)

## Azure analytics solutions

- Azure synapse analytics
- Azure HDInsight
- Azure Databricks
- Azure Data LAke analytics

[12 Oct 2021]
# Core Solutions and Management Tools on Azure

1. IOT

IOT solutions collect data from the physical world and send and receive data to/from a server  like azure for analysis and instructions. Some common uses of IOT are:

    Environmental sensors that capture temperature and humidity levels.
    Barcode, QR code, or optical character recognition (OCR) scanners.
    Geo-location and proximity sensors.
    Light, color, and infrared sensors.
    Sound and ultrasonic sensors.
    Motion and touch sensors.
    Accelerometer and tilt sensors.
    Smoke, gas, and alcohol sensors.
    Error sensors to detect when there's a problem with the device.
    Mechanical sensors that detect anomalies or deformations.
    Flow, level, and pressure sensors for measuring gasses and liquids.

IOT devices communicate with a central server through the internet. They send data and receive instructions like commands they need to perform or software updates. The data from iot devices can be used to determine if they face any error, use tht data for training ML models, etc.

## Azure IOT hub

Its an azure service to act as a command and control server for bi-directional communication with the iot device. It can also really iot data to other azure services. Also helping with monitoring the iot device for errors, restarts etc. This is good for all the cases where regular customization is not needed and regular monitoring of devices is not critical.

## Azure IOT Central

IT is built on top of IOT hub and adds the functionality of dashboards. The dashboard can be used for monitoring,connect and manage the iot device. The UI of iot central makes it easy to perform all the above tasks. There are pre-built dashboard templates for use-cases like health, energy, retail etc. which you can customize later. This gives us complete control over all the iot devices on a large scale. upgrading software, pushing new commands/software in a bulk becomes easy and the dashboard give us a clear view of all the connected devices in one place. 

## Azure Sphere

Azure Sphere is an IOT solution that customers can use to create their iot devices. It focuses more on the security part of IOT. It ensures secure sending and receiving of messages. 

Below image shows an microsoft sphere micro controller which is responsible for processing the operating system and signals from attached sensors

<img src="/images/azure/mcu.png">

Azure sphere come with customized Linux OS installed which has a security service for communication and can run the vendor's software. Azure sphere come with azure sphere security service which ensures that the device hasn't been tampered with or maliciously compromised. It authenticates with the azure service before performing any other data exchange.

# Azure AI Services

There are two ways to deploy AI:
- deep learning system that's modeled on the neural network of the human mind, enabling it to discover, learn, and grow through experience.
- machine learning, a data science technique that uses existing data to train a model, test it, and then apply the model to new data to forecast future behaviors, outcomes, and trends.

Products for AI services in Azure:
- Azure Machine Learning: It consists of tools and services that allow you to connect to data to train and test models to find one that will most accurately predict a future result. deploy best performing models to API so that it can be consumed by other apps.
- Azure Cognitive Services: provides prebuilt machine learning models that enable applications to see, hear, speak, understand, and even begin to reason.
- Azure Bot Service: Azure Bot Service and Bot Framework are platforms for creating virtual agents that understand and reply to questions just like a human

# Azure DevOps solutions

I have little knowledge/interest of devops and software development cycles and processes so this section of notes will be small like the AI section.

Here is the basic process of a common CI/CD (Continuous integration/ continuous deployment) pipeline:

pull latest code from repo-> compile source code to binary/library -> move compiled binary to a location for testing -> deploy the binary to production

Apart from this there are many other factor in this pipeline:
- after code is pulled, check commit msgs
- add tags to repo
- create work items like todo list
- perform unit tests, integration tests
- perform static analysis and make sure code is free from vulnerabilities
 
and so on...

Some azure devops services:
- Azure repos: repositories for the software
- Azure boards: agile project management suite that includes Kanban boards, reporting, and tracking ideas and work from high-level epics to work items and issues
- Azure pipeline: CI/CD automation tool
- Azure Artifacts: repository for hosting artifacts, such as compiled source code, which can be fed into testing or deployment pipeline steps.
- Azure test plans: automated test tool that can be used in a CI/CD pipeline to ensure quality before a software release.


Github and github actions can also be used for devops purposes. Github is known more for open source whereas azure devops is known more for enterprise software development with more fine tuned tools.

Azure dev test labs: provides an automated means of managing the process of building, setting up, and tearing down virtual machines (VMs) that contain builds of your software projects. This helps developers in performing tests on variety of environments.

Azure devops has a finer access control mechanism compared to github which has mostly read/write permissions.

# Azure management tools

available in 2 types:
- visual: visually friendly access to all the functionality of Azure. However, visual tools might be less useful when you're trying to set up a large deployment of resources with interdependencies and configuration options.
- code-based:When you're attempting to quickly set up and configure Azure resources, a code-based tool is usually the better choice. 

When code is written to setup and configure infrastructure it is known as infrastructure as code. This can be achieved in 2 ways:
- imperative code: details each step to be performed to achieve an outcome
- declarative code: just defines the desired outcome and allows and interpreter to make the decision on how to achieve it

Azure Administrative tasks can be performed based on different scenarios:

Azure Portal: a web-based user interface, you can access virtually every feature of Azure. When using this portal gets repetitive code based approach makes more sense.

Azure mobile app: helps monitor your azure resources,check , perform administrative tasks and fix errors and issues like restarting VMs or webapp, run azure cli or azure powershell.

Azure Powershell and Azure cli: a method with which you can interact with azure resources/cloud using a command line like bash/ terminal/ powershell. Difference between azure powershell and azure cli is only that of the syntax. (think bash/powershell)

ARM templates: These are templates of group of resources that you usually use together. For example if you often find yourself deploying a LAMP stack using azure you don't have to do it again and again. just write an ARM (azure resource template) and you will be able to deploy as many of those templates in a quicker way. You can define the configurations you want for a particular template and just deploy an infrastructure! There are also pre-built templates available for use.

# Azure monitoring solutions

- Azure Advisor: evaluates your Azure resources and makes recommendations to help improve reliability, security, and performance, achieve operational excellence, and reduce costs.
- Azure monitor: a platform for collecting, analyzing, visualizing, and potentially taking action based on the metric and logging data from your entire Azure and on-premises environment.

<img src="/images/azure/monitor.png">

This data can be used to set alerts for critical events via SMS, email etc. or use threshold to trigger auto scaling.

- Azure Service health: provides a personalized view of the health of the Azure services, regions, and resources you rely on. It can inform you about planned maintenances or outages. After any such incident a report called Root cause analysis is generated.

[13 Oct 2021]

# Protection Against security threats in Azure

Azure Security center: monitoring service that provides visibility of your security posture across all of your services, both on Azure and on-premises. The term security posture refers to cybersecurity policies and controls, as well as how well you can predict, prevent, and respond to security threats.

- monitoring security settings
- automatically apply security settings to new resources
- provide security recommendations
- perform automatic security assessments
- use ML to catch and block malware on resources like VMs
- detect incoming attacks and help analyze them
- alert when sensitive files are changed
- allow only required software to install
- provide just-in-time access control for network ports.(basically helps reducing attack surface and allow only the needed services)

<img src="/images/azure/seccenter.png">

Resource security hygiene provides health of resources from a security perspective

<img src="/images/azure/hygiene.png">

Azure Secure Score: It provides a score based on security controls and recommendations. Score is calculated based on how many controls we pass.

## Protection against threats

Azure provides some defense capabilities for resources:
- Just-in-time VM access: This access blocks traffic by default to specific network ports of VMs, but allows traffic for a specified time when an admin requests and approves it.
- Adaptive application controls: we can define which applications are allowed to run on a VM. A ML model runs in background that triggers an alert If any unauthorized apps runs.
- Adaptive network hardening: Looks at the current network traffic and the network security group to provide recommendations for further hardening.
- File integrity monitoring: alert when important files are changed

Security center event/alerts can be used as triggers for azure workflow to perform automated actions like stopping resources, message on ms teams or create and email etc.


## Azure Sentinel

Azure Sentinel is a cloud based SIEM (security information and event management) tool. It can:

-  Collect cloud data: To analyze security events it can collect data from microsoft solutions like Office365, active directory and windows defender firewall, non microsoft solution like AWS cloudtrail, Citrix,Sophos firewall, VMware carbon black cloud etc. Other sources which export data in CEF (common event format), syslog, REST APIs data can also be digested.

- Detect Threats: We can use either pre built rules for detecting malicious activity or make our own custom rules.
- Investigate and respond: It provides information regarding an incident. It can show the events and related info in the form of a graph for better investigation.

<img src="/images/azure/sentinel.png">

Automatic responses can also be setup for alerts. It has all the features that any other SIEM have like ticket system for alerts, sending automated messages via teams messages or emails with option to "block" or "ignore". "Block" option to block the IP address that is related to the event and disable the user in Azure AD. "Ignore" closes the alert ana no further action is required.

## Azure key vault

a centralized cloud service for storing an application's secrets(passwords, encryption keys and certificates) in a single, central location. It provides secure access to sensitive information by providing access control, monitoring and logging capabilities.

It can also work with [HMS](https://en.wikipedia.org/wiki/Hardware_security_module) to store sensitive data. And like any other service in azure it can be integrated with other services in azure. 

These keys and secrets can be accessed using azure powershell, cli, cloudshell(A browser based shell to access microsoft azure and its resources) or any other programming language of choice.

Then we follow an exercise on creating a secret in the vault and accessing it from azure portal and then from azure cloudshell. After I was done I decided to clean up the vault myself instead of the auto-removal that happens when a sandbox ends.

This was a great exercise because you can do all sorts of stuff apart from handling the key-vault. I tried finding info about my account.

I read through the `az -h` and `az keyvault -h` to navigate .

<img src="/images/azure/accinfo.png">

{%highlight text%}
az keyvault delete --name my-keyvault-123 --subscription "Concierge Subscription"
{%endhighlight%}

You can do other things too but this much extra activity was enough for me.

## Azure Dedicated hosting

Normally all the hardware is shared with other customers (workload is not affected) and is managed by azure. Due to compliance reasons organizations may need to have the whole hardware to themselves.

Dedicated hosts gives us full control over the whole infrastructure be it the processors, VM sizes, visibility, etc. These dedicated serves are hosted in a host group (bunch of dedicated servers in a group) and then VMs are deployed across them.


# Secure Networks on Azure

Defense in depth: The objective of defense in depth is to protect information and prevent it from being stolen by those who aren't authorized to access it.

Layers of defense in depth:

<img src="/images/azure/did.png">

- Physical: protecting hardware in the data center
- Identity and access: access to the infrastructure, SSO and MFA, audit changes and events
- Perimeter: Protection from Ddos and other attacks using perimeter firewalls
- Network: limit communication between resources, deny by default(block all inbound and outbound traffic that has not been expressly permitted by firewall policy)
- Compute: secure access to VMs, implement endpoint protection and keep systems patched and up-to-date
- Application: ensure apps are free of vulnerabilities, storing secrets in a secure storage, security as a requirement in development process
- Data: ensure data is properly secured


Security Posture: Your security posture is your organization's ability to protect from and respond to security threats. It is defined using the CIA triad. 

(A fun talk I had with some of my peers from security was about the order of importance of the elements of the CIA triad. I decided to go with AIC. So according to me Availability > Integrity > Confidentiality. Most of them said ACI)

[14 OCt 2021]

## Azure Firewall

A Cloud based stateful (analyzes context of network connection )firewall that protects your azure resources.

<img src="/images/azure/firewall.png">

It uses azure threat intelligence to allow or block traffic, provides a monitoring service(performing metrics), has automatic scaling etc

WE can whitelist domain names for access from the subnet, create network rules (ports, destination ets). Azure Application Gateway also provides a firewall that's called the web application firewall (WAF). WAF provides centralized, inbound protection for your web applications against common exploits and vulnerabilities. Azure Front Door and Azure Content Delivery Network also provide WAF services.

## Ddos Attacks

Ddos is when massive amounts of network requests/connections are made on a server to exhaust its resources and hence make it slow/inoperable. 

<img src="/images/azure/dos.png">

Dos protection is necessary because it can harm your business. Another reason (which I think is really cool) is that when you have azure autoscaling, it auto-scales your infra according to rate of incoming requests, now since the requests made in the attack is high it results in increased costs for resources.

Azure Ddos protection also helps prevent volumetric attacks, protocol attacks (vulnerability in protocols) and Application layer attacks (think a web application attack)

Network security groups: (we talked about this above) is like an internal firewall with rules for inbound and outbound requests.

NSG rules:
- Name
- priority: number between 100 and 4096. lower the number higher the priority. higher priority rules are processed first.
- Source/destination: IP(s), resource tags or application sec group
- protocol: TCP/UDP or any other
- Direction: inbound or outbound
- Action: allow or deny

Exercise time! (always fun, im not being sarcastic I genuinely like them)

Here we create a VM, install a web server, configure it to take requests from the internet and then configure NSGs! All through azure cli on cloud shell.

So I completed the whole exercise and again did the cleanup myself.

<img src="/images/azure/stop.png">

And then de-allocated the VM in the same way! We can try so many other command regarding VMs. But I just saved the exercise and moved on because time is money and I'm on a budget!

# Azure Identity Services

## Azure Active Directory

Azure Active Directory (Azure AD) provides identity services that enable your users to sign in and access both Microsoft cloud applications and cloud applications. So just like a normal AD which is used for signing in and access management. The difference is azure AD can be accessed globally. azure ad can help detect suspicious sign-ins from unknown locations or devices. 

Each organization on azure AD is known as a tenant. You can connect your existing AD with azure AD using azure ad connect. Azure AD Connect synchronizes user identities between on-premises Active Directory and Azure AD. Azure AD Connect synchronizes changes between both identity systems, so you can use features like SSO, multi-factor authentication, and self-service password reset under both systems. Self-service password reset prevents users from using known compromised passwords.

<img src="/images/azure/tent.png">

functions of azure AD:
- Authentication: verifying identity for access to resources and apps. also has self service password reset functionality where no IT person is needed, MFA, banned passwords and smart lockout.
- Single sign-on: Signing in once enables you to access multiple apps and resources and there is no need to login again and again. For example if you login to your microsoft account provided by your company you are able to access all the apps like microsoft teams, outlook, share point etc.
- application management
- device management: azure ad allows for device registration after which device based access controls can be implemented to only known devices.

Azure Ad helps secure external resources like Office365,Azure portal,Saas etc. and internal resources like apps in the corporate network or the intranet.

## Azure conditional Access

Conditional Access is a tool that Azure Active Directory uses to allow (or deny) access to resources based on identity signals. These signals include who the user is, where the user is, and what device the user is requesting access from. a user might not be challenged for second authentication factor if they're at a known location but they might be challenged for a second authentication factor if their sign-in signals are unusual or they're at an unexpected location.

# Cloud Governance

Governance in cyber security is establishing and enforcing a set of rules and policies. 

rbac is role based access control applied to a scope (a resource or a group of resources). RBAC in azure:

<img src="/images/azure/scope.png">

RBAC is implemented through the IAM pane in azure portal:

<img src="/images/azure/iam.png">

## Prevent accidental changes using resource locks

As the name suggests resource locks prevent accidental modification or deletion of resources. For ex while cleaning up unused resources you accidentally delete a resource which was critical to production server... (*Panic screams in the background*)

<img src="/images/azure/lock.png">

Locks can be applied to subscriptions,resource groups or individual resources. There are 2 types of locks:
- CanNotDelete: Even the people with right privileges cannot delete a resource until the lock is removed explicitly
- ReadOnly: this lock is similar to the read-only access control

To prevent accidental deletion of the locks themselves, azure blueprints can be used, which defines a set of resources that are integral to your infrastructure. If these resources are deleted they are automatically replace with a new one tat looks the same. (more on this later...)

PS: Be careful while deleting a resource group. It will delete all the resources that are inside that group. ALL OF THEM!

## Tags

Tagging resources help in organizing your infrastructure. A good organization strategy helps you understand your cloud usage and can help you manage costs. For example tag the resource used for testing purposes and the resources used for production. 

Tags help in:
- resource management (testing,production)
- cost management: group resources according to tags and calculate/predict costs
- operation management: tag critical resources to business. (SLA)
- security: tag resources based on sensitivity (public, private)
- Governance and compliance
- workload optimization and automation

You can also manage tags by using Azure Policy. For example, you can apply tags to a resource group, but those tags aren't automatically applied to the resources within that resource group. You can use Azure Policy to ensure that a resource inherits the same tags as its parent resource group.

## Control and audit your resources by using Azure Policy

Azure Policy is a service in Azure that enables you to create, assign, and manage policies that control or audit your resources. These policies enforce different rules and effects over your resource configurations so that those configurations stay compliant with corporate standards.

A group of policies is known as initiatives. Azure Policy evaluates your resources and highlights resources that aren't compliant with the policies you've created. Azure Policy can also prevent noncompliant resources from being created. Azure Policy comes with a number of built-in policy and initiative definitions that you can use, under categories such as Storage, Networking, Compute, Security Center, and Monitoring.

For ex. you don't want VMs in your environment to exceed a certain size. creating a policy for will scan all the present VMs , or any in the future. Accepting requests from only certain regions, number of Vms, you can deploy, MFA on accounts with write permissions and so on...

Policy assignment is when we assign the policy to subscription(s), resource groups,or a resource. Policies are inherited by members of the resource group.(members can be also excluded). These policies are evaluated over resources every hour. 

A set of policies are known as initiatives. for ex: Azure Policy includes an initiative named Enable Monitoring in Azure Security Center. Its goal is to monitor all of the available security recommendations for all Azure resource types in Azure Security Center. This initiative includes policies like monitor un-encrypted SQL databases, monitor Os vulnerabilities, etc

<img src="/images/azure/policy.png">

## Azure Blueprints

Instead of having to configure features like Azure Policy for each new subscription, with Azure Blueprints you can define a repeatable set of governance tools and standard Azure resources that your organization requires. Each component of a blueprint is known as an artifact.It is possible for artifacts to have no additional parameters (configurations). An example is the Deploy threat detection on SQL servers policy, which requires no additional configuration.

Azure has pre-built blueprints for standards such as ISO 27001. 

## Azure Cloud Adoption framework

(Its late night and this topic is really boring, just read it from source)

https://docs.microsoft.com/en-us/learn/modules/build-cloud-governance-strategy-azure/9-accelerate-cloud-adoption-framework

[15 Oct 2021]

# Privacy, compliance and data protection in azure 

(Boring alert: The content you are about to read is really really boring. Read it at your own risk.)

compliance means to adhere to a law, standard, or set of guidelines. Regulatory compliance refers to the discipline and process of ensuring that a company follows the laws that governing bodies enforce.

Microsoft's online services build upon a common set of regulatory and compliance controls. Think of a control as a known good standard that you can compare your solution against to ensure security. These controls address today's regulations and adapt as regulations evolve.

The following compliances offered by azure:

<img src="/images/azure/compliance.png">

[For more info about various compliances](https://docs.microsoft.com/en-us/learn/modules/examine-privacy-compliance-data-protection-standards/2-explore-compliance-terms-requirements)

The Microsoft Privacy Statement explains what personal data Microsoft collects, how Microsoft uses it, and for what purposes.

The Online Services Terms (OST) is a legal agreement between Microsoft and the customer. The OST details the obligations by both parties with respect to the processing and security of customer data and personal data

The Data Protection Addendum (DPA) further defines the data processing and security terms for online services. These terms include:

    Compliance with laws.
    Disclosure of processed data.
    Data Security, which includes security practices and policies, data encryption, data access, customer responsibilities, and compliance with auditing.
    Data transfer, retention, and deletion.

The Trust Center is an important part of the Microsoft Trusted Cloud Initiative and provides support and resources for the legal and compliance community.

Clicking on any standard in the azure trust center you see:

    An overview of the standard.
    Which cloud services are in scope.
    An overview of the audit cycle and links to audit reports.
    Answers to frequently asked questions.
    Additional resources and white papers.

**Azure compliance documentation**

PCI DSS, seeks to prevent fraud through increased control of credit card data. The standard applies to any organization that stores, processes, or transmits payment and cardholder data.

The Azure compliance documentation provides you with detailed documentation about legal and regulatory standards and compliance on Azure.

**Azure government**

It addresses the security and compliance needs of US federal agencies, state and local governments, and their solution providers. Azure Government offers physical isolation from non-US government deployments and provides screened US personnel. To provide the highest level of security and compliance, Azure Government uses physically isolated datacenters and networks located only in the US. Azure Government customers, such as the US federal, state, and local government or their partners, are subject to validation of eligibility.

**Azure china 21vianet**

Azure China 21Vianet is operated by 21Vianet. It's a physically separated instance of cloud services located in China. According to the China Telecommunication Regulation, providers of cloud services, infrastructure as a service (IaaS) and platform as a service (PaaS), must have value-added telecom permits. Only locally registered companies with less than 50 percent foreign investment qualify for these permits. To comply with this regulation, the Azure service in China is operated by 21Vianet, based on the technologies licensed from Microsoft.

It offers almost the same services as the original azure.

# Planning and managing azure costs

TCO calculator: Total cost of ownership is a calculator that can help you compare the cost of running in the data-center versus running on Azure. Then you review the suggested industry average cost (which you can adjust) for related operational costs. These costs include electricity, network maintenance, and IT labor. You're then presented with a side-by-side report. Using the report, you can compare those costs with the same workloads running on Azure.

<img src="/images/azure/break.png">

TCO work by taking your workloads(servers, databases,storage,networking), assumptions(importing already bought licenses for software to azure, replicate on-premises storage, electricity, pay rate for IT admins,network maintenance costs etc) to guess the overall costs. And then shows a comparison of the two:

<img src="/images/azure/compare.png">

<img src="/images/azure/costs.png">

How can azure services be purchased:
- Enterprise agreement: large customers enter an agreement for using resources over a period of three years and pay annually.
- directly from web: like any normal person but the resources from the azure portal
- through a CSP:  A cloud service provider helps customers build solutions on top of azure and charge the customer.

Factors affecting cost:

- resource type
- usage meters: When you provision a resource, Azure creates meters to track usage of that resource. Azure uses these meters to generate a usage record that's later used to help calculate your bill. fo ex for a VM , meters may record CPU time, network traffic, disk read/writes etc.
- resource usage: pay as you use. (PS: when de-allocating a VM also remember to de-allocate any storage/disks associated with it which might lead to incurring costs for resources you didn't even use.)
- azure marketplace: purchasing azure based solutions from third party vendors.
- location: geographic regions can impact where your network traffic flows, network traffic is a cost influence to consider as well.
- zones for billing of network traffic: Bandwidth refers to data moving in and out of Azure datacenters. Some inbound data transfers (data going into Azure datacenters) are free. For outbound data transfers (data leaving Azure datacenters), data transfer pricing is based on zones.

## Pricing calculator

The Pricing calculator displays Azure products in categories. You add these categories to your estimate and configure according to your specific requirements. You then receive a consolidated estimated price, with a detailed breakdown of the costs associated with each resource you added to your solution.

<img src="/images/azure/price.png">

This is not the actual price but just an estimate.

Azure advisor: provides advise (well duh...) about unused or underutilized resources and recommends unused resources that you can remove. This information helps you configure your resources to match your actual workload.

<img src="/images/azure/advisor.png">

You can configure spending limits for credit based accounts. If you have a credit-based subscription and you reach your configured spending limit, Azure suspends your subscription until a new billing period begins.

Azure Reservations offers discounted prices on certain Azure services. Azure Reservations can save you up to 72 percent as compared to pay-as-you-go prices. To receive a discount, you reserve services and resources by paying in advance.

The cost of Azure products, services, and resources can vary across locations and regions. If possible, you should use them in those locations and regions where they cost less.But remember to put resources that they communicate with them in the same region otherwise you will incur costs dur to network bandwidth usage.

Azure Cost Management + Billing is a free service that helps you understand your Azure bill, manage your account and subscriptions, monitor and control Azure spending, and optimize resource use. It has the following features:
- reporting: look at past usage and try to predict the future usages
- data enrichment: organize resources  with tags
- budgets: Create and manage cost and usage budgets by monitoring resource demand trends, consumption rates, and cost patterns.
- alerting: Get alerts based on your cost and usage budgets.
- recommendations

Tags are a great way for managing anything. organizing resources, getting insights on costs incurred by specific teams (and respond accordingly) etc. Resizing underutilized VMs, de-allocating VMs during off hours(their state remains the same because the hard is not de-allocated),deleting unused resources, migrate Iaas to Paas(they are cheaper and easier to manage, for ex using azure sql database instead of running SQL server on a VM), choosing cost effective operating systems (yes, it costs different for different OSs)

# Service Level Agreements and service lifestyle

A service-level agreement (SLA) is a formal agreement between a service company and the customer that guarantees a level of service (availability/uptime). For Azure, this agreement defines the performance standards that Microsoft commits to for you, the customer. Each azure resource has its own SLA.

<img src="/images/azure/sla.png">

A service credit is the percentage of the fees you paid that are credited back to you according to the claim approval process.

An SLA describes how Microsoft responds when an Azure service fails to perform to its specification. For example, you might receive a discount on your Azure bill as compensation when a service fails to perform according to its SLA.

composite SLA are derived by multiplying the SLA of each individual service used in an app. Givin you the total availability SLA for that app. 

Free services don't have SLAs. Azure status provides a view of health of azure services and regions.

An application SLA defines the SLA requirements for a specific application. This term typically refers to an application that you build on Azure.

## Service lifecycle

The service lifecycle defines how every Azure service is released for public use. First it goes into development where requirements are defined and collected to start building. Next the service goes to public preview phase where the public uses the service and provides feedback.After a new Azure service is validated and tested, it's released to all customers as a production-ready service. This is known as general availability (GA).

preview services can be found from the resource center.