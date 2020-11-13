# Go Out Safe - users

[![Build Status](https://travis-ci.com/federicosilvestri/ase-GoOutSafe-s4.svg?token=wrPAra8ynq6rYZess6c1&branch=master)](https://travis-ci.com/federicosilvestri/ase-GoOutSafe-s4)
![codecov](https://codecov.io/gh/federicosilvestri/ase-GoOutSafe-s4/branch/master/graph/badge.svg?token=WN7CJ8Q74F)

This is the source code of GoOutSafe application, self
project of *Advanced Software Engineering* course,
University of Pisa.
 
## Team info

- The *squad id* is **4**
- The *team leader* is *TBD*

#### Members

|Name and Surname  | Email                         |
|------------------|-------------------------------|
|Federico Silvestri|f.silvestri10@studenti.unipi.it|
|Leonardo Calamita |l.calamita@studenti.unipi.it   |
|Chiara Boni       |c.boni5@studenti.unipi.it      |
|Nunzio Lopardo    |n.lopardo@studenti.unipi.it    |
|Paolo Murgia      |p.murgia1@studenti.unipi.it    |


## Diagrams
We have created the Class Diagram using UML to simplify
and document the project.

[Class Diagram schema](https://app.diagrams.net/#G1fXT6PbLfamFTwbCxVI-jCJrf9b1DjUMB)

## Instructions

### Initialization

To setup the project initially you have to run these commands
inside the project's root.

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### Run the project

To run the project you have to setup the flask environment,
you can do it by executing the following command:

`export FLASK_ENV=<environment-name>`

and now you can run the application

`flask run`


#### Application Environments

The available environments are:

- debug
- development
- testing
- production

If you want to run the application with development environment
you can run the `run.sh` script.


### Apply migrations

If you change something in the models package or you create a new model,
you have to run these commands to apply the modifications:

`flask db migrate -m '<message>'`

and
 
`flask db upgrade`

### Run tests

To run all the tests, execute the following command:

`python -m pytest`

You can also specify one or more specific test files, in order to run only those specific tests.
In case you also want to see the overall coverage of the tests, execute the following command:

`python -m pytest --cov=gooutsafe`

In order to know what are the lines of codes which are not covered by the tests, execute the command:

`python -m pytest --cov-report term-missing`

## Celery

In order to set up Celery, you need to open two other terminals, using the same development virtual environment. You setup both Redis, the message broker, and the Celery scheduler in the first one, while starting the Celery worker in the other one.
(Note: Redis can be set up in either one of the new terminals, there is no need to put it in the same one of the scheduler).

Execute the following command to download and run the docker container with Redis in the background:

`docker run --name=redis-devel --publish=6379:6379 --hostname=redis --restart=on-failure --detach redis:latest`

If the Redis docker has already been downloaded and created, run the following command instead :

`docker run -p 127.0.0.1:6379:6379/tcp redis`

Execute the following command to run the Celery scheduler:

`celery -A app.celery beat --loglevel=INFO`

Execute the following command to run the Celery worker:

`celery -A app.celery worker --loglevel=INFO`

## Conventions

- Name of files must be snake_cased
- Name of methods, properties, variables must be snake_cased
- Name of classes must be PascalCased 
- Name of constants must be UPPERCASE 
- The class name of managers must be in the format `<BeanName>Manager`

### Future implementations

- [Checking phone numbers](https://pypi.org/project/phonenumbers/)
