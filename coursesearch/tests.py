from unittest.mock import Mock, patch

import requests
from django.http import HttpResponse
from django.test import RequestFactory
from django.test import SimpleTestCase
from django.test import override_settings
from django.test import tag

from coursesearch import api
from coursesearch.api import MAX_BODY_BYTES
from coursesearch.api import api_proxy
from coursesearch.models import CourseFinderResults
from coursesearch.views import course_finder_results_new


@tag('azure')
class CourseFinderResultsEndpointTests(SimpleTestCase):
    english_urls = (
        '/course-finder/results/',
        '/course-finder/results/institution',
        '/course-finder/results/subject',
        '/en/course-finder/results/',
        '/en/course-finder/results/institution',
        '/en/course-finder/results/subject',
    )
    welsh_urls = (
        '/cy/course-finder/results/',
        '/cy/course-finder/results/institution',
        '/cy/course-finder/results/subject',
    )

    def setUp(self):
        self.page = object()

    @patch('coursesearch.views.render', return_value=HttpResponse('results'))
    @patch('coursesearch.views.get_page_for_language')
    def test_english_results_urls_render_the_results_template(self, get_page, render):
        get_page.return_value = self.page

        for url in self.english_urls:
            with self.subTest(url=url):
                get_page.reset_mock()
                render.reset_mock()
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                get_page.assert_called_once()
                render.assert_called_once()
                request, template, context = render.call_args.args
                self.assertEqual(request.path, url)
                self.assertEqual(template, 'coursefinder/course_finder_results.html')
                self.assertIs(context['page'], self.page)
                self.assertEqual(context['lang'], 'en')
                self.assertEqual(context['translated_url'], '/cy' + url.replace('/en/', '/'))

    @patch('coursesearch.views.render', return_value=HttpResponse('results'))
    @patch('coursesearch.views.get_page_for_language')
    def test_welsh_results_urls_render_the_results_template(self, get_page, render):
        get_page.return_value = self.page

        for url in self.welsh_urls:
            with self.subTest(url=url):
                get_page.reset_mock()
                render.reset_mock()
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                get_page.assert_called_once()
                render.assert_called_once()
                request, template, context = render.call_args.args
                self.assertEqual(request.path, url)
                self.assertEqual(template, 'coursefinder/course_finder_results.html')
                self.assertIs(context['page'], self.page)

    @patch('coursesearch.views.render', return_value=HttpResponse('results'))
    @patch('coursesearch.views.get_page_for_language')
    def test_results_view_uses_requested_welsh_language_and_translation(self, get_page, render):
        get_page.return_value = self.page
        request = RequestFactory().get('/cy/course-finder/results/')

        response = course_finder_results_new(request, language='cy')

        self.assertEqual(response.status_code, 200)
        context = render.call_args.args[2]
        self.assertEqual(context['lang'], 'cy')
        self.assertEqual(context['translated_url'], '/course-finder/results/')
        get_page.assert_called_once()
        self.assertEqual(get_page.call_args.args[0], 'cy')
        self.assertEqual(get_page.call_args.args[1].model, CourseFinderResults)


@tag('azure')
@override_settings(SEARCH_API_BASE_URL='https://search.example/api/', SEARCH_API_TIMEOUT=3)
class CourseSearchApiEndpointTests(SimpleTestCase):
    url = '/course-finder/search/v2/api/courses/nested'

    def setUp(self):
        self.upstream_request = Mock()
        session = Mock(request=self.upstream_request)
        session_patcher = patch.object(api, '_session', session)
        session_patcher.start()
        self.addCleanup(session_patcher.stop)

    def test_get_forwards_path_query_and_selected_headers_and_returns_response(self):
        upstream_request = self.upstream_request
        upstream_request.return_value = Mock(
            content=b'{"results": []}',
            status_code=206,
            headers={
                'Content-Type': 'application/json',
                'Cache-Control': 'max-age=60',
                'ETag': 'search-result',
                'Last-Modified': 'Mon, 01 Jan 2024 00:00:00 GMT',
                'Set-Cookie': 'not-forwarded=true',
            },
        )

        response = self.client.get(
            self.url + '?query=biology&tag=one&tag=two',
            HTTP_ACCEPT='application/json',
            HTTP_ACCEPT_LANGUAGE='cy',
            HTTP_AUTHORIZATION='not-forwarded',
        )

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.content, b'{"results": []}')
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response['Cache-Control'], 'max-age=60')
        self.assertEqual(response['ETag'], 'search-result')
        self.assertEqual(response['Last-Modified'], 'Mon, 01 Jan 2024 00:00:00 GMT')
        self.assertNotIn('Set-Cookie', response)
        call = upstream_request.call_args
        self.assertEqual(call.kwargs['method'], 'GET')
        self.assertEqual(call.kwargs['url'], 'https://search.example/api/courses/nested')
        self.assertEqual(call.kwargs['params'].getlist('tag'), ['one', 'two'])
        self.assertEqual(call.kwargs['params']['query'], 'biology')
        self.assertIsNone(call.kwargs['data'])
        self.assertEqual(call.kwargs['headers'], {
            'Accept': 'application/json',
            'Accept-Language': 'cy',
        })
        self.assertEqual(call.kwargs['timeout'], 3)
        self.assertFalse(call.kwargs['allow_redirects'])

    def test_post_forwards_body_and_content_type(self):
        upstream_request = self.upstream_request
        upstream_request.return_value = Mock(content=b'ok', status_code=201, headers={})
        body = b'{"query":"biology"}'

        response = self.client.post(
            self.url,
            data=body,
            content_type='application/json',
            HTTP_ACCEPT='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'ok')
        call = upstream_request.call_args.kwargs
        self.assertEqual(call['method'], 'POST')
        self.assertEqual(call['data'], body)
        self.assertEqual(call['headers'], {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

    def test_rejects_invalid_proxy_path_without_requesting_upstream(self):
        upstream_request = self.upstream_request
        request = RequestFactory().get('/course-finder/search/v2/api/invalid')

        response = api_proxy(request, '../private')

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'Invalid path'})
        upstream_request.assert_not_called()

    def test_rejects_oversized_post_body_without_requesting_upstream(self):
        upstream_request = self.upstream_request
        response = self.client.post(
            self.url,
            data=b'x' * (MAX_BODY_BYTES + 1),
            content_type='application/octet-stream',
        )

        self.assertEqual(response.status_code, 413)
        self.assertJSONEqual(response.content, {'error': 'Request body too large'})
        upstream_request.assert_not_called()

    def test_rejects_unsupported_methods(self):
        upstream_request = self.upstream_request
        response = self.client.put(self.url, data=b'ignored')

        self.assertEqual(response.status_code, 405)
        upstream_request.assert_not_called()

    def test_returns_gateway_timeout_when_upstream_times_out(self):
        upstream_request = self.upstream_request
        upstream_request.side_effect = requests.Timeout
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 504)
        self.assertJSONEqual(response.content, {'error': 'Upstream timed out'})
        upstream_request.assert_called_once()

    def test_returns_bad_gateway_when_upstream_is_unavailable(self):
        upstream_request = self.upstream_request
        upstream_request.side_effect = requests.ConnectionError
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 502)
        self.assertJSONEqual(response.content, {'error': 'Upstream unavailable'})
        upstream_request.assert_called_once()