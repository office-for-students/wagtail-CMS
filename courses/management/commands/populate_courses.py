import json
import requests
from math import ceil

from django.core.management.base import CommandError
import azure.cosmos.cosmos_client as cosmos_client

from core.command import RootCommand
from core.mongo import Mongo

from django.conf import settings


class Command(RootCommand):
    help = 'Copies Courses from Cosmos DB to the local MongoDB ' + \
        '(and into the courses/fixtures folder)'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fixture_file = \
            settings.BASE_DIR + '/courses/fixtures/courses.json'

        self.mongo = Mongo('courses')
        self.mongo.collection_delete()


    def handle(self, *args, **options):
        version = self.get_latest_version_number()

        courses_list = self.get_courses(version)

        try:
            self.mongo.insert(courses_list)
            self.success('Inserted courses into MongoDB')
        except Exception as e:
            raise CommandError('Failed to insert courses into MongoDB (' + \
                str(e) + ')')

        with open(self.fixture_file, 'w') as outfile:
            json.dump(courses_list, outfile, indent=4)
            self.success('Saved file to ' + self.fixture_file)


    def get_courses(self, version):
        if not settings.TEST_COURSES:
            raise CommandError('No test corses found in TEST_COURSES')

        courses = []
        for course_id in settings.TEST_COURSES.split(','):
            course_data = self.get_course(course_id, version)
            if course_data:
                self.success('Got course (' + str(course_id) + ') from CosmosDB')
                courses.append(course_data[0])
            else:
                self.error('Could not get data for course (' + \
                    str(course_id) + ')')

        return courses


    def get_course(self, course_id, version):
        sql = 'SELECT * from c WHERE c.version = ' + str(version) + ' ' + \
            'AND c.course_id = "' + str(course_id) + '"'

        qurey_result = None

        try:
            qurey_result = self.cosmos_client.QueryItems(
                self.base_url + 'courses', sql,
                self.request_options
            )
        except Exception:
            raise CommandError('CosmosDB course query failed')

        try:
            list_result = list(qurey_result)
        except Exception:
            raise CommandError('Converting course into list failed (' + \
                str(query_result) + ')')

        return list_result
