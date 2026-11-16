import json
import logging
from unittest.mock import Mock, mock_open, patch

from django.http import HttpResponse
from django.test import Client, RequestFactory, SimpleTestCase, TestCase, override_settings, tag
from wagtail.models import Page

from CMS.enums import enums
from CMS.test.utils import UniSimpleTestCase
from core import request_handler, utils
from core.exceptions import VirusException
from core.templatetags import discover_uni_tags
from core.utils import get_page_for_language

logger = logging.getLogger(__name__)
logging.basicConfig(level=9999) # suppress logs during unit tests


@tag('azure')
class CoreUtilsTests(UniSimpleTestCase):

    def test_get_page_for_language_returns_no_page_for_welsh_if_no_english_exists(self):
        pages = Page.objects.none()
        self.assertEqual(len(pages), 0)

        found_page = get_page_for_language(enums.languages.WELSH, pages)
        self.assertIsNone(found_page)

    def test_get_language_detects_welsh_paths_only(self):
        self.assertEqual(utils.get_language('/cy/course-finder/'), 'cy')
        self.assertEqual(utils.get_language('/course-finder/'), 'en')
        self.assertEqual(utils.get_language(None), 'en')

    def test_get_page_for_language_returns_matching_page(self):
        english_page = Mock(get_language=Mock(return_value='en'))
        welsh_page = Mock(get_language=Mock(return_value='cy'))

        self.assertIs(utils.get_page_for_language('cy', [english_page, welsh_page]), welsh_page)

    def test_get_page_for_language_falls_back_to_english(self):
        english_page = Mock(get_language=Mock(return_value='en'))
        welsh_page = Mock(get_language=Mock(return_value='cy'))

        self.assertIs(utils.get_page_for_language('cy', [english_page]), english_page)
        self.assertIs(utils.get_page_for_language('en', [english_page, welsh_page]), english_page)

    def test_get_page_for_language_returns_first_duplicate_match(self):
        first_page = Mock(get_language=Mock(return_value='en'))
        second_page = Mock(get_language=Mock(return_value='en'))

        self.assertIs(utils.get_page_for_language('en', [first_page, second_page]), first_page)

    def test_fallback_to_uses_default_only_for_none(self):
        self.assertEqual(utils.fallback_to(None, 'default'), 'default')
        self.assertEqual(utils.fallback_to('', 'default'), '')

    @override_settings(CLAMAV_ACTIVE=False)
    @patch('core.utils.get_clam')
    def test_is_infected_skips_clam_when_disabled(self, get_clam):
        self.assertEqual(utils.is_infected(b'file contents'), (None, ''))
        get_clam.assert_called_once_with()

    @override_settings(CLAMAV_ACTIVE=True)
    @patch('core.utils.get_clam')
    def test_is_infected_reports_clean_and_infected_streams(self, get_clam):
        clam = Mock()
        get_clam.return_value = clam
        clam.scan_stream.return_value = None
        self.assertEqual(utils.is_infected(b'clean'), (False, ''))

        clam.scan_stream.return_value = {'stream': ('FOUND', 'Example.Virus')}
        self.assertEqual(utils.is_infected(b'infected'), (True, 'Example.Virus'))

    @patch('core.utils.pyclamd.ClamdUnixSocket')
    def test_get_clam_returns_reachable_unix_socket(self, unix_socket):
        clam = unix_socket.return_value

        self.assertIs(utils.get_clam(), clam)
        clam.ping.assert_called_once_with()

    @patch('core.utils.pyclamd.ClamdNetworkSocket')
    @patch('core.utils.pyclamd.ClamdUnixSocket')
    def test_get_clam_uses_network_socket_when_unix_socket_fails(self, unix_socket, network_socket):
        unix_socket.return_value.ping.side_effect = utils.pyclamd.ConnectionError
        clam = network_socket.return_value

        self.assertIs(utils.get_clam(), clam)
        network_socket.assert_called_once_with()
        clam.ping.assert_called_once_with()

    @patch('core.utils.pyclamd.ClamdNetworkSocket')
    @patch('core.utils.pyclamd.ClamdUnixSocket')
    def test_get_clam_raises_when_both_sockets_fail(self, unix_socket, network_socket):
        unix_socket.return_value.ping.side_effect = utils.pyclamd.ConnectionError
        network_socket.return_value.ping.side_effect = utils.pyclamd.ConnectionError

        with self.assertRaisesRegex(ValueError, 'could not connect to clamd'):
            utils.get_clam()

    @patch('core.utils.is_infected', return_value=(False, ''))
    def test_check_for_virus_returns_clean_instance(self, is_infected):
        instance = Mock()
        instance.file.closed = False
        instance.file.read.return_value = b'clean'

        self.assertIs(utils.check_for_virus(instance), instance)
        is_infected.assert_called_once_with(b'clean')

    @patch('core.utils.is_infected', return_value=(True, 'Example.Virus'))
    def test_check_for_virus_raises_for_infected_file(self, is_infected):
        instance = Mock()
        instance.file.closed = False
        instance.file.read.return_value = b'infected'

        with self.assertRaisesRegex(VirusException, 'Example.Virus'):
            utils.check_for_virus(instance)

    @patch('core.utils.get_json_file')
    def test_get_current_version_returns_remote_version_or_empty_string(self, get_json_file):
        response = Mock(ok=True)
        response.json.return_value = {'version': '2.1'}
        get_json_file.return_value = response
        self.assertEqual(utils.get_current_version(), '2.1')

        get_json_file.return_value = Mock(ok=False)
        self.assertEqual(utils.get_current_version(), '')

    def test_get_code_version_reads_version_file(self):
        self.assertTrue(utils.get_code_version())

    def test_get_new_landing_page_for_language(self):
        self.assertEqual(utils.get_new_landing_page_for_language('en'), '/')
        self.assertEqual(utils.get_new_landing_page_for_language('cy'), '/cy/')


@tag('azure')
class CoreRequestHandlerTests(SimpleTestCase):

    @override_settings(DATASETAPIKEY='test-api-key-not-real', FEEDBACK_API_HOST='https://feedback.example')
    @patch('core.request_handler.requests.post')
    def test_send_feedback_forwards_payload_and_subscription_header(self, post):
        request_handler.send_feedback('payload')

        post.assert_called_once_with(
            url='https://feedback.example',
            headers={'Ocp-Apim-Subscription-Key': 'test-api-key-not-real'},
            data='payload',
        )

    @override_settings(LOCAL='True')
    @patch('builtins.open', mock_open(read_data='[{"id":"01"}]'))
    def test_get_json_file_reads_local_json(self):
        response = request_handler.get_json_file('test.json')

        self.assertTrue(response.ok)
        self.assertEqual(response.json(), [{'id': '01'}])

    @override_settings(LOCAL=False, JSONFILES_STORAGE_CONTAINER='https://files.example')
    @patch.dict('os.environ', {'JSONFILES_STORAGE_CONTAINER': 'https://files.example'})
    @patch('core.request_handler.requests.get')
    def test_get_json_file_fetches_remote_json(self, get):
        request_handler.get_json_file('institutions_en.json')

        get.assert_called_once_with('https://files.example/institutions_en.json')

    @override_settings(LOCAL='True', JSONFILES_STORAGE_CONTAINER='')
    def test_get_sitemap_file_returns_local_xml(self):
        response = request_handler.get_sitemap_file()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '<xml></xml>')

    @override_settings(LOCAL=False, JSONFILES_STORAGE_CONTAINER='https://files.example')
    @patch('core.request_handler.requests.get')
    def test_get_sitemap_file_fetches_remote_xml(self, get):
        request_handler.get_sitemap_file()

        get.assert_called_once_with('https://files.example/sitemaps.xml')

    def test_is_ajax_accepts_both_header_representations(self):
        factory = RequestFactory()

        self.assertTrue(request_handler.is_ajax(factory.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')))
        self.assertTrue(request_handler.is_ajax(factory.get('/', headers={'x-requested-with': 'XMLHttpRequest'})))
        self.assertFalse(request_handler.is_ajax(factory.get('/')))


@tag('azure')
class DiscoverUniTemplateTagTests(SimpleTestCase):

    def test_queryparams_omits_none_and_returns_empty_for_no_values(self):
        self.assertEqual(discover_uni_tags.queryparams(page=2, ignored=None), '?page=2')
        self.assertEqual(discover_uni_tags.queryparams(ignored=None), '')

    def test_string_and_sequence_helpers(self):
        self.assertTrue(discover_uni_tags.is_string('course'))
        self.assertFalse(discover_uni_tags.is_string(2))
        self.assertEqual(discover_uni_tags.create_list('a', 'b'), ('a', 'b'))
        self.assertEqual(discover_uni_tags.length_of_list([1, 2]), 2)
        self.assertEqual(list(discover_uni_tags.times(3)), [0, 1, 2])
        self.assertEqual(discover_uni_tags.get_index(1, ['a', 'b']), 'b')
        self.assertIsNone(discover_uni_tags.get_index(2, ['a', 'b']))

    def test_text_helpers_cover_values_and_missing_indices(self):
        self.assertEqual(discover_uni_tags.title_to_id('Course Finder'), 'course_finder')
        self.assertEqual(discover_uni_tags.split_by_line_break(text='one\n\ntwo', index=1), 'two')
        self.assertEqual(discover_uni_tags.split_by_line_break(text='one', index=2), '')
        self.assertEqual(discover_uni_tags.brackets_replace_year('Year {}', '2025'), 'Year 2025')
        self.assertEqual(discover_uni_tags.brackets_replace_year('', '2025'), '')

    @patch('core.templatetags.discover_uni_tags.translations.term_for_key')
    def test_translation_and_availability_tags_apply_language_and_substitutions(self, term_for_key):
        term_for_key.side_effect = ['No data available', 'Only %s places', 'No data available']

        self.assertEqual(discover_uni_tags.data_not_available(language='en', subject='No data available'), 'hidden')
        self.assertEqual(discover_uni_tags.get_translation(key='places', language='en', substitutions=('5',)), 'Only 5 places')
        self.assertEqual(discover_uni_tags.map_distance_learning_values('no_data_available', 'cy'), 'No data available')
        self.assertEqual(term_for_key.call_args_list[0].kwargs, {'key': 'no_data_available', 'language': 'en'})

    def test_course_name_location_and_value_helpers(self):
        course = {
            'qualification': 'BSc',
            'honours_award': 1,
            'title': {'english': 'Biology', 'welsh': 'Bioleg'},
        }
        self.assertEqual(discover_uni_tags.get_course_name(course, True), 'BSc (Hons) Biology')
        self.assertEqual(discover_uni_tags.get_course_name(course, False), 'BSc (Hons) Bioleg')
        self.assertEqual(
            discover_uni_tags.get_course_locations_list([
                {'english': 'Campus A', 'welsh': 'Campws A'},
                {'english': '', 'welsh': 'Campws B'},
            ], True),
            'Campus A,Campws B',
        )
        self.assertEqual(discover_uni_tags.get_course_locations_list([{'english': 'Campus A', 'welsh': 'Campws A'}], False), 'Campws A')
        self.assertEqual(discover_uni_tags.get_max_length([1, 2], [3]), 2)
        self.assertEqual(discover_uni_tags.get_salary_from_index([10], 4), 10)
        self.assertIsNone(discover_uni_tags.get_item_at_index(['a'], 4))
        self.assertEqual(discover_uni_tags.insert_values_to_plain_text(content='Hello {}', substitutions=('world',)), 'Hello world')
        self.assertEqual(discover_uni_tags.concat('a', 2, 'c'), 'a2c')
        self.assertTrue(discover_uni_tags.is_multiple_of(9, 3))
        self.assertFalse(discover_uni_tags.is_franchise('123', '123'))


@tag('azure')
class BaseTestCase(TestCase):
    institution_id  = 10005343

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()


@tag('azure')
class CoreEndpointTests(SimpleTestCase):

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

    @patch('core.views.get_json_file')
    def test_subjects_endpoint_returns_empty_object_for_failed_request(self, get_json_file):
        get_json_file.return_value = Mock(ok=False, status_code=503)

        response = self.client.get('/jsonfiles/subjects')

        self.assertEqual(response.status_code, 503)
        self.assertJSONEqual(response.content, {})

    @patch('core.views.load_institution_json', return_value={'en': [{'id': '1'}]})
    def test_institutions_endpoint_returns_requested_language(self, load_institution_json):
        response = self.client.get('/jsonfiles/institutions/en/')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [{'id': '1'}])
        load_institution_json.assert_called_once_with()
