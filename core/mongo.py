from pymongo import MongoClient

from django.conf import settings


class Mongo():
    client           = None
    database         = None
    collection_name  = None
    collection       = None

    def __init__(self, collection_name):

        if not settings.MONGODB_HOST or \
           not settings.MONGODB_USERNAME or \
           not settings.MONGODB_PASSWORD:
            raise CommandError('MONGODB_HOST, MONGODB_USERNAME and  ' +
                'MONGODB_PASSWORD should be in the docker-compose.yml')

        self.collection_name = collection_name
        self.client = MongoClient(
            settings.MONGODB_HOST,
            username = settings.MONGODB_USERNAME,
            password = settings.MONGODB_PASSWORD
        )
        self.database = self.client.database
        self.collection = self.database[self.collection_name]

    def collection_delete(self):
        collections = self.database.list_collection_names()
        if self.collection_name in collections:
            self.database.drop_collection(self.collection_name)

    def insert(self, json):
        self.collection.insert(json)

    def get_one(self, key, value):
        return self.collection.find_one({key: value})
