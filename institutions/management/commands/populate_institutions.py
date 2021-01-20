import requests
from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client

from django.conf import settings


class Command(BaseCommand):
    help = 'Copies Institutions from the Cosmos DB in Azure'
    version_url = 'dbs/discoveruni/colls/datasets'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.cosmos_client = cosmos_client.CosmosClient(
            settings.DATASETAPIHOST,
            {'masterKey': settings.DATASETAPIKEY}
        )

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        #database = self.client.get_database_client('d735a2c7-1a90-4b37-9b85-687226b2e1f9')
        #print('Database with id \'{0}\' was found, it\'s link is {1}'.format(id, database.database_link))
        print(self.get_latest_version_number())
        self.stdout.write(self.style.SUCCESS('Successfully closed poll Dave'))

    def get_latest_version_number(self):
        '''query = "SELECT VALUE MAX(c.version) from c "
        options = {"enableCrossPartitionQuery": True}
        max_version_number_list = list(
            self.cosmos_client.QueryItems(self.version_url, query, options)
        )
        return max_version_number_list[0]'''

        return requests.get(
            url=settings.DATASETAPIHOST + '/institutions/' + str(10000047),
            headers={'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY}
        )
