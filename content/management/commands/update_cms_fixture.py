import re
import os
import json
import requests
import subprocess
from math import ceil
from pathlib import Path

from django.core import management
import azure.cosmos.cosmos_client as cosmos_client
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from wagtail.core.models import Page
from core.command import SimpleCommand
from core.mongo import Mongo

from django.conf import settings


class Command(SimpleCommand):
    help = 'Updated the Postgres fixture data'

    db_host                 = 'db'
    db_name                 = 'django'
    db_user                 = 'docker'
    db_password             = 'docker'
    json_file               = 'CMS/fixtures/postgres.json'
    full_file_name          = None
    default_password        = 'password'
    password                = None
    message_count           = None
    total_success_messages  = 2


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.environ.get('DBHOST') != self.db_host or \
           os.environ.get('DBNAME') != self.db_name or \
           os.environ.get('DBUSER') != self.db_user or \
           os.environ.get('DBPASSWORD') != self.db_password:
            raise CommandError('DBHOST, DBNAME, DBUSER & DBPASSWORD should ' + \
                'be pointing to the local PostgresSQL in docker')

        base_path = Path(settings.BASE_DIR + '/')
        self.full_file_name = base_path / self.json_file

        self.message_count = 1
        self.password      = make_password(self.default_password)


    def add_arguments(self, parser):
        parser.add_argument('--db_host',
            help='The URL for the remote PostgreSQL instance')
        parser.add_argument('--db_name', help='The database table name')
        parser.add_argument('--db_user', help='The user name used to login ' + \
            'to the remote PostgreSQL instance')
        parser.add_argument('--db_password', help='The password used to ' + \
            'login to the remote PostgreSQL instance')
        parser.add_argument('--db_port', help='The port used to connect ' + \
            'to the remote PostgreSQL instance')


    def handle(self, *args, **options):
        settings.DATABASES['remote'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': options['db_host'],
            'NAME': options['db_name'],
            'USER': options['db_user'],
            'PASSWORD': options['db_password'],
            'PORT': str(options['db_port']),
        }

        self.info('Copying database (<2mins) (remote)')

        json_data = management.call_command(
            'dumpdata',
            '--database',
            'remote',
            '--natural-foreign',
            '--exclude',
            'axes.accesslog',
            '--exclude',
            'axes.accessattempt',
            '--exclude',
            'sessions',
            '--exclude',
            'wagtailcore.pagerevision',
            '--indent',
            '4',
            '--output',
            self.full_file_name
        )

        self.success('Updating file (' + str(self.full_file_name) + ')')

        current_user_index = 0
        new_usernames = {}
        with open(self.full_file_name, '+r') as file:
            data = json.load(file)
            for index, item in enumerate(data):
                # (source: https://www.accordbox.com/blog/how-export-restore-wagtail-site/)
                if data[index]['model'] == 'wagtailcore.page':
                    data[index]['fields']['latest_revision_created_at'] = None
                    data[index]['fields']['live_revision'] = None
                # change the user creds so they can't be found in the repo
                if data[index]['model'] == 'auth.user':
                    user = 'user_' + str(current_user_index)
                    old_username = data[index]['fields']['username']
                    new_usernames[old_username]          = user
                    data[index]['fields']['password']    = self.password
                    data[index]['fields']['username']    = user
                    data[index]['fields']['first_name']  = user + ' first name'
                    data[index]['fields']['last_name']   = user + ' last name'
                    data[index]['fields']['email']       = user + '@' + user + '.com'
                    current_user_index += 1

            # where users are used else where in the json they need to be replaced
            # by the new users as well
            for index, item in enumerate(data):
                if data[index]['model'] == 'wagtailcore.page' and \
                   data[index]['fields']['owner']:
                    old_username = data[index]['fields']['owner'][0]
                    data[index]['fields']['owner'][0] = new_usernames[old_username]
                if data[index]['model'] == 'wagtaildocs.document' and \
                   data[index]['fields']['uploaded_by_user']:
                    old_username = data[index]['fields']['uploaded_by_user'][0]
                    data[index]['fields']['uploaded_by_user'][0] = new_usernames[old_username]
                if data[index]['model'] == 'wagtailusers.userprofile' and \
                   data[index]['fields']['user']:
                    old_username = data[index]['fields']['user'][0]
                    data[index]['fields']['user'][0] = new_usernames[old_username]

            file.seek(0)
            file.write(json.dumps(data, indent=4))
            file.truncate()
            file.close()

        with open(self.full_file_name, '+r') as file:
            contents = file.read()
            contents = re.sub('[\-\w]+\.azurewebsites\.net', 'localhost', contents)
            contents = re.sub(
                '\%7C[\.\w]+\%40officeforstudents\.org\.uk',
                '%7Ctest@test.com',
                contents
            )
            file.seek(0)
            file.write(contents)
            file.truncate()
            file.close()

        self.success('Updated complete')


    def success(self, message):
        super().success('[' + str(self.message_count) + ' of ' + \
            str(self.total_success_messages) + '] ' + message)
        self.message_count += 1
