---
title: AWS ECR & ECS
tags:
- technology
- DevOps
- Cloud
- Docker
image: /images/ecs/info.png
---

I worked with AWS ECR (Elastic container registry) & ECS (Elastic Container Service) a while ago and so I'm documenting some of the concepts and issues I faced while doing so.

<!--more-->

Let's define what they are first.

ECR: A registry where you can store your container images.

ECS: Here you use the images stored in ECR (Or somewhere else like dockerhub) to create containers and manage them.

# ECR

ECR is very straight forward. You can first create a repository by doing something as simple as:

`aws ecr create-repository --repository-name test-repo`

Next we push our Docker image to this repository.

{% highlight text %}
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <accountID>.dkr.ecr.<region>.amazonaws.com

docker build -t test .

docker tag docker/getting-started:latest <accountID>.dkr.ecr.<region>.amazonaws.com/test-repo:latest

docker push <accountID>.dkr.ecr.<region>.amazonaws.com/test-repo:latest
{% endhighlight %}

- login to docker using username: AWS, Password: taken from get-login-password cmd and finally URL of your ECR repository
- Build The image. This is assuming you are using a Dockerfile present in the current folder. If not and you just have an image ready, skip this step.
- Tag the image you want to push according to the format AWS needs.
- Do a simple docker push and you will be able to see your image in the repository you created.

I just pushed the getting-started docker image just to check if the server is running when we use it in ECS. Next comes the step of using this image in ECS. 

# ECS

There are several steps to use our ECR image.

### Step 1. Create Task definition

Before doing anything, we need to understand what is Fargate. ECS works using EC2 machines and deploying containers on those machines. Fargate is a service which automatically manages the EC2 machines for us. Without it we have to create, scale, patch, setup monitoring all by ourselves on our EC2 instances and register them to ECS for use. [Here is a longer comparison](https://aws.amazon.com/fargate/)

Task definition is a configuration that defines basically what your docker container will look like. It defines parameters such as the image to use, the size of container, Number of CPUs, port mappings (host:container), attach volumes, IAM role, define dependency on other containers etc. Think of this as the docker-compose file.

You can either use the console or the CLI to create this. Console is much easier since they ask everything that is needed. Whereas when using CLI you need to create a JSON with all the parameters, and this is the one we are going to use (I'm a fan of infrastructure-as-code).

`aws ecs register-task-definition --generate-cli-skeleton`

Use this command to generate a sample json to use and remove all the un-needed fields.

Here is what I wrote for my small task.

`ecs_task.json`

{% highlight text %}
{
    "family": "poc-task",
    "taskRoleArn": "arn:aws:iam::<accountID>:role/ecsTaskExecutionRole",
    "executionRoleArn": "arn:aws:iam::<accountID>:role/ecsTaskExecutionRole",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "getting-started-container",
            "image": "<accountID>.dkr.ecr.<region>.amazonaws.com/test-repo:latest",
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "interactive": true,
            "pseudoTerminal": true
        }
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "512",
    "memory": "1024",
    "runtimePlatform": {
        "cpuArchitecture": "X86_64",
        "operatingSystemFamily": "LINUX"
    }
}
{% endhighlight %}

Let's review some of the parameters:

- family: The name of the task definition
- taskRoleArn: The role that our container can assume
- executionRoleArn: The role for our containers. We use a pre-created role named ecsTaskExecutionRole which already has the needed permissions
- networkMode: host, bridge, nat, awsvpc. We are required to use "awsvpc" since it is a requirement for using FARGATE. "awsvpc" mode configures containers to have the same network as the EC2 instance they are being run on.
- containerDefinitions: Here we definesome configs for the container. In the image section we use the ID of the image we uploaded to ECR. Now if the image was hosted somewhere else such as docker hub we input "docker.io/httpd:latest" or just "httpd:latest".

[Refer this for info on all parameters](https://docs.aws.amazon.com/cli/latest/reference/ecs/register-task-definition.html)

Now just use this command to create the task definition:

`aws ecs register-task-definition --cli-input-json file://ecs_task.json`

## Step 2. Create a ECS cluster

Can we now finally create a container?! Nope. That comes after this. First we need to create a cluster for our containers. All the containers are launched inside a cluster. This can be done with a simple AWS command:

`aws ecs create-cluster --cluster-name poc-cluster`

You can add more settings to this for example container-insights and logging but this is as simple as it gets.

[Refer this for more info](https://docs.aws.amazon.com/cli/latest/reference/ecs/create-cluster.html)

## Step 3. Create Containers!

Just one more thing before that. There are two ways to do this:

1. Task: For short timed jobs. The task ends whenever the job is done or it exits on its own.

2. Service: For long term jobs. Jobs like web servers that should be up at all times use this configuration. It automatically replaces containers whenever they stop (maybe due to an error).

Now, since we are only working on a proof-of-concept of ECS we can just go ahead with a task to run our container.

Here is the command to create a new task. Remember what we are doing right now is just creating a container from the image we uploaded to ECR. Don't get confused with all the technical terms such as service, cluster, fargate etc.

`aws ecs run-task --cluster poc-cluster --count 1  --task-definition poc-task --launch-type FARGATE --network-configuration file://network.json`

`network.json`

{% highlight text %}
{
    "awsvpcConfiguration": {
        "subnets": [
            "subnet-124abcd"
        ],
        "securityGroups": [
            "sg-124abcd"
        ],
        "assignPublicIp": "ENABLED"
    }
}
{% endhighlight %}

Your container should be up and running and now you can get it's public IP using:

`aws ecs describe-tasks --tasks <taskID> --cluster poc-cluster`

You get the task ID from the "run-task" command. Browsing to this IP we see that our application is hosted!

![](https://i.imgur.com/KfAmull.png)

Recap: Create a task definition (Which is just a blueprint of the container that will be created), create a cluster(all the tasks and services are launched inside a cluster) and then run a task (create a container from the image).

This was the simplest way to do this. All the parameters in the commands and steps are the bare minimum and are required. As the requirements increase the complexity will also increase. 