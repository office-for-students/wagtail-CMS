import logging

from CMS.enums import enums
from CMS.test.factories import PageFactory
from CMS.test.utils import UniSimpleTestCase
from core.utils import get_page_for_language
from coursefinder.models import CourseFinderChooseCountry
from django.conf import settings
from django.core import management
from django.test import Client
from django.test import TestCase
from django.test import tag
from site_search.models import SearchLandingPage

logger = logging.getLogger(__name__)
logging.basicConfig(level=9999) # suppress logs during unit tests

@tag('azure')
class CoreUtilsTests(UniSimpleTestCase):

    def test_get_page_for_language_returns_english_page_if_it_exists(self):
        created_page = PageFactory.create_search_landing_page('English course finder')
        self.assertIsNotNone(created_page)

        found_page = get_page_for_language(enums.languages.ENGLISH, SearchLandingPage.objects.all())
        self.assertIsNotNone(found_page)
        self.assertEqual(created_page.id, found_page.id)

    def test_get_page_for_language_returns_english_page_if_multiple_english_pages_exist(self):
        created_page = PageFactory.create_search_landing_page('English course finder')
        second_created_page = PageFactory.create_search_landing_page('English course finder 2')
        self.assertIsNotNone(created_page)
        self.assertIsNotNone(second_created_page)

        found_page = get_page_for_language(enums.languages.ENGLISH, SearchLandingPage.objects.all())
        self.assertIsNotNone(found_page)
        self.assertEqual(created_page.id, found_page.id)

    def test_get_page_for_language_returns_no_page_for_english_if_no_english_exists(self):
        pages = SearchLandingPage.objects.all()
        self.assertEqual(len(pages), 0)

        found_page = get_page_for_language(enums.languages.ENGLISH, SearchLandingPage.objects.all())
        self.assertIsNone(found_page)

    def test_get_page_for_language_returns_welsh_page_if_it_exists(self):
        welsh_root = PageFactory.create_search_landing_page('cy')
        created_page = PageFactory.create_country_finder_page('Welsh course finder', parent_page=welsh_root)
        self.assertIsNotNone(created_page)
        self.assertIsTrue('cy' in created_page.url)

        found_page = get_page_for_language(enums.languages.WELSH, CourseFinderChooseCountry.objects.all())
        self.assertIsNotNone(found_page)
        self.assertEqual(created_page.id, found_page.id)

    def test_get_page_for_language_returns_welsh_page_if_multiple_welsh_pages_exist(self):
        welsh_root = PageFactory.create_search_landing_page('cy')
        created_page = PageFactory.create_country_finder_page('Welsh course finder', parent_page=welsh_root)
        second_created_page = PageFactory.create_country_finder_page('Welsh course finder 2', parent_page=welsh_root)
        self.assertIsNotNone(created_page)
        self.assertIsNotNone(second_created_page)
        self.assertIsTrue('cy' in created_page.url)

        found_page = get_page_for_language(enums.languages.WELSH, CourseFinderChooseCountry.objects.all())
        self.assertIsNotNone(found_page)
        self.assertEqual(created_page.id, found_page.id)

    def test_get_page_for_language_returns_english_page_for_welsh_if_no_welsh_page_exists(self):
        created_page = PageFactory.create_country_finder_page('English course finder')
        self.assertIsNotNone(created_page)
        self.assertIsTrue('cy' not in created_page.url)
        pages = CourseFinderChooseCountry.objects.all()
        self.assertEqual(len(pages), 1)

        found_page = get_page_for_language(enums.languages.WELSH, CourseFinderChooseCountry.objects.all())
        self.assertIsNotNone(found_page)
        self.assertEqual(created_page.id, found_page.id)

    def test_get_page_for_language_returns_no_page_for_welsh_if_no_english_exists(self):
        pages = CourseFinderChooseCountry.objects.all()
        self.assertEqual(len(pages), 0)

        found_page = get_page_for_language(enums.languages.WELSH, CourseFinderChooseCountry.objects.all())
        self.assertIsNone(found_page)


@tag('azure')
class CoreModelsTests(UniSimpleTestCase):

    def test_get_language_returns_en_for_english_page(self):
        english_root = PageFactory.create_search_landing_page('home')
        created_page = PageFactory.create_country_finder_page('English course finder', parent_page=english_root)
        self.assertIsNotNone(created_page)

        self.assertEqual(created_page.get_language(), enums.languages.ENGLISH)

    def test_get_page_for_language_returns_welsh_page_if_it_exists(self):
        welsh_root = PageFactory.create_search_landing_page('cy')
        created_page = PageFactory.create_country_finder_page('Welsh course finder', parent_page=welsh_root)
        self.assertIsNotNone(created_page)
        self.assertIsTrue('cy' in created_page.url)

        self.assertEqual(created_page.get_language(), enums.languages.WELSH)


@tag('azure')
class BaseTestCase(TestCase):
    institution_id  = 10005343

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()
