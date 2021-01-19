import requests
from django.core.management.base import BaseCommand, CommandError
import azure.cosmos.cosmos_client as cosmos_client

from django.conf import settings


class Command(BaseCommand):
    help = 'Copies Institutions from the Cosmos DB in Azure'
    version_url = 'dbs/discoveruni/colls/datasets'

    def __init__(self):
        self.cosmos_client = cosmos_client.CosmosClient(
            url_connection=settings.DATASETAPIHOST,
            auth={'master_key': settings.DATASETAPIKEY}
        )

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_ids']:
        self.get_latest_version_number()
        self.stdout.write(self.style.SUCCESS('Successfully closed poll Dave'))

    def get_latest_version_number(self):
        query = "SELECT VALUE MAX(c.version) from c "
        options = {"enableCrossPartitionQuery": True}
        max_version_number_list = list(
            self.cosmos_client.QueryItems(self.version_url, query, options)
        )
        return max_version_number_list[0]
