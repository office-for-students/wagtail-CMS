import requests
from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client

from pprint import pprint

from django.conf import settings


class Command(BaseCommand):
    help = 'Copies Institutions from the Cosmos DB in Azure to the projects root folder as a json'
    base_url = 'dbs/discoveruni/colls/'
    version = None

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.cosmos_client = cosmos_client.CosmosClient(
            settings.COSMOSDBHOST,
            {'masterKey': settings.COSMOSDBKEY}
        )
        version = self.get_latest_version_number()

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        #database = self.client.get_database_client('d735a2c7-1a90-4b37-9b85-687226b2e1f9')
        #print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        pprint(self.get_all_institutions())
        self.stdout.write(self.style.SUCCESS('Successfully closed poll Dave'))

    def get_all_institutions(self):
        query = "SELECT * from c OFFSET 0 LIMIT 100"
        options = {"enableCrossPartitionQuery": True}
        institutions_json = list(
            self.cosmos_client.QueryItems(
                self.base_url + 'institutions',
                query,
                options
            )
        )
        return institutions_json

    def get_latest_version_number(self):
        query = "SELECT VALUE MAX(c.version) from c "
        options = {"enableCrossPartitionQuery": True}
        max_version_number_list = list(
            self.cosmos_client.QueryItems(
                self.base_url + 'datasets',
                query,
                options
            )
        )
        return int(max_version_number_list[0])
