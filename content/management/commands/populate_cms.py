import os
import json
import requests
import subprocess
from math import ceil
from pathlib import Path

from django.core import management
import azure.cosmos.cosmos_client as cosmos_client
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from wagtail.core.models import Page
from core.command import SimpleCommand
from core.mongo import Mongo

from django.conf import settings


class Command(SimpleCommand):
    help = 'Copies the PostgreSQL data into your local environment for ' + \
        'development and testing'

    db_host                 = 'db'
    db_name                 = 'django'
    db_user                 = 'docker'
    db_password             = 'docker'
    json_file               = 'postgres.json'
    message_count           = None
    total_success_messages  = 9


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.environ.get('DBHOST') != self.db_host or \
           os.environ.get('DBNAME') != self.db_name or \
           os.environ.get('DBUSER') != self.db_user or \
           os.environ.get('DBPASSWORD') != self.db_password:
            raise CommandError('DBHOST, DBNAME, DBUSER & DBPASSWORD should ' + \
                'be pointing to the local PostgresSQL in docker')

        self.message_count = 1


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

        self.info('Copying database (>5mins) (remote)')
        json_data = management.call_command(
            'dumpdata',
            '--database',
            'remote',
            '--natural-foreign',
            '--output',
            self.json_file
        )
        self.success('Saved file (' + self.json_file + ')')

        management.call_command(
            'flush_db',
            '--allow-cascade',
            '--no-input'
        )
        self.success('Flushed database (local)')

        management.call_command('migrate')
        self.success('Migrated database (local)')

        Page.objects.all().delete()
        self.success('Deleted all Page rows (local)')

        ContentType.objects.all().delete()
        self.success('Deleted all ContentType rows (local)')

        self.info('Loading file (>1min)(' + self.json_file + ')')
        management.call_command('loaddata', self.json_file)
        self.success('Loaded file (' + self.json_file + ')')

        base_path = Path(settings.BASE_DIR + '/')
        full_file_name = base_path / self.json_file

        if os.path.isfile(full_file_name):
            os.remove(full_file_name)
            self.success('Removed file (' + self.json_file + ')')

        self.success('Population complete')


    def success(self, message):
        super().success('[' + str(self.message_count) + ' of ' + \
            str(self.total_success_messages) + '] ' + message)
        self.message_count += 1
