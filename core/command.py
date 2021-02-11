import json
import requests
from math import ceil

from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client

from django.conf import settings
from core.mongo import Mongo


class SimpleCommand(BaseCommand):
    help = 'IMPORTANT: Replace the help text in your command!!!'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def info(self, message):
        self.stdout.write(self.style.WARNING('INFO:    ' + message))


    def success(self, message):
        self.stdout.write(self.style.SUCCESS('SUCCESS: ' + message))


    def error(self, message):
        self.stdout.write(self.style.ERROR('ERROR:   ' + message))


class CosmosCommand(SimpleCommand):
    help = 'IMPORTANT: Replace the help text in your command!!!'

    cosmos_client     = None
    fixture_file      = None
    request_options   = {"enableCrossPartitionQuery": True}
    base_url          = 'dbs/discoveruni/colls/'
    mongo             = None
    version           = None

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if not settings.AZURECOSMOSDBURI or \
           not settings.AZURECOSMOSDBKEY:
            raise CommandError('AZURECOSMOSDBURI and AZURECOSMOSDBKEY in ' + \
                'docker-compose.yml need to point to the CosmosDB')

        self.cosmos_client = cosmos_client.CosmosClient(
            settings.AZURECOSMOSDBURI,
            {'masterKey': settings.AZURECOSMOSDBKEY}
        )


    def get_latest_version_number(self):
        version = self.base_query('datasets', 'SELECT VALUE MAX(c.version) from c')
        try:
            version_int = int(version[0])
        except Exception:
            raise CommandError('version returned is not an integer in a list (' + \
                str(version) + ')')
        self.success('Got latest version number from CosmosDB (' + \
            str(version_int) + ')')
        return version_int


    def base_query(self, table, query):
        return list(
            self.cosmos_client.QueryItems(
                self.base_url + table,
                query,
                self.request_options
            )
        )
