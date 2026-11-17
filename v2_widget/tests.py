from unittest.mock import patch

import requests
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, tag
from django.urls import resolve

from v2_widget import views as widget_views


@tag('azure')
class WidgetUrlRoutingTests(SimpleTestCase):

    def test_widget_routes_resolve_for_each_configured_prefix(self):
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
            for suffix, expected_view in widget_routes:
                url = prefix + suffix
                with self.subTest(url=url):
                    self.assertIs(resolve(url).func, expected_view)


@tag('azure')
class WidgetViewTests(SimpleTestCase):

    @patch('v2_widget.views.requests.get')
    def test_proxy_forwards_query_parameters_user_agent_and_timeout(self, get):
        get.return_value = MockResponse(b'widget', 206, {'Content-Type': 'text/html; charset=utf-8'})
        request = RequestFactory().get('/proxy/?q=biology&page=2', HTTP_USER_AGENT='test-browser')

        response = widget_views.proxy_content(request, 'https://widget.example/endpoint')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.content, b'widget')
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        get.assert_called_once_with(
            'https://widget.example/endpoint',
            params={'q': 'biology', 'page': '2'},
            headers={'User-Agent': 'test-browser'},
            timeout=10,
        )

    @patch('v2_widget.views.requests.get')
    def test_proxy_uses_default_content_type_when_upstream_omits_it(self, get):
        get.return_value = MockResponse(b'[]', 200, {})
        request = RequestFactory().get('/')

        response = widget_views.proxy_content(request, 'https://widget.example/api')

        self.assertEqual(response['Content-Type'], 'text/html')

    def test_proxy_rejects_non_get_methods(self):
        request = RequestFactory().post('/')

        response = widget_views.proxy_content(request, 'https://widget.example/endpoint')

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.content, b'Method not allowed')

    @patch('v2_widget.views.requests.get')
    @patch('v2_widget.views.render', return_value=HttpResponse('configurator'))
    def test_configurator_renders_its_template(self, render, get):
        response = self.client.get('/v2/widget/configurator/')

        self.assertEqual(response.content, b'configurator')
        render.assert_called_once_with(
            request=render.call_args.kwargs['request'],
            template_name='v2_widget/configurator.html',
            context={},
        )
        get.assert_not_called()

    @patch('v2_widget.views.WIDGET_HOST', 'https://widget.example/')
    @patch('v2_widget.views.requests.get')
    def test_embed_builds_widget_target_url(self, get):
        get.return_value = MockResponse(b'embedded', 200, {'Content-Type': 'text/html'})

        response = self.client.get('/v2/widget/123/biology/full/en', HTTP_USER_AGENT='test-browser')

        self.assertEqual(response.content, b'embedded')
        self.assertEqual(get.call_args.args[0], 'https://widget.example/widget/v2/123/biology/full/en')

    @patch('v2_widget.views.WIDGET_HOST', 'https://widget.example/')
    @patch('v2_widget.views.requests.get')
    def test_placeholder_builds_widget_target_url(self, get):
        get.return_value = MockResponse(b'placeholder', 200, {'Content-Type': 'text/html'})

        response = self.client.get('/v2/widget/placeholder/en')

        self.assertEqual(response.content, b'placeholder')
        self.assertEqual(get.call_args.args[0], 'https://widget.example/widget/v2/placeholder/en')

    @patch('v2_widget.views.WIDGET_HOST', 'https://widget.example/')
    @patch('v2_widget.views.requests.get')
    def test_api_views_build_json_target_urls(self, get):
        get.return_value = MockResponse(b'[]', 200, {})

        all_institutions = self.client.get('/v2/widget/api/all_institutions/')
        institution_courses = self.client.get('/v2/widget/api/institution/123/courses')

        self.assertEqual(all_institutions['Content-Type'], 'application/json')
        self.assertEqual(institution_courses['Content-Type'], 'application/json')
        self.assertEqual(get.call_args_list[0].args[0], 'https://widget.example/api/all_institutions/')
        self.assertEqual(get.call_args_list[1].args[0], 'https://widget.example/api/institution/123/courses')

    @patch('v2_widget.views.requests.get', side_effect=requests.exceptions.Timeout('timeout'))
    def test_all_proxy_views_convert_upstream_failures_to_bad_gateway(self, get):
        urls = (
            '/v2/widget/123/biology/full/en',
            '/v2/widget/placeholder/en',
            '/v2/widget/api/all_institutions/',
            '/v2/widget/api/institution/123/courses',
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 502)
                self.assertIn(b'Error:', response.content)


class MockResponse:
    def __init__(self, content, status_code, headers):
        self.content = content
        self.status_code = status_code
        self.headers = headers