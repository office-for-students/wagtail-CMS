import logging

from django.test import Client
from django.test import TestCase
from django.test import tag

from CMS.enums import enums
from CMS.test.factories import PageFactory
from CMS.test.utils import UniSimpleTestCase
from core.utils import get_page_for_language
from coursesearch.models import CourseFinderChooseCountry


logger = logging.getLogger(__name__)
logging.basicConfig(level=9999) # suppress logs during unit tests

@tag('azure')
class CoreUtilsTests(UniSimpleTestCase):

    def test_get_page_for_language_returns_no_page_for_welsh_if_no_english_exists(self):
        pages = CourseFinderChooseCountry.objects.all()
        self.assertEqual(len(pages), 0)

        found_page = get_page_for_language(enums.languages.WELSH, CourseFinderChooseCountry.objects.all())
        self.assertIsNone(found_page)


@tag('azure')
class BaseTestCase(TestCase):
    institution_id  = 10005343

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()
