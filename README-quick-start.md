# How to install CMS locally from scratch
This document cherry picks some commands that can already be found in [README-short.md](https://github.com/office-for-students/wagtail-CMS/blob/develop/README-short.md)

Notes:
1. Python 3.6.8 is referenced in [Confluence](https://mobilisecloud.atlassian.net/wiki/spaces/OFS/pages/236912643/Managing+multiple+Python+versions) and [Docker](https://github.com/office-for-students/wagtail-CMS/blob/master/Dockerfile). If you don't already have 3.6 installed, a later version should work too.


```
# First, delete any existing Docker containers/images using CLI or UI, then...

# Create a fresh directory to work in 
mkdir -p ~/temp/demo-wagtail-fresh-install 
cd ~/temp/demo-wagtail-fresh-install

# Clone the relevant directories
git clone https://github.com/office-for-students/wagtail-CMS
git clone https://gitlab.mgmt.mobilise.cloud/mobilise-dev/ofs-secrets

# Copy the secrets
cp ofs-secrets/wagtail-CMS/.env* wagtail-CMS/.

cd wagtail-CMS

# Create a virtual environment using Python 3.6.8 using https://virtualenv.pypa.io
virtualenv venv -p 3.6.8

# Activate the virtual environment 
source venv/bin/activate

# Verify Python version
python -V

# Install dependencies
pip install -r requirements.txt

# Enable mocks for testing
export LOCAL=True

# Run tests
python manage.py test

# Unset mocks
unset LOCAL

# Start the application
docker-compose up 

# Open new Terminal to run following commands from, then...
source venv/bin/activate

# Migrate database tables
docker container exec -it wagtail-cms_web_1 python manage.py migrate

# Load local databases with data from fixtures

# CMS
docker container exec -it wagtail-cms_web_1 python manage.py populate_cms

# Courses
docker container exec -it wagtail-cms_web_1 python manage.py populate_courses

# Institutions
docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions

# Navigate to application
open http://0.0.0.0:8000/

# To point to the pre-prod remote database instead of local, cut'n paste contents of .env.pre-prod into .env and restart the application

```
