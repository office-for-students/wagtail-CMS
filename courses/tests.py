import json
from threading import local
from unittest.mock import Mock, patch

from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings, tag
from django.urls import resolve
from requests.models import Response

from CMS.test.utils import UniSimpleTestCase
from core.request_handler import REQUEST_TIMEOUT
from courses import request_handler
from courses.models import (
    AccreditationBlock,
    AfterOneYearBlock,
    Course,
    EarningsAfterCourseBlock,
    EntryInformationBlock,
    SatisfactionBlock,
)
from courses.test_files.course_mocks import CourseMocks
from courses.views import compare_courses, compare_courses_body, courses_detail, regional_earnings
from courses.views.translate import get_translations
from errors.models import ApiError


@tag('azure')
class CoursesModelsTests(UniSimpleTestCase):

    def test_SatisfactionBlock_returns_student_satisfaction_data_set_value(self):
        satisfaction_block = SatisfactionBlock().meta.value_class
        self.assertEqual(satisfaction_block.data_set(), 'student_satisfaction')

    def test_EntryInformationBlock_returns_entry_information_data_set_value(self):
        entry_block = EntryInformationBlock().meta.value_class
        self.assertEqual(entry_block.data_set(), 'entry_information')

    def test_AfterOneYearBlock_returns_after_one_year_data_set_value(self):
        one_year_block = AfterOneYearBlock().meta.value_class
        self.assertEqual(one_year_block.data_set(), 'after_one_year')

    def test_AfterCourseBlock_returns_after_the_course_data_set_value(self):
        after_course_block = EarningsAfterCourseBlock().meta.value_class
        self.assertEqual(after_course_block.data_set(), 'earnings_after_the_course')

    def test_AccreditationBlock_returns_professional_accreditation_data_set_value(self):
        accreditation_block = AccreditationBlock().meta.value_class
        self.assertEqual(accreditation_block.data_set(), 'professional_accreditation')

    @patch('courses.request_handler.load_course_data', return_value=CourseMocks.get_unsuccessful_course_load_response())
    def test_course_find_returns_api_error_if_course_not_found(self, mock_response):
        course, error = Course.find('10000055', 'AB20', 'Full-time', 'en')

        self.assertIsNone(course)
        self.assertIsInstance(error, ApiError)
        self.assertEqual(error.status_code, 500)
        mock_response.assert_called_once_with('10000055', 'AB20', 1)

    @patch.object(Course, '__init__', return_value=None)
    @patch('courses.request_handler.load_course_data', return_value=CourseMocks.get_successful_course_load_response())
    def test_course_find_constructs_course_from_successful_response(self, load_course_data, course_init):
        course, error = Course.find('10000055', 'AB20', 'Full-time', 'en')

        self.assertIsInstance(course, Course)
        self.assertIsNone(error)
        course_init.assert_called_once_with(CourseMocks.get_successful_course_load_content(), 'en')
        load_course_data.assert_called_once_with('10000055', 'AB20', 1)

    @patch.object(Course, '__init__', return_value=None)
    @patch('courses.request_handler.load_course_data', return_value={'id': 'course-record'})
    def test_course_find_constructs_course_from_dictionary_response(self, load_course_data, course_init):
        course, error = Course.find('10000055', 'AB20', 'Part-time', 'cy')

        self.assertIsInstance(course, Course)
        self.assertIsNone(error)
        course_init.assert_called_once_with({'id': 'course-record'}, 'cy')
        load_course_data.assert_called_once_with('10000055', 'AB20', 2)

    def test_get_mode_code_maps_known_modes_and_returns_none_for_unknown(self):
        self.assertEqual(Course.get_mode_code('Full-time'), 1)
        self.assertEqual(Course.get_mode_code('PartTime'), 2)
        self.assertIsNone(Course.get_mode_code('Evening'))


@tag('azure')
class CourseRequestHandlerTests(SimpleTestCase):

    def setUp(self) -> None:
        cache.clear()

    @staticmethod
    def successful_response(payload: dict[str, str]) -> Response:
        response = Response()
        response.status_code = 200
        response._content = json.dumps(payload).encode('utf-8')
        return response

    @patch('courses.request_handler._get_session')
    def test_load_course_data_formats_url_header_and_timeout(self, get_session: Mock) -> None:
        session = Mock()
        session.get.return_value = self.successful_response({'id': 'course-record'})
        get_session.return_value = session
        with patch('courses.request_handler.settings.DATASETAPIHOST', 'https://dataset.example'), \
                patch('courses.request_handler.settings.DATASETAPIKEY', 'test-api-key-not-real'):
            result = request_handler.load_course_data('10000055', 'AB20', 1)

        self.assertEqual(result, {'id': 'course-record'})
        session.get.assert_called_once_with(
            url='https://dataset.example/institutions/10000055/courses/AB20/modes/1',
            headers={'Ocp-Apim-Subscription-Key': 'test-api-key-not-real'},
            timeout=REQUEST_TIMEOUT,
        )

    @patch('courses.request_handler._get_session')
    def test_load_course_data_caches_successful_payload(self, get_session: Mock) -> None:
        session = Mock()
        session.get.return_value = self.successful_response({'id': 'course-record'})
        get_session.return_value = session

        first = request_handler.load_course_data('10000055', 'AB20', 1)
        second = request_handler.load_course_data('10000055', 'AB20', 1)

        self.assertEqual(first, {'id': 'course-record'})
        self.assertEqual(second, first)
        session.get.assert_called_once()

    @patch('courses.request_handler._get_session')
    def test_load_course_data_does_not_cache_unsuccessful_responses(self, get_session: Mock) -> None:
        session = Mock()
        response = Response()
        response.status_code = 404
        session.get.return_value = response
        get_session.return_value = session

        first = request_handler.load_course_data('10000055', 'AB20', 1)
        second = request_handler.load_course_data('10000055', 'AB20', 1)

        self.assertIs(first, response)
        self.assertIs(second, response)
        self.assertEqual(session.get.call_count, 2)

    @patch('courses.request_handler._get_session')
    def test_load_course_data_separates_cache_entries_by_course_and_mode(self, get_session: Mock) -> None:
        session = Mock()
        session.get.side_effect = [
            self.successful_response({'id': 'first'}),
            self.successful_response({'id': 'second-mode'}),
            self.successful_response({'id': 'second-course'}),
        ]
        get_session.return_value = session

        first = request_handler.load_course_data('10000055', 'AB20', 1)
        second_mode = request_handler.load_course_data('10000055', 'AB20', 2)
        second_course = request_handler.load_course_data('10000055', 'XY10', 1)

        self.assertEqual(first, {'id': 'first'})
        self.assertEqual(second_mode, {'id': 'second-mode'})
        self.assertEqual(second_course, {'id': 'second-course'})
        self.assertEqual(session.get.call_count, 3)

    def test_get_session_reuses_session_in_same_thread(self) -> None:
        with patch.object(request_handler, '_SESSION_LOCAL', local()), \
                patch('courses.request_handler.requests.Session') as session_factory:
            first = request_handler._get_session()
            second = request_handler._get_session()

        self.assertIs(first, second)
        session_factory.assert_called_once_with()

    @patch('courses.request_handler._get_session')
    def test_non_object_success_response_remains_a_response(self, get_session: Mock) -> None:
        session = Mock()
        response = Response()
        response.status_code = 200
        response._content = b'[]'
        session.get.return_value = response
        get_session.return_value = session

        result = request_handler.load_course_data('10000055', 'AB20', 1)

        self.assertIs(result, response)
        session.get.assert_called_once()

    @override_settings(COURSE_DATA_CACHE_SECONDS=0)
    @patch('courses.request_handler._get_session')
    def test_zero_cache_ttl_disables_course_data_cache(self, get_session: Mock) -> None:
        session = Mock()
        session.get.side_effect = [
            self.successful_response({'id': 'first'}),
            self.successful_response({'id': 'second'}),
        ]
        get_session.return_value = session

        request_handler.load_course_data('10000055', 'AB20', 1)
        second = request_handler.load_course_data('10000055', 'AB20', 1)

        self.assertEqual(second, {'id': 'second'})
        self.assertEqual(session.get.call_count, 2)


@tag('azure')
class CourseTranslationEndpointTests(SimpleTestCase):

    def test_non_ajax_and_ajax_get_requests_are_rejected(self):
        factory = RequestFactory()

        self.assertEqual(get_translations(factory.get('/course-details/translations/')).status_code, 400)
        ajax_get = factory.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(get_translations(ajax_get).status_code, 400)

    @patch('courses.views.translate.translations.term_for_key', side_effect=lambda key, language: f'{language}:{key}')
    def test_ajax_post_returns_translated_terms(self, term_for_key):
        request = RequestFactory().post(
            '/',
            data=json.dumps({'language': 'cy', 'terms': ['search', 'compare']}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        response = get_translations(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ['cy:search', 'cy:compare'])
        self.assertEqual(term_for_key.call_count, 2)

    def test_ajax_post_rejects_more_than_twenty_five_terms(self):
        request = RequestFactory().post(
            '/',
            data=json.dumps({'language': 'en', 'terms': [f'term-{index}' for index in range(26)]}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        with self.assertRaisesRegex(Exception, 'to big'):
            get_translations(request)


@tag('azure')
class CourseEndpointTests(SimpleTestCase):

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

    @patch('courses.views.comparison_body.render', return_value=HttpResponse('comparison body', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    def test_ajax_comparison_without_courses_shows_not_enough_message(self, term_for_key, render):
        response = self.client.get('/ajax/course-comparison/')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(render.call_args.args[1], 'courses/comparison/has_no_compare_courses.html')
        self.assertEqual(render.call_args.kwargs['status'], 206)
        term_for_key.assert_called_once_with('can_compare_courses', 'en')

    @patch('courses.views.comparison_body.render', return_value=HttpResponse('no bookmarks', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='term')
    @patch('courses.views.comparison_body.InstitutionList.get_options', return_value={'en': []})
    def test_comparison_without_storage_shows_no_bookmarked_courses(self, get_options, term_for_key, render):
        response = self.client.get('/ajax/course-comparison/?hasStorage=0')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(render.call_args.args[1], 'courses/comparison/has_no_saved_courses.html')
        get_options.assert_called_once_with()
        self.assertGreater(term_for_key.call_count, 0)

    @patch('courses.views.comparison_body.render', return_value=HttpResponse('not enough', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    @patch('courses.views.comparison_body.Course.find')
    def test_comparison_with_one_course_shows_not_enough_message(self, find, term_for_key, render):
        response = self.client.get('/ajax/course-comparison/', {'courses': ['institution/course/1']})

        self.assertEqual(response.status_code, 206)
        self.assertEqual(render.call_args.args[1], 'courses/comparison/has_no_compare_courses.html')
        find.assert_not_called()
        term_for_key.assert_called_once_with('can_compare_courses', 'en')

    @patch('courses.views.comparison_body.Course.find')
    @patch('courses.views.comparison_body.renderer.dataset_for_comparison_view', return_value=[{'id': 'course'}])
    @patch('courses.views.comparison_body.render', return_value=HttpResponse('comparison'))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    def test_comparison_caps_course_lookups_at_seven(self, term_for_key, render, dataset, find):
        courses = [f'institution/{index}/1' for index in range(8)]
        find.side_effect = [(Mock(id=str(index)), None) for index in range(8)]

        response = self.client.get('/ajax/course-comparison/', {'courses': courses})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(find.call_count, 7)
        rendered_courses = render.call_args.args[2]['courses']
        self.assertEqual(len(rendered_courses), 7)
        dataset.assert_called_once_with(rendered_courses, 'en')
        self.assertEqual(term_for_key.call_args.args, ('can_compare_courses', 'en'))

    @patch('courses.views.comparison_body.Course.find', return_value=(None, Mock(status_code=404)))
    @patch('courses.views.comparison_body.renderer.dataset_for_comparison_view', return_value=[{'id': 'placeholder'}])
    @patch('courses.views.comparison_body.render', return_value=HttpResponse('comparison'))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    def test_comparison_logs_course_lookup_failures(self, term_for_key, render, dataset, find):
        with self.assertLogs('courses.views.comparison_body', level='WARNING') as logs:
            response = self.client.get('/ajax/course-comparison/', {'courses': ['institution/course/1', 'institution/course/2']})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any('Failed to fetch course' in message for message in logs.output))
        find.assert_called()

    @patch('courses.views.comparison_body.Course.find', return_value=(Mock(), None))
    @patch('courses.views.comparison_body.renderer.dataset_for_comparison_view', return_value=[])
    @patch('courses.views.comparison_body.render', return_value=HttpResponse('not enough', status=206))
    @patch('courses.views.comparison_body.translations.term_for_key', return_value='Compare courses')
    def test_comparison_with_empty_dataset_shows_not_enough_message(self, term_for_key, render, dataset, find):
        response = self.client.get('/ajax/course-comparison/', {'courses': ['institution/1/1', 'institution/2/1']})

        self.assertEqual(response.status_code, 206)
        self.assertEqual(render.call_args.args[1], 'courses/comparison/has_no_compare_courses.html')
        dataset.assert_called_once()
        find.assert_called()

    def test_course_urls_resolve_to_their_views(self):
        routes = {
            '/course-details/123/biology/full/': courses_detail,
            '/course-details/translations/': get_translations,
            '/course-comparison/': compare_courses,
            '/ajax/course-comparison/': compare_courses_body,
            '/regional_earnings': regional_earnings,
        }

        for url, expected_view in routes.items():
            with self.subTest(url=url):
                self.assertIs(resolve(url).func, expected_view)