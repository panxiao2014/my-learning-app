# 🚀 Overview

This is a complete guide of building a web application with CI/CD support. It includes:

* Build a framework of web application with fronentend, backend and database support.
* Run application in local and Docker environment.
* Setup and run test cases for the application.
* Continuous Integration by Github Actions.
* Deploy application to AWS.

It is focusing on the process of setup the CI/CD not the features the source code provides. Once we have completed the process we can enjoy the efficient developmenting streamline, adding any feature we want with regression test and deploy it to AWS with minimum effort.

# 💡 How to use it

The best way is to create an empty repository, then follow the tutorials step by step to setup the whole developing environment. Feel comportable with task in each of the tutorial, and then go to next one.

# 🔧 Dependencies

I am doing this project in a Windows 11 laptop, with the following software and packages:

* Python 3.13.7
* Uvicorn (install by "pip install uvicorn")
* npm 10.9.3 (install Node.js)
* PostgreSQL server 17.6 running in local
* Ubuntu 22.04.5 running on WSL

Other tools are not mentioned here but we can install them whenever they are needed during tutorials.

# ⚒️ Quick setup

If you want to run the application in local host without following the tutorials, here are the steps.

## Download source code and install dependencies

>git clone git@github.com:panxiao2014/my-learning-app.git
>
>cd my-learning-app
>
>python -m venv .venv
>
>.venv\Scripts\activate
>
>cd backend
>
>python -m pip install --upgrade pip
>
>pip install -r requirements.txt
>
>playwright install
>
>cd ../frontend
>
>npm install

## Setup database

Install PostgreSQL server, create a database named "userdb" by user postgres:

>psql -U postgres
>
>CREATE DATABASE userdb;


Make sure to add a password to user postgres:

>\password postgres

After set the password, quit psql:

>\q

Create a folder named **tokens** in folder **backend**, and create a file named **postgresql.txt** in this folder, write the postgres password to this file. 

## Start backend and frontend

>cd backend
>
>uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

In another console window:

>cd frontend
>
>npm run dev

Then you can access the web application through port 5173.

# 🐋 Run in Docker

If you want to run the application in Docker without following the tutorials, here are the steps.

## Build images

Build images for frontend and backend:

>docker build -f Dockerfile-frontend -t my-frontend:latest .
>
>docker build -f Dockerfile-backend -t my-backend:latest .

## Set database password

>export POSTGRES_PASSWORD=\<database password\>

## Start application

>docker-compose up

Then you can access the web application through port 80. 