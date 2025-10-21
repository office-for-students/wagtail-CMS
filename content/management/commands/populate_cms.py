import os
from pathlib import Path

from core.command import SimpleCommand
from django.contrib.contenttypes.models import ContentType
from django.core import management
from django.core.management.base import CommandError
from wagtail.core.models import Page


class Command(SimpleCommand):
    help = 'Populates Postgres using the data in the CMS fixture folder'

    db_host                 = 'db'
    db_name                 = 'django'
    db_user                 = 'docker'
    db_password             = 'docker'
    json_file               = 'CMS/fixtures/postgres.json'
    message_count           = None
    total_success_messages  = 6


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.environ.get('DBHOST') != self.db_host or \
           os.environ.get('DBNAME') != self.db_name or \
           os.environ.get('DBUSER') != self.db_user or \
           os.environ.get('DBPASSWORD') != self.db_password:
            raise CommandError('DBHOST, DBNAME, DBUSER & DBPASSWORD should ' + \
                'be pointing to the local PostgresSQL in docker')

        self.message_count = 1
        self.json_file = str(Path(self.json_file))


    def handle(self, *args, **options):

        management.call_command(
            'flush_db',
            '--allow-cascade',
            '--no-input'
        )
        self.success('Flushed database')

        management.call_command('migrate')
        self.success('Migrated database')

        Page.objects.all().delete()
        self.success('Deleted all Page rows')

        ContentType.objects.all().delete()
        self.success('Deleted all ContentType rows')

        management.call_command('loaddata', self.json_file)
        self.success('Loaded file (' + self.json_file + ')')

        self.success('Population complete')


    def success(self, message):
        super().success('[' + str(self.message_count) + ' of ' + \
            str(self.total_success_messages) + '] ' + message)
        self.message_count += 1
