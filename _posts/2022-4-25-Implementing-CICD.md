---
title: Getting started with CICD
tags:
- technology
- DevOps
image: /images/cicd/info.png
---

Heyo! remember me? Me niether. So I just setup a CICD for one of my projects. I am now 50% bald. I'm documenting about every issue I  faced and how I solved it.

<!--more-->

Steps:
- Create a basic Flask web application
- Create basic tests for the code
- Containerize the whole application using docker
- Create Github actions to automate testing
- Create Github actions to automate deployment to Heroku

[Checkout the final product here](https://github.com/vandanrohatgi/Project-OSINT)

## Step 1. Creating a basic flask application

So I am working on a not so basic flask application right now. But I'm assuming you do and already have a working application.

## Step 2. Creating tests using Pytest

I used Pytest to write some very basic tests for testing functionality and authentication.

How I wrote tests for my flask application:

`conftest.py`

{% highlight text %}
from app import flask_app
import pytest

@pytest.fixture
def app():
    app=flask_app()
    app.config.update({"TESTING":True,})
    yield app

@pytest.fixture
def test_client(app):
    client=app.test_client()
    return client
{% endhighlight %}

`test_flask.py`

{% highlight text %}
import json
from unittest.mock import patch

def test_index(client):
    response=client.get("/")
    assert response.status_code==200

def test_index_response(client):
    response=client.get("/")
    assert response.json["msg"]=="API works!"

@patch('flask_jwt_extended.view_decorators.verify_jwt_in_request') ### disable jwt_required() (authentication) for this test
def test_auth(mock_jwt_token,client):
    response=client.post("/login",data=json.dumps({"username":"test","password":"test"}),content_type="application/json")
    assert response.status_code==200
    assert 'access_token' in response.json.keys()

    response=client.get("/getScanInfo")
    assert response.status_code == 200

def test_unauth(client):
    response=client.get("/logout")
    assert response.status_code == 401
    response=client.get("/getScanInfo")
    assert response.status_code == 401
    response=client.post("/start")
    assert response.status_code == 401
{% endhighlight %}

- Create a `/tests` directory in the root.
- If you have any tests that require a resource before testing, use @pytest.fixture to create those. For example I needed a test client to test the requests to my flask API. So I added that to my conftest.py.
- Next to test functionality I added a few tests.
- remember to name the test files to contain "test" in the front or the back of the filename.
- To run the tests, use `pytest` from the root directory

I was facing troubles with paths while using pytest. Pytest was not able to find the modules/files in my application. To solve that I turned my application to a module and installed it. Though there are much easier ways to this, but due to my directory structure I had to do this to setup my paths. 

To turn any application into a module you need to create a setup.py file.

## Step 3. Containerize the application

So this application consists of two components. One is a backend written in Python and the other is a frontend written in ReactJS (Created by my fellow workers). 

\
 \ - Project-OSINT
    | - backend
    | - frontend

{% highlight text %}
\
 \ - Project-OSINT
    | - backend
       \ - Dockerfile
       | - app/
    | - frontend
      \ - Dockerfile
      | - app/
     
{% endhighlight %}

I create two Dockerfiles. one for frontend and other for the backend. Backend:


{% highlight text %}
FROM python:3.9-alpine
COPY . /backend/
WORKDIR /backend/app
RUN python3 db.py
WORKDIR /backend
RUN pip install -r requirements.txt
RUN pip install -e .
ENV FLASK_APP=/app:flask_app
CMD flask run --host 0.0.0.0 --port $PORT
{% endhighlight %}

- We use the python3.9 alpine image.
- move all the code the /backend
- change the current working directory
- install the requirements and the backend module
- tell flask about the file and function that will run the app, by setting the environment variable.
- Finally define the command that will be run when we start a container from this image

I took the value of port from $PORT variable due to complexities faced when hosting on Heroku. More on this later.

frontend:

{% highlight text %}
FROM node:alpine
WORKDIR /frontend
EXPOSE 3000
COPY . .
RUN npm i
#RUN npm run build
CMD ["npm","run","start"]
{% endhighlight %}

Similarly we create one for nodeJS. One thing I found was that the "EXPOSE" command is not of much importance since we need to define the port to publish during the  "docker run" command anyway.

Finally to deploy the whole application (front and back) we create a simple docker-compose.

{% highlight text %}
version: '3.9'
services:
  backend:
    build: ./backend
    ports: 
      - "5000:5000"
    container_name: OSINT_backend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    container_name: OSINT_frontend
{% endhighlight %}

we just need to guide the file in which folder does the respective Dockerfiles reside. So now it can go build the images and then create a container from them.

Remember, when your backend and frontend are not running on the same host, you will face a CORS issue. You will need to modify your backend code to accept requests from other domains. 

Next we tell the react frontend about the URL on which frontend is running so that we can connect the two. We do this using an .env file inside the frontend folder.

`REACT_APP_API_HOST=http://localhost:5000`

Now all you need to run the whole thing is `docker-compose up` from the root folder.

## Step 4. Github Actions for Continuous integration

Now when your pytest command starts working on the localhost we can create a github action for it, which will be triggered whenever changes are pushed to the master branch. The use for this is, whenever someone pushes some code, it is automatically tested for intended behaviour. 

{% highlight text %}
name: Python application

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      working-directory: backend/
      run: |
        python -m pip install --upgrade pip
        python -m venv venv
        source venv/bin/activate
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        pip install -e .
    - name: setup db files
      working-directory: backend/app/
      run: |
        python db.py
    - name: Test with pytest
      working-directory: backend/
      run: |
        source venv/bin/activate
        pytest
{% endhighlight %}

- We first name the action
- define when should it trigger. We define that it should trigger on push to master branch.
- we define `runs-on` as ubuntu, which is one of the most common platforms for github actions. You can define other OS like windows and other flavours too.
- Next we move on to the jobs. i.e the steps it needs to perform when it is triggered.
- `uses` is a way to use other actions in our action. We use an action to checkout our code. i.e the code on our github. Another action we use here is setup-python to create a python environment.
- Now it is just a matter of writing name of the step and it's respective shell command.

One thing I learned was to write a single line command just write it in front of the `run` keyword. To write multiple commands in on run use pipe (|).

## Step 5. Continuous deployment on Heroku

To make it so that whenver I update my application (push changes to github), it should automatically update the site where I have hosted it too. I used the Dockerfile we wrote earlier for this.

{% highlight text %}
name: Docker Image CI

on:
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: install Heroku CLI
        run: curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
      - name: heroku deploy
        working-directory: backend/
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API }}
        run: |
          heroku container:login
          heroku container:push web -a osint-backend
          heroku container:release web -a osint-backend
{% endhighlight %}

- Once again we write our initial environment setup statements.
- since I was using heroku (It is free and easy!), I first installed heroku CLI on the environment.
- Next I added my heroku API key to the environment. I used github secrets to do this. In this you just create key:value pair in your github repository. Next we refer that data using {{ secrets.YOUR_SECRET }}. It is a great way to access secrets like API keys that should not be made public.
- Finally we run the statements to build our application image, push that image and finally release it.
- `-a` is the name of the application you created on heroku before. `web` is the type of process we need. Since our application is an API, we use a web worker.

The major issue I faced with Heroku was that it assigns a port on which our app will run dynamically. which means we cannot predefine on which port our app will be accessible. Hence I used $PORT in my Dockerfile command `CMD flask run --host 0.0.0.0 --port $PORT` (to access the value of $PORT from the heroku environment). Heroku sets the $PORT env variable to tell us which port is going to be used for hosting.

That is all for this one folks! I have seen many people facing issue with github actions and Heroku, Do get in touch with me and I shall try my best to troubleshoot!