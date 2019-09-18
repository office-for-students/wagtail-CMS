# DiscoverUni

<!-- vim-markdown-toc GitLab -->

* [Purpose of this app](#purpose-of-this-app)
* [About this application](#about-this-application)
* [Getting Started](#getting-started)
  * [Running the development server](#running-the-development-server)
  * [Adding new dependencies](#adding-new-dependencies)

<!-- vim-markdown-toc -->


## Purpose of this app


The purpose of this app is to provide a user interface for admin users to maintain the 'DiscoverUni' site content.


## About this application


This application is based on the Wagtail CMS.

## Getting Started

### Prerequisites

#### Without Docker

You need to have Python (3.6.8), PIP and PostgreSQL installed. There are multiple ways to install Python, either download from the official [Python site](https://www.python.org/downloads/) or use the package manager [Homebrew](https://brew.sh/) ```brew install python3```. PIP comes installed with Python 3.4(or greater) by default.

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```


#### With Docker

You need to have Docker and PostgreSQL installed. Docker installation guidance can be found in the [Docker Docs](https://docs.docker.com/install/).

To install Postgres you can also use [Homebrew](https://brew.sh/)

```
brew update
brew doctor
brew install postgresql
```

### Running the database

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

### Environment variables

| Variable          | Default              | Description                                 |
| ----------------- | -------------------- | ------------------------------------------- |
| DBHOST            | host.docker.internal | DB host url/string                          |
| DBPORT            | 5432                 | DB connection port                          |
| DBNAME            | discoveruni          | DB name to use                              |
| DBUSER            | <username>           | DB user                                     |
| DBPASSWORD        | <password>           | DB password                                 |
| SEARCHAPIHOST     | <searchapihost>      | The url endpoint for the search api         |
| DATASETAPIHOST    | <datasetapihost>     | The url endpoint for the dataset api        |
| WIDGETAPIKEY      | <widgetaccesskey>    | The access key for the api for the widget   |
| DATASETAPIKEY     | <datasetaccesskey>   | The access key for the api for the site     |
| FEEDBACK_API_HOST | <feedbackapihost>    | The url endpoint for the feedback api       |
| AZURE_ACCOUNT_NAME| <azureaccountname>   | The name of the account for image storage   |
| AZURE_ACCOUNT_KEY | <azureaccountkey>    | The access key to account for image storage |
| AZURE_ACCOUNT     | <azureaccount>       | The account for image storage               |
| LOCAL             | False                | Tells the site to use external API or mocks |


### Running the site

#### Without Docker

Create a Python 3.6.8 virtual environment and run the following commands from the root directory of the project:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


#### With Docker

```
docker-compose build
docker-compose up
```

The first command builds the docker image.
The second command starts the docker container, running on port 8000.

After the docker image is running for the first time, connect to it and create an admin login as follows:

(From the route directory)
```
./bin/manage createsuperuser
```



##### Adding new dependencies

Adding a new dependency requires rebuilding docker image for Django app.

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

### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.
