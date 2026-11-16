import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import SimpleTestCase
from django.test import override_settings
from django.test import tag
from django.urls import resolve

from CMS import urls as cms_urls
from CMS.test.utils import UniSimpleTestCase
from core import views as core_views
from courses import views as course_views
from courses.views import translate as translate_views
from coursesearch import api as coursesearch_api
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
class CMSDirectEndpointTests(SimpleTestCase):

    @patch('core.views.render', return_value=HttpResponse('robots', content_type='text/plain'))
    def test_robots_endpoint_renders_plain_text(self, render):
        response = self.client.get('/robots.txt')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'robots')
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertEqual(render.call_args.args[1], 'robots.txt')

    @patch('core.views.render', return_value=HttpResponse('<urlset/>', content_type='text/xml'))
    def test_primary_sitemap_endpoint_renders_xml(self, render):
        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'<urlset/>')
        self.assertEqual(response['Content-Type'], 'text/xml')
        self.assertEqual(render.call_args.args[1], 'sitemap_primary.xml')

    @patch('core.views.get_sitemap_file')
    def test_content_sitemap_endpoint_propagates_upstream_response(self, get_sitemap_file):
        get_sitemap_file.return_value = Mock(content=b'<xml>content</xml>', status_code=206)

        response = self.client.get('/sitemaps/content.xml')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.content, b'<xml>content</xml>')
        self.assertEqual(response['Content-Type'], 'text/xml')
        get_sitemap_file.assert_called_once_with()

    @patch('core.views.send_feedback')
    def test_feedback_endpoint_forwards_normalized_feedback(self, send_feedback):
        send_feedback.return_value = Mock(ok=True, status_code=202)

        response = self.client.post('/feedback', {
            'page': '/course-finder/',
            'user_feedback': 'Helpful results',
            'ignored': 'not forwarded',
        })

        self.assertEqual(response.status_code, 202)
        self.assertJSONEqual(response.content, {})
        feedback = json.loads(send_feedback.call_args.args[0])
        self.assertEqual(feedback, {
            'is_useful': True,
            'questions': [{
                'title': 'howwasthisuseful',
                'feedback': 'Helpful results',
            }],
            'page': '/course-finder/',
        })

    @patch('core.views.send_feedback')
    def test_feedback_endpoint_propagates_upstream_error(self, send_feedback):
        upstream_response = Mock(ok=False, status_code=400)
        upstream_response.json.return_value = {'error': 'invalid feedback'}
        send_feedback.return_value = upstream_response

        response = self.client.post('/feedback', {'user_feedback': 'Feedback'})

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'invalid feedback'})

    @patch('core.views.get_json_file')
    def test_subjects_endpoint_returns_json_file_content(self, get_json_file):
        result = Mock(ok=True, status_code=200)
        result.json.return_value = [{'id': '01', 'name': 'Biology'}]
        get_json_file.return_value = result

        response = self.client.get('/jsonfiles/subjects')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [{'id': '01', 'name': 'Biology'}])
        get_json_file.assert_called_once_with('subjects.json')

    @patch('core.views.load_institution_json', return_value={'en': [{'id': '1'}]})
    def test_institutions_endpoint_returns_requested_language(self, load_institution_json):
        response = self.client.get('/jsonfiles/institutions/en/')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [{'id': '1'}])
        load_institution_json.assert_called_once_with()

    @patch('courses.views.views.render', return_value=HttpResponse('comparison'))
    @patch('courses.views.views.get_page_for_language')
    def test_english_comparison_endpoint_renders_comparison_page(self, get_page, render):
        page = Mock()
        page.get_context.return_value = {'existing': 'context'}
        get_page.return_value = page

        response = self.client.get('/course-comparison/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'comparison')
        get_page.assert_called_once()
        self.assertEqual(get_page.call_args.args[0], 'en')
        self.assertEqual(render.call_args.args[1], 'courses/course_comparison_page.html')
        self.assertIs(render.call_args.args[2]['page'], page)

    @patch('courses.views.views.render', return_value=HttpResponse('comparison'))
    @patch('courses.views.views.get_page_for_language')
    def test_welsh_comparison_endpoint_passes_welsh_language(self, get_page, render):
        page = Mock()
        page.get_context.return_value = {}
        get_page.return_value = page

        response = self.client.get('/cy/cymharu-cyrsiau/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_page.call_args.args[0], 'cy')
        self.assertEqual(render.call_args.args[1], 'courses/course_comparison_page.html')

    @patch('courses.views.comparison_body.render', return_value=HttpResponse('comparison body', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    def test_ajax_comparison_endpoint_renders_empty_selection(self, term_for_key, render):
        response = self.client.get('/ajax/course-comparison/?courses=')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.content, b'comparison body')
        self.assertEqual(render.call_args.args[1], 'courses/comparison/has_no_compare_courses.html')
        self.assertEqual(render.call_args.kwargs['status'], 206)
        self.assertEqual(render.call_args.args[2]['page']['get_language'], 'en')
        term_for_key.assert_called_once_with('can_compare_courses', 'en')

    @patch('courses.views.comparison_body.render', return_value=HttpResponse('comparison body', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Cymharu cyrsiau')
    def test_welsh_ajax_comparison_endpoint_passes_welsh_language(self, term_for_key, render):
        response = self.client.get('/cy/ajax/course-comparison/?courses=')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(render.call_args.kwargs['status'], 206)
        self.assertEqual(render.call_args.args[2]['page']['get_language'], 'cy')
        term_for_key.assert_called_once_with('can_compare_courses', 'cy')

    def test_regional_earnings_endpoint_resolves_to_its_view(self):
        self.assertIs(resolve('/regional_earnings').func, course_views.regional_earnings)


@tag('azure')
class CMSUrlRoutingTests(SimpleTestCase):

    def test_every_registered_endpoint_resolves_to_its_view(self):
        routes = {
            '/robots.txt': core_views.robots,
            '/sitemap.xml': core_views.sitemap_new,
            '/sitemaps/content.xml': core_views.content_sitemap,
            '/sitemaps/general.xml': cms_urls.sitemap,
            '/feedback': core_views.submit_feedback,
            '/jsonfiles/subjects': core_views.get_subjects_json,
            '/jsonfiles/institutions/en/': core_views.get_institutions_json,
            '/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/course-finder/results/institution': coursesearch_views.course_finder_results_new,
            '/course-finder/results/subject': coursesearch_views.course_finder_results_new,
            '/course-finder/search/v2/api/courses/nested': coursesearch_api.api_proxy,
            '/course-details/123/biology/full/': course_views.courses_detail,
            '/course-details/translations/': translate_views.get_translations,
            '/institution-details/123/': institution_views.institution_detail,
            '/course-comparison/': course_views.compare_courses,
            '/ajax/course-comparison/': course_views.compare_courses_body,
            '/regional_earnings': course_views.regional_earnings,
            '/en/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/en/course-finder/results/institution': coursesearch_views.course_finder_results_new,
            '/en/course-finder/results/subject': coursesearch_views.course_finder_results_new,
            '/en/course-details/123/biology/full/': course_views.courses_detail,
            '/en/course-details/translations/': translate_views.get_translations,
            '/en/institution-details/123/': institution_views.institution_detail,
            '/en/cymharu-cyrsiau/': course_views.compare_courses,
            '/en/ajax/course-comparison/': course_views.compare_courses_body,
            '/cy/course-finder/results/': coursesearch_views.course_finder_results_new,
            '/cy/course-finder/results/institution': coursesearch_views.course_finder_results_new,
            '/cy/course-finder/results/subject': coursesearch_views.course_finder_results_new,
            '/cy/course-details/123/biology/full/': course_views.courses_detail,
            '/cy/course-details/translations/': translate_views.get_translations,
            '/cy/institution-details/123/': institution_views.institution_detail,
            '/cy/cymharu-cyrsiau/': course_views.compare_courses,
            '/cy/ajax/course-comparison/': course_views.compare_courses_body,
        }

        widget_routes = (
            ('configurator/', widget_views.configurator_view),
            ('configurator/guidance', widget_views.configurator_view),
            ('configurator/help', widget_views.configurator_view),
            ('configurator/privacy', widget_views.configurator_view),
            ('123/en', widget_views.v2_widget_placeholder_embed),
            ('api/all_institutions/', widget_views.v2_api_institutions),
            ('api/institution/123/courses', widget_views.v2_api_institution_courses),
            ('123/biology/full/en', widget_views.v2_widget_embed),
        )
        for prefix in ('/v2/widget/', '/v2/Widget/'):
            for suffix, view in widget_routes:
                routes[prefix + suffix] = view

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
