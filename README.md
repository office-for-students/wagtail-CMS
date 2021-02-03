# DiscoverUni

[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/dev/dev-wagtail-cms?branchName=develop&label=Dev%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=9&branchName=develop)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/pre-prod/pp-wagtail-cms?label=Pre%20prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=11)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/prod/prod-wagtail-cms?branchName=master&label=Prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=12&branchName=master)

# Table of Contents

...

## Tech stack

This application is based on the Wagtail CMS.
It utilises:
- Wagtail CMS
- Python/Django framework
- jQuery
- SASS

## Rollout

### LIVE

The following command will need to be run to make the codebase work in LIVE:

```
$ cp docker-compose.yml.example docker-compose.yml
```

## Environment variables

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

# Getting Started

## Configure

### Defaults

```
$ cp docker-compose.yml.example docker-compose.yml
$ vim docker-compose.yml
...
DBHOST:               "db"
DBNAME:               "django"
DBUSER:               "docker"
DBPASSWORD:           "docker"
DBPORT:               "5432"
...
...
```

### Secret Key

```
$ python
>>> import random, string
>>> ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)])
'<secret_key>'
>>> exit()
$ vim docker-compose.yml
...
SECRET_KEY: "<secret_key>"
...
```

## Docker

You need to have [Docker Docs](https://docs.docker.com/install/) installed to be able to see changes in the code, run tests and update local data.

```
$ docker-compose up
```

> Make sure to run this command in a separate window so you have somewhere to run other commands from

> This command will download all the required images (Python, PostgreSQL, CosmosDB) and start them for you all preconfigured

## Database (PostgreSQL)

### Creating

```
$ docker container exec -it wagtail-cms_web_1 python manage.py migrate
```

### Populating

First lets get the data from the development environment in Azure.

> **IMPORTANT:** Remember to use the **REMOTE** database details below (because you are getting the data from the remote database)

```
$ vim docker-compose.yml
...
DBHOST:      "..."
DBNAME:      "..."
DBUSER:      "..."
DBPASSWORD:  "..."
DBPORT:      "..."
...
$ docker container exec -it wagtail-cms_web_1 python manage.py dumpdata --natural-foreign --indent=4 > postgres.json
```

> **IMPORTANT:** Stop docker (press Ctrl+C in the window in which you have it running)

Now put back in your local variables.

```
$ vim docker-compose.yml
...
DBHOST:      "db"
DBNAME:      "django"
DBUSER:      "docker"
DBPASSWORD:  "docker"
DBPORT:      "5432"
...
```

Restart Docker in the other window.

Now we need to create the schema in the database. Unfortunately this will also creates a number of default entries. We need to remove these default entries otherwise the import will not work.

```
$ docker container exec wagtail-cms_web_1 python manage.py migrate
...
$ docker container exec -it wagtail-cms_web_1 python manage.py shell
>>> from wagtail.core.models import Page
>>> Page.objects.all().delete()
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> exit()
$ docker container exec wagtail-cms_web_1 python manage.py loaddata postgres.json
```

> Because we have copied wholesale the data over from development you can use your original development credentials to login to the Wagtail Admin if you need to

> Also now that Wagtail has been localised you can login and change things to your hearts content. If anything breaks (irrevocably) then just just delete the PostgreSQL container (use the docker commands below) and re-do the populating as described above.

## CosmosDB

### Populating

...

# Useful Commands

## Docker

### List images

```
$ docker images
```

From this list you can find the docker images you no longer need. Copy their `IMAGE ID`

### Deleting Images

```
$ docker rm <IMAGE_ID>
```

### Listing Containers

Container are based of images. This is what runs your code

```
$ docker ps --all
```

The `NAME`s you can see in the commands above. The `STATUS` tells you whether ac container is being used. If you no longer need a container copy the `CONTAINER ID`

### Deleting Containers

```
$  docker rmi -f <CONTAINER_ID>
```

### Get into a Container

```
$ docker container exec -it wagtail-cms_web_1 bash
$ docker container exec -it wagtail-cms_db_1 bash
```

### Using the Django Shell

```
$ docker container exec -it wagtail-cms_web_1 python manage.py shell
```

##### Adding new dependencies

```
$ docker container exec -it wagtail-cms_web_1 pip install ...
$ docker container exec -it wagtail-cms_web_1 pip freeze > requirements.txt
```

# Other Stuff

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
