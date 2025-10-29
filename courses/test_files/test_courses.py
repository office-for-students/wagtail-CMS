from django.test.testcases import TestCase

from django.test import tag


@tag('github')
class CoursesTestCase(TestCase):

    def test_front_page(self):

        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
