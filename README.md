# DiscoverUni

[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/dev/dev-wagtail-cms?branchName=develop&label=Dev%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=9&branchName=develop)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/pre-prod/pp-wagtail-cms?label=Pre%20prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=11)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/prod/prod-wagtail-cms?branchName=master&label=Prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=12&branchName=master)

<!-- vim-markdown-toc GitLab -->

* [About this application](#about-this-application)
    * [Purpose of this app](#purpose-of-this-app)
    * [Tech stack](#tech-stack)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
    * [Without Docker](#without-docker)
    * [With Docker](#with-docker)
  * [Running the database](#running-the-database)
  * [Environment variables](#environment-variables)
  * [Running the site](#running-the-site)
    * [Running without Docker](#running-without-docker)
    * [Running with Docker](#running-with-docker)
      * [Useful  commands](#useful-commands)
      * [Adding new dependencies](#adding-new-dependencies)
* [Continuous Integration and Deployment Pipeline](#continuous-integration-and-deployment-pipeline)
  * [Continuous Integration](#continuous-integration)
    * [CI test](#ci-test)
    * [Development build](#development-build)
    * [Pre prod build](#pre-prod-build)
    * [Production build](#production-build)
  * [Continuous Deployment](#continuous-deployment)
    * [Development deploy](#development-deploy)
    * [Pre prod deploy](#pre-prod-deploy)
    * [Production deploy](#production-deploy)
  * [Releases](#releases)
    * [Creating A Release](#creating-a-release)
        * [Manual release process](#manual-release-process)
        * [Automated release process](#automated-release-process)
    * [Finishing A Release](#finishing-a-release)
* [Contributing](#contributing)
* [License](#license)

<!-- vim-markdown-toc -->


## About this application

### Purpose of this app

The purpose of this app is to provide a user interface for admin users to maintain the 'DiscoverUni' site content.

### Tech stack

This application is based on the Wagtail CMS.
It utilises:
- Wagtail CMS
- Python/Django framework
- jQuery
- SASS

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

| Variable                          | Default              | Description                                 |
| --------------------------------- | -------------------- | ------------------------------------------- |
| DBHOST                            | host.docker.internal | DB host url/string                          |
| DBPORT                            | 5432                 | DB connection port                          |
| DBNAME                            | discoveruni          | DB name to use                              |
| DBUSER                            | <username>           | DB user                                     |
| DBPASSWORD                        | <password>           | DB password                                 |
| SEARCHAPIHOST                     | <searchapihost>      | The url endpoint for the search api         |
| DATASETAPIHOST                    | <datasetapihost>     | The url endpoint for the dataset api        |
| WIDGETAPIKEY                      | <widgetaccesskey>    | The access key for the api for the widget   |
| DATASETAPIKEY                     | <datasetaccesskey>   | The access key for the api for the site     |
| FEEDBACK_API_HOST                 | <feedbackapihost>    | The url endpoint for the feedback api       |
| AZURE_ACCOUNT_NAME                | <azureaccountname>   | The name of the account for image storage   |
| AZURE_ACCOUNT_KEY                 | <azureaccountkey>    | The access key to account for image storage |
| AZURE_ACCOUNT                     | <azureaccount>       | The account for image storage               |
| JSONFILES_STORAGE_CONTAINER       | <azurecontainer>     | The container URI for the json files        |
| SENDGRID_API_KEY                  | <sendgridapikey>     | The API key for the e-mail notifications    |
| SENDGRID_FROM_EMAIL               | <sendgridfromemail>  | The e-mail address used for notifications   |
| LOCAL                             | False                | Tells the site to use external API or mocks |


### Running the site

#### Running without Docker

Create a Python 3.6.8 virtual environment and run the following commands from the root directory of the project:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


#### Running with Docker

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

##### Useful commands

There are commands setup in the bin directory of the project, that allow easy use of common commands inside the docker container.

- container - takes you on to the containers command line.
- manage - can be passed arguments to run standard django manage.py commands.
- shell - takes you on to the python shell command line for the project.


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

## Continuous Integration and Deployment Pipeline

The continuous integration and deployment pipeline for this project is implemented using Azure DevOps pipelines.

### Continuous Integration

The continuous integration pipeline for the project is defined in yml files in the root of the project, all starting with 'azure-pipelines'.

There are 4 pipelines defined in the project.

#### CI test
_Defined in 'azure-pipelines.yml'_

This pipeline should run on every push to Github from feature, bug and refactor branches. All this pipeline does is run the tests to regression check the new code.

#### Development build
_Defined in 'dev-azure-pipelines.yml'_

This pipeline should run on every push to Github on the develop branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the dev container registry.

#### Pre prod build
_Defined in 'pre-prod-azure-pipelines.yml'_

This pipeline should run on every push to Github from a release branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the pre-prod container registry.

#### Production build

_Defined in 'prod-azure-pipelines.yml'_

This pipeline should run on every push to Github on the master branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the prod container registry.

### Continuous Deployment

The continuous deployment pipeline is defined through the Azure DevOps pipeline UI.

There are 3 pipelines setup for the project.

#### Development deploy

The pipeline runs when the Development CI pipeline passes, it pulls the container generated by the CI build on to the WebApp server and starts the container.

#### Pre prod deploy

The pipeline runs when the a new container is pushed to the pre-prod container registry, it pulls the container on to the WebApp server and starts the container.

#### Production deploy

The pipeline runs when the a new container is pushed to the prod container registry, it pulls the container on to the WebApp server and starts the container.

### Releases

Releases of the code are following the major/minor/patch pattern for release numbering.

#### Creating a release

New releases can be generated manually or by using the 'release' command in the bin directory.

##### Manual release process

- update the version number with in the version.txt file
- create a new branch named in the pattern 'release/v`version number`' (e.g. release/v0.0.1)
- push the branch to Github

##### Automated release process

- ensure there are no uncommitted changes in your local repository
- call the 'release' command in the bin directory, passing as a parameter either major/minor/patch.

#### Finishing a release

Once a release has been signed off and deployed to production, you need to:

- merge the release branch into master and to development.
- tag master with the release number at the point it was merged in.
- delete the release branch

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

See [LICENSE](LICENSE.md) for details.