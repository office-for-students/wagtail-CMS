# DiscoverUni

[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/dev/dev-wagtail-cms?branchName=develop&label=Dev%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=9&branchName=develop)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/pre-prod/pp-wagtail-cms?label=Pre%20prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=11)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/prod/prod-wagtail-cms?branchName=master&label=Prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=12&branchName=master)

# Table of Contents

...

## Tech stack

This application is based on the Wagtail CMS.
It utilises:
- Wagtail CMS (v7.3.2)
- Python (v3.13) / Django framework (v5.2.12)
- PostgreSQL
- Azure Blob Storage (for media and JSON files)
- Azure Communication Services (for email)
- jQuery
- SASS

## Rollout

### LIVE

The following command will need to be run to make the codebase work in LIVE:

```
$ cp docker-compose.yml.example docker-compose.yml
```

## Environment variables

| Variable                              | Default              | Description                                                      |
|---------------------------------------|----------------------|------------------------------------------------------------------|
| DEBUG                                 | False                | Enable/disable debug mode                                        |
| LOCAL                                 | False                | Tells the site to use external API or mocks/sqlite               |
| ROOT_DOMAIN                           | http://localhost:3000| The root domain of the application                               |
| ALLOWED_HOSTS                         | []                   | JSON list of allowed hosts                                       |
| CSRF_TRUSTED_ORIGINS                  | []                   | JSON list of trusted origins for CSRF                            |
| DBHOST                                | host.docker.internal | DB host url/string                                               |
| DBPORT                                | 5432                 | DB connection port                                               |
| DBNAME                                | discoveruni          | DB name to use                                                   |
| DBUSER                                | <username>           | DB user                                                          |
| DBPASSWORD                            | <password>           | DB password                                                      |
| SEARCHAPIHOST                         | <searchapihost>      | The url endpoint for the search api                              |
| DATASETAPIHOST                        | <datasetapihost>     | The url endpoint for the dataset api                             |
| WIDGETAPIHOST                         | <widgetapihost>      | The url endpoint for the widget api                              |
| V2_WIDGET_HOST                        | <v2widgethost>       | The url endpoint for the V2 widget host                          |
| WIDGETAPIKEY                          | <widgetaccesskey>    | The access key for the api for the widget                        |
| DATASETAPIKEY                         | <datasetaccesskey>   | The access key for the api for the site                          |
| AZURECOSMOSDBURI                      | <cosmosdburi>        | The URI for Azure Cosmos DB                                      |
| AZURECOSMOSDBKEY                      | <cosmosdbkey>        | The access key for Azure Cosmos DB                               |
| AZURE_ACCOUNT_NAME                    | <azureaccountname>   | The name of the account for image storage                        |
| AZURE_ACCOUNT_KEY                     | <azureaccountkey>    | The access key to account for image storage                      |
| AZURE_ACCOUNT                         | <azureaccount>       | The account for image storage                                    |
| AZURE_CONTAINER                       | <azurecontainer>     | The container name for image storage                             |
| JSONFILES_STORAGE_CONTAINER           | <azurecontainer>     | The container URI for the json files                             |
| SITEMAP_STORAGE_BLOB                  | <sitemap file name>  | Tells the app where the dynamic sitemap is stored                |
| AZURE_EMAIL_SERVICE_CONNECTION_STRING | <connectionstring>   | Connection string for Azure Email Service                        |
| AZURE_EMAIL_OUTGOING_EMAIL_ADDRESS    | <emailaddress>       | The e-mail address used for notifications                        |
| EMAIL_BACKEND                         | <emailbackend>       | Django email backend to use                                      |
| SORT_BY_SUBJECT_LIMIT                 | 5000                 | Used to determine how to display subjects                        |

# Getting Started

## Create and set up virtual environment (python 3.13)

```
$ python3.13 -m venv .venv
$ source .venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## Run Docker

```
$ docker-compose up
```

## Import database

Add a seed sql file to the root of the project and then run the following command:

```
cat <your-sql-file>.sql | docker exec -i wagtail-cms-db-1 psql -U docker -d django
```

## Open browser

Open a browser and navigate to http://localhost:8000/

# Other Stuff

## Adding Environment Variables

If you add environment variable to `docker-compose.yml` don't forget to also add it to `CMS/settings/base.py`

## Continuous Integration and Deployment Pipeline

The continuous integration and deployment pipeline for this project is implemented using Azure DevOps pipelines.

### Continuous Integration

The continuous integration pipeline for the project is defined in yml files in the root of the project, all starting with 'azure-pipelines'.

There are 3 pipelines defined in the project.

#### CI test
_Defined in 'azure-pipelines.yml'_

This pipeline should run on every push to Github from feature, bug and refactor branches. All this pipeline does is run the tests to regression check the new code.

#### Pre prod build
_Defined in 'pre-prod-azure-pipelines.yml'_

This pipeline should run on every push to Github from a release branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the pre-prod container registry.

#### Production build

_Defined in 'prod-azure-pipelines.yml'_

This pipeline should run on every push to Github on the master branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the prod container registry.

### Continuous Deployment

The continuous deployment pipeline is defined through the Azure DevOps pipeline UI.

There are 2 pipelines setup for the project.

#### Pre prod deploy

The pipeline runs when the a new container is pushed to the pre-prod container registry, it pulls the container on to the WebApp server and starts the container.

#### Production deploy

The pipeline runs when the a new container is pushed to the prod container registry, it pulls the container on to the WebApp server and starts the container.

## Deployment Details

### Deployment Files

The `deploy_files` folder contains files specifically used for deploying the application to production and pre-production environments.

- `Dockerfile`: This Dockerfile is used by the Azure DevOps pipelines to build the production-ready container image. It differs from the root `Dockerfile` by including production-specific configurations and dependencies.
- `docker-entrypoint.sh`: This script is the entry point for the deployed container. It handles running database migrations and starting the Gunicorn server with gevent workers.
- `docker-entrypoint-readonly.sh`: A variant of the entry point script for read-only environments.

### Requirements Files

The application uses two requirements files for Python packages:

1. `requirements.txt`: Contains the core dependencies required to run the Wagtail CMS application in all environments (development, test, and production).
2. `requirements-deploy.txt`: Contains additional dependencies required specifically for the deployed production environment, such as `gevent` for the Gunicorn worker class.

Both of these files are needed to build the production container image.

### Deployed Environment Requirements

In the deployed environment, the `deploy_files/docker-entrypoint.sh` file is critical as it ensures the database is migrated and the application server (Gunicorn) is correctly configured and started.

### Releases

Releases of the code are following the major/minor/patch pattern for release numbering.

##### Automated release process

- ensure there are no uncommitted changes in your local repository
- call the 'release' command in the bin directory, passing as a parameter either major/minor/patch.

#### Finishing a release

Once a release has been signed off and deployed to production, you need to:

- merge the release branch into master and to development.
- tag master with the release number at the point it was merged in.
- delete the release branch

## Performance and Reliability

### Widget Proxy Timeout

The `proxy_content` endpoint, used by the v2 widget and related API endpoints, includes a **10-second timeout** for external requests to the widget host (`WIDGET_HOST`). 

This change ensures that:
- **Server Resources:** Prevents application threads from hanging indefinitely if the external service is slow or unresponsive.
- **User Experience:** Provides a deterministic failure state (502 Bad Gateway) after 10 seconds, rather than an infinite loading state.
- **System Stability:** Protects the CMS from cascading failures during periods of external service degradation.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

See [LICENSE](LICENSE.md) for details.
