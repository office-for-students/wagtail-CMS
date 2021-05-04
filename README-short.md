# Introduction
**<font color="red">This is a _work-in-progress_ document....</font>**

The purpose of this document is to try an simplify the dev start-up process, in particular:
- introduce a virtual environment, of use when running tests outside of docker
- use a default `docker-compose.yml` file suitable for dev
- use a `docker-compose.non-dev.yml` file that does not contain Mongo for non-dev
- use docker `.env` files to store local environment variables (https://github.com/xni06/ofs-secrets.git)
- easier and quicker to read/digest

_Note that the original `docker-compose.yml.example` is maintained for CI but ideally `docker-compose.non-dev.yml` should be used in future._

# Virtual environment setup
```bash
## Create a virtual environment using Python 3.6.8 using https://virtualenv.pypa.io
virtualenv venv -p 3.6.8

# Activate the virtual environment 
source venv/bin/activate

# Verify Python version
python -V

# To deactivate
deactivate
```

# How to run tests
## Without Docker
### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Enable mocks for testing
export LOCAL=True

# To unset...
unset LOCAL
```

### Run tests
```bash
python manage.py test
```

## With Docker
### Run tests
```bash
# Grab hold of some pre-configured .env files
# see https://github.com/xni06/ofs-secrets.git

# Fire it up if not already running
docker-compose --env-file .env.test up 

docker container exec -it wagtail-cms_web_1 python manage.py test   
```

# How to configure the server
```bash
# Grab hold of some pre-configured .env files
# see https://github.com/xni06/ofs-secrets.git

# Fire it up 

# dev environment using default `docker-compose.yml` and `.env` files
docker-compose up 

# or using a specific `.env` file for remote Courses/Institutions
docker-compose --env-file .env.pre-prod up
docker-compose --env-file .env.prod up

# or using a specific `docker-compose` file for remote CMS
docker-compose -f docker-compose.non-dev.yml --env-file .env.pre-prod up
docker-compose -f docker-compose.non-dev.yml --env-file .env.prod up
```

# Databases
## Fixtures
Type         | Local DB    | Remote DB   | Name                                     
---          | ---         | ---         | ---
CMS          | PostgresSQL | PostgresSQL | `CMS/fixtures/postgres.json` 
Courses      | MongoDB     | CosmosDB    | `courses/fixtures/courses.json` 
Institutions | MongoDB     | CosmosDB    | `institutions/fixtures/institutions.json` 

## Load local databases with data from fixtures
```bash
# CMS
docker container exec -it wagtail-cms_web_1 python manage.py populate_cms

# Courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses

# Institutions
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions
```

## Optional - update fixture with data from remote database
```bash
# See https://github.com/xni06/ofs-secrets.git for the following environment variables 

# CMS
docker container exec -it wagtail-cms_web_1 python manage.py update_cms_fixture \
      --db_host $REMOTE_DB_HOST \
      --db_name $REMOTE_DB_NAME \
      --db_user $REMOTE_DB_USER \
      --db_password $REMOTE_DB_PASSWORD \
      --db_port $REMOTE_DB_PORT

# Courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses --update

# Institutions
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions --update
```
