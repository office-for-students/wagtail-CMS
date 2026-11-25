import importlib.util
import sys
from pathlib import Path
from unittest.mock import (
    Mock,
    patch,
)

from django.test import (
    override_settings,
    RequestFactory,
    SimpleTestCase,
    tag,
)
from django.urls import resolve

from CMS import (
    translations,
    urls as cms_urls,
)
from CMS.context_processors import nav_context_processor
from CMS.test.utils import UniSimpleTestCase
from CMS.translations.translations import cleanup_key
from core import views as core_views
from courses import views as course_views
from courses.views import translate as translate_views
from coursesearch import views as coursesearch_views
from institutions import views as institution_views
from v2_widget import views as widget_views


@tag('azure')
class MedexTestUtilsTests(UniSimpleTestCase):

    def test_uni_simple_test_case_assert_is_true_returns_true_when_passed_true(self):
        self.assertIsTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_false(self):
        try:
            self.assertIsTrue(False)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsTrue(truthy_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_true_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsTrue(falsey_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_true_when_passed_false(self):
        self.assertIsFalse(False)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_true(self):
        try:
            self.assertIsFalse(True)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_a_truthy_value(self):
        try:
            truthy_variable = 'A string'
            self.assertIsFalse(truthy_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_false_returns_false_when_passed_a_falsey_value(self):
        try:
            falsey_variable = None
            self.assertIsFalse(falsey_variable)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_none_returns_true_when_passed_none(self):
        self.assertIsNone(None)

    def test_uni_simple_test_case_assert_is_none_returns_false_when_passed_something_other_than_none(self):
        try:
            self.assertIsNone("test")

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_uni_simple_test_case_assert_is_not_none_returns_true_when_not_passed_something_other_than_none(self):
        self.assertIsNotNone('Anything that is not none')

    def test_uni_simple_test_case_assert_is_not_none_returns_false_when_passed_none(self):
        try:
            self.assertIsNone(None)

            # 'Test failed to produce expected assertion error'
            self.assertTrue(False)
        except AssertionError:
            # 'Test produced expected assertion error'
            self.assertTrue(True)

    def test_get_context_value_loads_the_correct_value_for_a_valid_key(self):
        key = 'testKey'
        value = 'A short test string'
        context = {
            key: value,
        }
        result = self.get_context_value(context, key)
        self.assertEqual(result, value)

    def test_get_context_value_throws_a_key_error_when_passed_an_invalid_key(self):
        key = 'testKey'
        value = 'A short test string'
        invalidKey = 'wrongKey'
        context = {
            key: value,
        }
        try:
            self.get_context_value(context, invalidKey)
            self.assertFalse('Test failed to produce expected key error')
        except KeyError:
            self.assertTrue('Test produced expected key error')


@tag('azure')
class CMSUrlRoutingTests(SimpleTestCase):

    def test_root_endpoints_and_include_mounts_resolve(self):
        routes = {
            '/robots.txt': core_views.robots,
            '/sitemap.xml': core_views.sitemap_primary,
            '/sitemaps/content.xml': core_views.content_sitemap,
            '/sitemaps/cms_pages.xml': cms_urls.sitemap,
            '/feedback': core_views.submit_feedback,
            '/jsonfiles/subjects': core_views.get_subjects_json,
            '/jsonfiles/institutions/en/': core_views.get_institutions_json,
            '/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/course-details/123/biology/full/': course_views.courses_detail,
            '/institution-details/123/': institution_views.institution_detail,
            '/course-comparison/': course_views.compare_courses,
            '/ajax/course-comparison/': course_views.compare_courses_body,
            '/regional_earnings': course_views.regional_earnings,
            '/v2/widget/configurator/': widget_views.configurator_view,
            '/v2/Widget/configurator/': widget_views.configurator_view,
        }

        for url, expected_view in routes.items():
            with self.subTest(url=url):
                self.assertIs(resolve(url).func, expected_view)

    def test_language_prefixed_routes_resolve_through_welsh_urlconf(self):
        routes = {
            '/en/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/en/course-finder/results/subject': coursesearch_views.course_finder_results_new,
            '/en/course-finder/results/institution': coursesearch_views.course_finder_results_new,
            '/en/course-details/123/biology/full/': course_views.courses_detail,
            '/en/course-details/translations/': translate_views.get_translations,
            '/en/institution-details/123/': institution_views.institution_detail,
            '/en/cymharu-cyrsiau/': course_views.compare_courses,
            '/en/ajax/course-comparison/': course_views.compare_courses_body,
            '/cy/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/cy/course-finder/results/subject': coursesearch_views.course_finder_results_new,
            '/cy/course-finder/results/institution': coursesearch_views.course_finder_results_new,
            '/cy/course-details/123/biology/full/': course_views.courses_detail,
            '/cy/course-details/translations/': translate_views.get_translations,
            '/cy/institution-details/123/': institution_views.institution_detail,
            '/cy/cymharu-cyrsiau/': course_views.compare_courses,
            '/cy/ajax/course-comparison/': course_views.compare_courses_body,
        }

        for url, expected_view in routes.items():
            with self.subTest(url=url):
                self.assertIs(resolve(url).func, expected_view)

    def test_framework_owned_document_and_wagtail_routes_resolve(self):
        documents_view = resolve('/documents/1/sample.pdf').func
        self.assertTrue(documents_view.__module__.startswith('wagtail.documents'))

        wagtail_view = resolve('/this-path-is-served-by-wagtail/').func
        self.assertTrue(wagtail_view.__module__.startswith('wagtail'))

    def test_urlconf_conditions_register_admin_and_debug_routes(self):
        urlconf_path = Path(cms_urls.__file__)

        for read_only, debug in ((False, False), (True, False), (False, True), (True, True)):
            with self.subTest(read_only=read_only, debug=debug):
                module_name = f'CMS._test_urls_{read_only}_{debug}'
                with override_settings(READ_ONLY=read_only, DEBUG=debug):
                    spec = importlib.util.spec_from_file_location(module_name, urlconf_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    try:
                        spec.loader.exec_module(module)
                        route_strings = [str(pattern.pattern) for pattern in module.urlpatterns]
                    finally:
                        del sys.modules[module_name]

                self.assertEqual('django-admin/' in route_strings, not read_only)
                self.assertEqual('admin/' in route_strings, not read_only)
                self.assertEqual('__debug__/' in route_strings, debug)


@tag('azure')
class TranslationHelperTests(SimpleTestCase):

    def test_term_for_key_looks_up_each_translation_dictionary(self):
        self.assertEqual(translations.term_for_key('Search', 'cy'), 'Chwilio')
        self.assertEqual(translations.term_for_key('no_data_available', 'en'), 'No data available')
        self.assertEqual(translations.term_for_key('administrative_occupations', 'en'), 'Administrative occupations')
        self.assertEqual(
            translations.term_for_key('unavailable_northern_ireland', 'en'),
            'Sorry, this data is not available for courses in Northern Ireland.',
        )
        self.assertEqual(translations.term_for_key('not_available', 'en'), 'Not Available')

    def test_unknown_translation_returns_normalized_key_and_cleanup_key_preserves_internal_tokens(self):
        self.assertEqual(translations.term_for_key('Unknown, Term!', 'en'), 'unknown_term')
        self.assertEqual(cleanup_key('Hello, World! _-'), 'hello_world___')


@tag('azure')
class NavigationContextProcessorTests(SimpleTestCase):

    def test_parse_menu_item_handles_labels_urls_and_nested_children(self):
        leaf = Mock(
            value={
                'label': 'Search courses',
                'link_page': Mock(title='Search', url='/search/'),
            },
        )
        nested = Mock(
            value={
                'label': 'Courses',
                'menu_items': [leaf],
            },
        )

        self.assertEqual(
            nav_context_processor.parse_menu_item(leaf), {
                'label': 'Search courses',
                'sub_items': None,
                'url': '/search/',
            },
        )
        self.assertEqual(
            nav_context_processor.parse_menu_item(nested), {
                'label': 'Courses',
                'sub_items': [
                    {
                        'label': 'Search courses',
                        'sub_items': None,
                        'url': '/search/',
                    },
                ],
            },
        )

    def test_parse_menu_item_falls_back_to_page_title_and_missing_url(self):
        menu_item = Mock(
            value={
                'link_page': Mock(title='About', url=None),
            },
        )

        self.assertEqual(
            nav_context_processor.parse_menu_item(menu_item), {
                'label': 'About',
                'sub_items': None,
                'url': None,
            },
        )

    def test_get_menu_selects_language_menu_and_returns_empty_for_missing_menu(self):
        menu_item = Mock(
            value={
                'label': 'About',
                'link_page': Mock(url='/about/'),
            },
        )
        model = Mock()
        model.objects.filter.return_value.first.return_value = Mock(menu_items=[menu_item])

        self.assertEqual(
            nav_context_processor.get_menu(model, 'en', 'menu_items'), [
                {
                    'label': 'About',
                    'sub_items': None,
                    'url': '/about/',
                },
            ],
        )
        model.objects.filter.assert_called_once_with(name='English')

        model.objects.filter.return_value.first.return_value = None
        self.assertEqual(nav_context_processor.get_menu(model, 'cy', 'menu_items'), [])
        model.objects.filter.assert_called_with(name='Welsh')

    @patch('CMS.context_processors.nav_context_processor.get_menu')
    @patch('CMS.context_processors.nav_context_processor.get_page_for_language')
    def test_nav_menu_render_builds_language_specific_brand_and_links(self, get_page, get_menu):
        get_page.side_effect = lambda language, pages: Mock(url=f'/{language}-page/')
        get_menu.side_effect = [
                                   [
                                       {
                                           'label': 'primary',
                                       },
                                   ],
                                   [
                                       {
                                           'label': 'footer',
                                       },
                                   ],
                               ] * 2
        factory = RequestFactory()

        english = nav_context_processor.nav_menu_render(factory.get('/course-finder/'))['navigation']
        welsh = nav_context_processor.nav_menu_render(factory.get('/cy/'))['navigation']

        self.assertEqual(
            english['brand_logo'], {
                'img': 'images/logos/nav_logo_english.svg',
                'url': '/',
            },
        )
        self.assertEqual(
            welsh['brand_logo'], {
                'img': 'images/logos/nav_logo_welsh.svg',
                'url': '/cy/',
            },
        )
        self.assertEqual(english['comp_menu'][0]['url'], '/en-page/')
        self.assertEqual(welsh['comp_menu'][0]['url'], '/cy-page/')
        self.assertEqual(
            english['primary_menu'], [
                {
                    'label': 'primary',
                },
            ],
        )
        self.assertEqual(
            welsh['footer_menu'], [
                {
                    'label': 'footer',
                },
            ],
        )
        self.assertEqual(get_page.call_count, 6)
        self.assertEqual(get_menu.call_count, 4)
