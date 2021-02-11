import json
import requests
from math import ceil

from django.core.management.base import CommandError
import azure.cosmos.cosmos_client as cosmos_client

from core.command import CosmosCommand
from core.mongo import Mongo

from django.conf import settings


class Command(CosmosCommand):
    help = 'Copies Institutions from Cosmos DB to the local MongoDB ' + \
        '(and into the institutions/fixtures folder)'

    fixture_file      = None
    request_options   = {"enableCrossPartitionQuery": True}
    base_url          = 'dbs/discoveruni/colls/'
    mongo             = None
    version           = None
    num_institutions  = None

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fixture_file = \
            settings.BASE_DIR + '/institutions/fixtures/institutions.json'

        self.mongo = Mongo('institutions')
        self.mongo.collection_delete()

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        #database = self.client.get_database_client('d735a2c7-1a90-4b37-9b85-687226b2e1f9')
        #print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        version = self.get_latest_version_number()
        num_institutions = self.get_number_of_institutions(version)

        institutions_list = self.get_institutions(version)

        try:
            self.mongo.insert(institutions_list)
            self.success('Inserted institutions into MongoDB')
        except Exception:
            raise CommandError('Failed to insert institutions into MongoDB')

        with open(self.fixture_file, 'w') as outfile:
            json.dump(institutions_list, outfile, indent=4)
            self.success('Saved file to ' + self.fixture_file)


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
        self.success('Got number of institutions from CosmosDB (' + \
            str(number_of_institutions_int) + ')')
        return number_of_institutions_int


    def get_institutions(self, version):
        sql = 'SELECT * from c WHERE c.version = ' + str(version)

        qurey_result = None

        try:
            qurey_result = self.cosmos_client.QueryItems(
                self.base_url + 'institutions', sql,
                self.request_options
            )
        except Exception:
            raise CommandError('CosmosDB instututions query failed')

        try:
            list_result = list(qurey_result)
        except Exception:
            raise CommandError('Converting instututions into list failed (' + \
                str(query_result) + ')')

        self.success('Got institutions from CosmosDB')

        return list_result


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
