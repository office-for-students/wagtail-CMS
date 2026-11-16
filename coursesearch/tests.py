from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.template.loader import get_template
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings, tag

from core.models import DiscoverUniBasePage
from coursesearch import models as coursefinder_models
from coursesearch import utils as coursefinder_utils
from coursesearch.models import (
    CourseFinderChooseCountry,
    CourseFinderChooseSubject,
    CourseFinderModeOfStudy,
    CourseFinderNarrowSearch,
    CourseFinderPostcode,
    CourseFinderResults,
    CourseFinderSummary,
    CourseFinderUni,
)
from coursesearch.views import course_finder_results_new
from institutions.models import InstitutionList


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

    def test_language_select_uses_requested_language_without_a_page(self):
        navigation = {
            'brand_logo': {'url': '/', 'img': 'logo.svg'},
            'comp_menu': [],
            'primary_menu': [],
        }

        def render_nav(request, template_name, context):
            # Render without context processors: they query CMS pages, which SimpleTestCase forbids.
            nav_context = {**context, 'navigation': navigation, 'request': request}
            return HttpResponse(get_template('partials/nav.html').render(nav_context))

        test_cases = (
            ('/course-finder/results/', 'en', 'Cymraeg', '/cy/course-finder/results/'),
            ('/cy/course-finder/results/', 'cy', 'English', '/course-finder/results/'),
        )
        with (
            patch('coursesearch.views.get_page_for_language', return_value=None),
            patch('coursesearch.views.render', side_effect=render_nav),
            patch('core.templatetags.discover_uni_tags.translations.term_for_key', return_value='Site logo'),
        ):
            for url, language, expected_label, expected_url in test_cases:
                with self.subTest(url=url):
                    request = RequestFactory().get(url)
                    response = course_finder_results_new(request, language=language)
                    content = response.content.decode()
                    language_select = content.split('class="nav__primary-link language-select"', 1)[1].split('</a>', 1)[0]

                    self.assertIn(expected_label, language_select)
                    self.assertIn(f'href="{expected_url}?"', language_select)


@tag('azure')
class CourseFinderSiblingTests(TestCase):

    finder_cases = (
        (coursefinder_utils.choose_country_sibling_finder, CourseFinderChooseCountry, True),
        (coursefinder_utils.mode_of_study_sibling_finder, CourseFinderModeOfStudy, False),
        (coursefinder_utils.choose_subject_sibling_finder, CourseFinderChooseSubject, False),
        (coursefinder_utils.narrow_search_sibling_finder, CourseFinderNarrowSearch, False),
        (coursefinder_utils.postcode_sibling_finder, CourseFinderPostcode, False),
        (coursefinder_utils.summary_sibling_finder, CourseFinderSummary, False),
        (coursefinder_utils.results_sibling_finder, CourseFinderResults, False),
    )

    def test_each_sibling_finder_handles_none_one_and_duplicate_matches(self):
        for finder, page_type, takes_list in self.finder_cases:
            with self.subTest(page_type=page_type.__name__), patch('coursesearch.utils.InternalError') as internal_error:
                page = Mock()
                siblings = []
                page.get_siblings.return_value.specific.return_value = siblings

                self.assertIsNone(self._invoke_finder(finder, page, siblings, takes_list))
                internal_error.assert_called_once()

                first_match = page_type()
                self.assertIs(self._invoke_finder(finder, page, [first_match], takes_list), first_match)
                self.assertEqual(internal_error.call_count, 1)

                second_match = page_type()
                self.assertIs(self._invoke_finder(finder, page, [first_match, second_match], takes_list), first_match)
                self.assertEqual(internal_error.call_count, 2)

    @staticmethod
    def _invoke_finder(finder, page, siblings, takes_list):
        if takes_list:
            return finder(siblings)
        return CourseFinderSiblingTests._find_for_page(finder, page, siblings)

    @staticmethod
    def _find_for_page(finder, page, siblings):
        page.get_siblings.return_value.specific.return_value = siblings
        return finder(page)


@tag('azure')
class CourseFinderModelTests(TestCase):

    def test_navigation_properties_delegate_to_their_sibling_finders(self):
        properties = (
            (CourseFinderChooseCountry, 'next_page', 'mode_of_study_sibling_finder', False),
            (CourseFinderModeOfStudy, 'next_page', 'choose_subject_sibling_finder', False),
            (CourseFinderModeOfStudy, 'back_page', 'choose_country_sibling_finder', True),
            (CourseFinderChooseSubject, 'next_page', 'narrow_search_sibling_finder', False),
            (CourseFinderChooseSubject, 'back_page', 'mode_of_study_sibling_finder', False),
            (CourseFinderNarrowSearch, 'back_page', 'choose_subject_sibling_finder', False),
            (CourseFinderUni, 'next_page', 'summary_sibling_finder', False),
            (CourseFinderUni, 'back_page', 'narrow_search_sibling_finder', False),
            (CourseFinderPostcode, 'next_page', 'summary_sibling_finder', False),
            (CourseFinderPostcode, 'back_page', 'narrow_search_sibling_finder', False),
            (CourseFinderSummary, 'next_page', 'results_sibling_finder', False),
            (CourseFinderSummary, 'back_page', 'narrow_search_sibling_finder', False),
        )
        expected = object()

        for model, property_name, finder_name, uses_siblings in properties:
            with self.subTest(model=model.__name__, property_name=property_name):
                page = model()
                expected_argument = page
                if uses_siblings:
                    siblings = Mock()
                    siblings.specific.return_value = expected
                    page.get_siblings = Mock(return_value=siblings)
                    expected_argument = expected

                with patch.object(coursefinder_models, finder_name, return_value=expected) as finder:
                    self.assertIs(getattr(page, property_name), expected)
                    finder.assert_called_once_with(expected_argument)

    def test_results_search_url_is_language_aware(self):
        page = CourseFinderResults()

        with patch.object(page, 'get_language', return_value='en'):
            self.assertEqual(page.get_search_url(), '/course-finder/results/')
        with patch.object(page, 'get_language', return_value='cy'):
            self.assertEqual(page.get_search_url(), '/cy/course-finder/results/')

    @patch.object(InstitutionList, 'get_options', return_value={'en': [], 'cy': []})
    @patch.object(coursefinder_models, 'get_page_for_language')
    @patch.object(CourseFinderChooseCountry.objects, 'all', return_value=[])
    @patch.object(DiscoverUniBasePage, 'get_context', return_value={'base': True})
    def test_results_context_adds_search_and_course_finder_urls(
        self, get_context, all_choose_country_pages, get_page, get_options
    ):
        selected_page = Mock(url='/en/course-finder/')
        get_page.return_value = selected_page
        page = CourseFinderResults()
        with patch.object(page, 'get_language', return_value='en'):
            context = page.get_context(Mock())

        self.assertTrue(context['base'])
        self.assertEqual(context['search_url'], '/course-finder/results/')
        self.assertEqual(context['course_finder_url'], '/en/course-finder/')
        self.assertEqual(context['institutions_list'], [])
        get_context.assert_called_once()
        all_choose_country_pages.assert_called_once_with()
        get_page.assert_called_once_with('en', all_choose_country_pages.return_value)
        get_options.assert_called_once_with()

