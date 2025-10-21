# 🚀 Overview

This is a complete guide of building a web application with CI/CD support. It includes:

* Build a framework of web application with fronentend, backend and database suupport.
* Run application in local and Docker environment.
* Setup and run test cases for the application.
* Continuous Integration by Github Actions.
* Deploy application to AWS.

It is focusing on the process of setup the CI/CD not the fetures the source code provides. Once we have completed the process we can enjoy the efficient developmenting streamline, with any feature we want to add with regression test to make sure its quality and deploy it to AWS with minimum effort.

# 💡 How to use it

The best way is to create an empty repository, then follow the tutorials step by step to setup the whole developing environment. Feel comportable with task in each of the tutorial, and then go to next one.

# 🔧 Dependencies

I am doing this project in a Windows 11 laptop, with the following software and packages:

* Python 3.13.7
* Uvicorn (install by "pip install uvicorn")
* npm (install Node.js)
* PostgreSQL server running in local
* Ubuntu running on WSL

Other tools are needed and we can install them whenever they are needed during tutorials.

# ⚒️ Quick setup

If you want to run the application in local without following the tutorials, here are the steps.

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
