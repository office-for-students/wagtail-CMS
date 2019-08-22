# uniSimple

<!-- vim-markdown-toc GitLab -->

* [Purpose of this app](#purpose-of-this-app)
* [About this application](#about-this-application)
* [Getting Started](#getting-started)
  * [Running the development server](#running-the-development-server)
  * [Adding new dependencies](#adding-new-dependencies)

<!-- vim-markdown-toc -->


## Purpose of this app


The purpose of this app is to provide a user interface for admin users to maintain the 'uniSimple' site.


## About this application


This application is based on the Wagtail CMS.

## Getting Started


### Running the site

As a prerequisite to running the site you need to have Python (3.6.8), PIP and PostgreSQL installed. There are multiple ways to install Python, either download from the official [Python site](https://www.python.org/downloads/) or use the package manager [Homebrew](https://brew.sh/) ```brew install python3```. PIP comes installed with Python 3.4(or greater) by default.

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```

To start Postgres:

```
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

Create a local database

```
CREATE DATABASE sampledb;
CREATE USER manager WITH PASSWORD 'supersecretpassword';
GRANT ALL PRIVILEGES ON DATABASE sample TO manager;
```

You have two options to run the development server:

**1.** Create a Python 3.6.8 virtual environment and run the following commands from the root directory of the project:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


**2.** Using Docker containers, which requires you to have [Docker](https://docs.docker.com/v17.12/docker-for-mac/install/) installed in order to run the site in a Docker container

```
docker-compose build
docker-compose up
```

The first command builds the docker image.
The second command starts the docker container, running on port 8000.

After the docker image is running for the first time, connect to it and create an admin login as follows:

1. Connect to the Docker image
```
docker exec -it <containerid> /bin/bash
```

2. Run the Django createsuperuser command
```
python manage.py createsuperuser
```






### Adding new dependencies

Adding a new dependency requires rebuilding docker image for Django app if you are working with Docker. After installing dependency with `pip install <dependency>` run following to update requirements.txt

```
pip freeze > requirements.txt
```

Stop docker container

```
docker-compose down
```

Rebuild Docker image

```
docker-compose build
```

Start server again

```
docker-compose up
```

## Environment variables

| Variable        | Default              | Description                       |
| --------------- | -------------------- | --------------------------------- |
| DBHOST          | host.docker.internal | DB host url/string                |
| DBPORT          | 5432                 | DB connection port                |
| DBNAME          | unisimple            | DB name to use                    |
| DBUSER          | <username>           | DB user                           |
| DBPASSWORD      | <password>           | DB password                       |


### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.
