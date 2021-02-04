import requests
from math import ceil

from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client
from pymongo import MongoClient

from pprint import pprint

from django.conf import settings


class Mongo():
    client      = None
    database    = None
    collection  = None

    def __init__(self):
        self.client = MongoClient(
            settings.MONGODB_HOST,
            username = settings.MONGODB_USERNAME,
            password = settings.MONGODB_PASSWORD
        )
        self.database = self.client.database
        self.collection = self.database.collection
        #self.auth()

    def auth(self):
        databases = self.client.list_database_names()
        if 'database' in databases:
            self.database.auth(
                settings.MONGODB_USERNAME,
                settings.MONGODB_PASSWORD
            )

    def database_delete(self):
        databases = self.client.list_database_names()
        if 'database' in databases:
          self.database.remove()

    def collection_delete(self):
        collections = mself.client.list_collection_names()
        if 'collection' in collections:
            self.collection.remove()

    def insert(self, json):
        self.collection.insert(json)


class Command(BaseCommand):
    help = 'Copies Institutions from the Cosmos DB in Azure to the institutions/fixtures folder as a json'

    request_options   = {"enableCrossPartitionQuery": True}
    base_url          = 'dbs/discoveruni/colls/'
    mongo_client      = None
    mongo_database    = None
    mongo_collection  = None
    batch_size        = 100
    version           = None
    num_institutions  = None

    def __init__(self, *args, **kwargs):

        super(Command, self).__init__(*args, **kwargs)

        if not settings.MONGODB_HOST or \
           not settings.MONGODB_USERNAME or \
           not settings.MONGODB_PASSWORD:
            raise CommandError('MONGODB_HOST, MONGODB_USERNAME and  ' +
                'MONGODB_PASSWORD should be in the docker-compose.yml')

        if not settings.AZURECOSMOSDBURI or \
           not settings.AZURECOSMOSDBKEY:
            raise CommandError('AZURECOSMOSDBURI and AZURECOSMOSDBKEY in ' + \
                'docker-compose.yml need to point to the CosmosDB')

        self.mongo = Mongo()
        self.collection_delete()
        self.database_delete()

        self.cosmos_client = cosmos_client.CosmosClient(
            settings.AZURECOSMOSDBURI,
            {'masterKey': settings.AZURECOSMOSDBKEY}
        )

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        #database = self.client.get_database_client('d735a2c7-1a90-4b37-9b85-687226b2e1f9')
        #print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        version = self.get_latest_version_number()
        num_institutions = self.get_number_of_institutions(version)

        for batch in range(0, ceil(num_institutions / self.batch_size)):
            institutions_json = self.get_institutions(batch*self.batch_size)
            self.mongo.insert(institutions_json)
            import sys
            sys.exit()

        #institutions_json = self.get_all_institutions()
        #pprint(institutions_json)

    def save_institutions_to_mongo_db(self, institutions_json):
        self.mongo_collection.insert(institutions_json)

    def get_number_of_institutions(self, version):
        number_of_institutions = self.base_query(
            'institutions',
            'SELECT VALUE COUNT(1) from c WHERE c.version = ' + str(version)
        )
        try:
            number_of_institutions_int = int(number_of_institutions[0])
        except Exception:
            raise CommandError('number of institutions returned is not an ' + \
                'integer in a list (' + str(number_of_institutions) + ')')
        self.success('SUCCESS: Got number of institutions from CosmosDB')
        return number_of_institutions_int

    def get_institutions(self, position):
        sql = 'SELECT * from c WHERE c.version = ' + str(self.version) + \
              ' OFFSET ' + str(position) + ' LIMIT ' + str(self.batch_size),
        try:
            institutions_json = list(
                self.cosmos_client.QueryItems(
                    self.base_url + 'institutions', sql,
                    self.request_options
                )
            )
        except Exception:
            raise CommandError('CosmosDB instututions query failed (' + \
                str(institutions_json) + ')')
        self.success('SUCCESS: Got ' + str(self.batch_size) + ' institutions from CosmosDB')
        return institutions_json

    def get_latest_version_number(self):
        version = self.base_query('datasets', 'SELECT VALUE MAX(c.version) from c')
        try:
            version_int = int(version[0])
        except Exception:
            raise CommandError('version returned is not an integer in a list (' + \
                str(version) + ')')
        self.success('SUCCESS: Got latest version number from CosmosDB')
        return version_int

    def base_query(self, table, query):
        return list(
            self.cosmos_client.QueryItems(
                self.base_url + table,
                query,
                self.request_options
            )
        )

    def success(self, message):
        self.stdout.write(self.style.SUCCESS(message))
