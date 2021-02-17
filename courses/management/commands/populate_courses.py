import json
import requests
from pathlib import Path

from django.core.management.base import CommandError
import azure.cosmos.cosmos_client as cosmos_client

from core.command import CosmosCommand
from core.mongo import Mongo

from django.conf import settings


class Command(CosmosCommand):
    help = 'Copies Courses from Cosmos DB to the local MongoDB ' + \
        '(and into the courses/fixtures folder)'

    fixture_file           = 'courses/fixtures/courses.json'
    full_fixture_filename  = None


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.full_fixture_filename = str(
            Path(settings.BASE_DIR + '/' + self.fixture_file)
        )


    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Gets the latest data from CosmosDB and stores it in ' + \
                self.fixture_file,
        )


    def handle(self, *args, **options):

        if options['update']:
            version = self.get_latest_version_number()
            courses_list = self.get_courses(version)

            with open(self.fixture_file, 'w') as outfile:
                json.dump(courses_list, outfile, indent=4)
                self.success('Saved file to ' + self.fixture_file)

        else:
            with open(self.fixture_file, 'r') as file:
                self.info('Getting courses from ' + self.fixture_file)
                contents = json.load(file)
                self.success('Retrived courses from ' + self.fixture_file)

                self.mongo = Mongo('courses')
                self.mongo.collection_delete()

                try:
                    self.mongo.insert(contents)
                    self.success('Inserted courses into MongoDB')
                except Exception as e:
                    message = e.message if hasattr(e, 'message') else \
                        'Failed to insert institutions into MongoDB'
                    raise CommandError(message)


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
