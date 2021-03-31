from django.test import tag

from core.tests import BaseTestCase
from courses.models import CourseManagePage


@tag('github')
class CoursesTestCase(BaseTestCase):

    def test_front_page(self):

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
