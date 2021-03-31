from django.test import TestCase, Client

from wagtail.core.models import Page


class PagesTest(TestCase):

    client = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()

    def test_wagtail_pages(self):
        for page in Page.objects.all():
            if page.url:
                response = self.client.get(page.url)
                try:
                    self.assertEqual(200, response.status_code)
                except AssertionError:
                    raise AssertionError(
                        str(page.title)+'('+str(page.url)+') does not exist'
                    )
