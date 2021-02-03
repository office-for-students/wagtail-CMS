import requests
from math import ceil

from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client

from pprint import pprint

from django.conf import settings


class Command(BaseCommand):
    help = 'Copies Institutions from the Cosmos DB in Azure to the institutions/fixtures folder as a json'

    request_options  = {"enableCrossPartitionQuery": True}
    base_url         = 'dbs/discoveruni/colls/'
    batch_size       = 100
    version          = None
    num_institutions = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        if not settings.AZURECOSMOSDBURI or \
           not settings.AZURECOSMOSDBKEY:
            raise CommandError('AZURECOSMOSDBURI and AZURECOSMOSDBKEY in ' + \
                'docker-compose.yml need to point to the CosmosDB')

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
            print('batch '+str(batch)+': start: '+str(batch*self.batch_size)+', end: '+str((batch*self.batch_size)+self.batch_size))

        #institutions_json = self.get_all_institutions()
        #pprint(institutions_json)

        self.stdout.write(self.style.SUCCESS('Success!'))

    def get_number_of_institutions(self, version):
        number_of_institutions = self.base_query(
            'institutions',
            'SELECT VALUE COUNT(1) from c WHERE c.version = ' + str(version)
        )
        try:
            return int(number_of_institutions[0])
        except Exception:
            raise CommandError('number of institutions returned is not an ' + \
                'integer in a list (' + str(number_of_institutions) + ')')

    def get_institutions(self, position):
        sql = 'SELECT * from c WHERE c.version = ' + str(self.version) + \
              ' OFFSET ' + str(position) + ' LIMIT ' + str(self.batch_size),
        return list(
            self.cosmos_client.QueryItems(
                self.base_url + 'institutions', sql,
                self.request_options
            )
        )

    def get_latest_version_number(self):
        version = self.base_query('datasets', 'SELECT VALUE MAX(c.version) from c')
        try:
            return int(version[0])
        except Exception:
            raise CommandError('version returned is not an integer in a list (' + \
                str(version) + ')')

    def base_query(self, table, query):
        return list(
            self.cosmos_client.QueryItems(
                self.base_url + table,
                query,
                self.request_options
            )
        )
