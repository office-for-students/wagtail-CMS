from django.test import tag
from django.test.testcases import TestCase


@tag('github')
class HomePageTests(TestCase):

    def test_front_page(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)