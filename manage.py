#!/usr/bin/env python
import os
import sys
import yaml


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMS.settings.dev")

    from django.core.management import execute_from_command_line


    # Environment variables below added for out-of-container debugging.
    os.environ["OUT_OF_CONTAINER_DEBUG"] = "False"
    if os.environ["OUT_OF_CONTAINER_DEBUG"] == "True":
        os.environ["ENVIRONMENT"] = "dev" # This env var can take the values 'dev' or 'pre-prod'.
        with open(r'docker-compose.{}.yml'.format(os.environ["ENVIRONMENT"])) as file:
            dataMap = yaml.safe_load(file)
            env = dataMap['services']['web']['environment']

            # Postgres:
            os.environ["DBHOST"] = env['DBHOST']
            os.environ["DBNAME"] = env['DBNAME']
            os.environ["DBPASSWORD"] = env['DBPASSWORD']
            os.environ["DBPORT"] = env['DBPORT']
            os.environ["DBUSER"] = env['DBUSER']

            # Azure Storage settings:
            os.environ["AZURE_ACCOUNT_KEY"] = env['AZURE_ACCOUNT_KEY']
            os.environ["AZURE_ACCOUNT_NAME"] = env['AZURE_ACCOUNT_NAME']
            os.environ["AZURE_CONTAINER"] = env['AZURE_CONTAINER']

            # Cosmos DB settings (via API Management service):
            os.environ["DATASETAPIHOST"] = env['DATASETAPIHOST']
            os.environ["DATASETAPIKEY"] = env['DATASETAPIKEY']

            os.environ["FEEDBACK_API_HOST"] = env['FEEDBACK_API_HOST']
            os.environ["JSONFILES_STORAGE_CONTAINER"] = env['JSONFILES_STORAGE_CONTAINER']
            os.environ["READ_ONLY"] = env['READ_ONLY']
            os.environ["SEARCHAPIHOST"] = env['SEARCHAPIHOST']

            os.environ["SECRET_KEY"] = env['SECRET_KEY']
            os.environ["SENDGRID_API_KEY"] = env['SENDGRID_API_KEY']
            os.environ["SENDGRID_FROM_EMAIL"] = env['SENDGRID_FROM_EMAIL']
            os.environ["WIDGETAPIHOST"] = env['WIDGETAPIHOST']
            os.environ["WIDGETAPIKEY"] = env['WIDGETAPIKEY']
    # Environment variables above added for debugging.


    execute_from_command_line(sys.argv)
