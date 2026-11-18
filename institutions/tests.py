import copy
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import SimpleTestCase, TestCase, tag
from django.urls import resolve

from CMS.enums import enums
from CMS.test.utils import UniSimpleTestCase
from errors.models import ApiError
from institutions import request_handler
from institutions import utils as institution_utils
from institutions import views as institution_views
from institutions.models import Institution, InstitutionStudentUnions
from institutions.test_files.institution_mocks import InstitutionMocks
from institutions.views import institution_detail


@tag('azure')
class InstitutionsModelsTests(UniSimpleTestCase):

    @patch('institutions.request_handler.load_institution_data',
           return_value=InstitutionMocks.get_unsuccessful_institution_load_response())
    def test_institution_find_returns_api_error_if_institution_not_found(self, mock_response):
        institution, error = Institution.find('10002718', 'en')

        self.assertIsNone(institution)
        self.assertIsInstance(error, ApiError)
        self.assertEqual(error.status_code, 500)
        mock_response.assert_called_once_with('10002718')

    @patch('institutions.request_handler.load_institution_data',
           return_value=InstitutionMocks.get_successful_institution_load_response())
    def test_institution_find_returns_institution_for_successful_response(self, load_institution_data):
        institution, error = Institution.find('10002718', 'en')

        self.assertIsInstance(institution, Institution)
        self.assertIsNone(error)
        self.assertEqual(institution.pub_ukprn_name, 'Goldsmiths, University of London')
        load_institution_data.assert_called_once_with('10002718')

    @patch('institutions.request_handler.load_institution_data', return_value=InstitutionMocks.get_successful_institution_load_content())
    def test_institution_find_accepts_dictionary_response(self, load_institution_data):
        institution, error = Institution.find('10002718', 'cy')

        self.assertIsInstance(institution, Institution)
        self.assertIsNone(error)
        self.assertEqual(institution.display_language, 'cy')
        load_institution_data.assert_called_once_with('10002718')

    def test_institution_uses_country_specific_qaa_strings(self):
        cases = (
            ('Wales', None, 'qaa_report_type_blank'),
            ('Wales', 'Gateway Quality Review (Wales)', 'gateway_quality_review_wales'),
            ('Wales', 'Quality Enhancement Review', 'quality_enhancement_review'),
            ('Scotland', None, 'more_about_qaa_scotland'),
            ('England', None, 'ni_previous_model'),
        )

        for country, report_type, key in cases:
            with self.subTest(country=country, report_type=report_type), \
                    patch('institutions.models.term_for_key', return_value=key) as term_for_key:
                data = copy.deepcopy(InstitutionMocks.get_successful_institution_load_content())
                data['institution']['pub_ukprn_country']['name'] = country
                data['institution']['qaa_report_type'] = report_type

                institution = Institution(data, 'en')

                self.assertEqual(institution.qaa_report_type_string, key)
                term_for_key.assert_called_once_with(key, 'en')

    def test_institution_tef_and_apr_flags_reflect_outcomes(self):
        data = copy.deepcopy(InstitutionMocks.get_successful_institution_load_content())
        institution_data = data['institution']
        institution_data['apr_outcome'] = enums.apr_values.MET
        institution_data['tef_outcome'] = enums.tef_values.GOLD
        institution = Institution(data, 'en')

        self.assertTrue(institution.apr_is_met)
        self.assertFalse(institution.apr_is_action_plan)
        self.assertTrue(institution.tef_is_gold)
        self.assertTrue(institution.show_tef_logo())

        institution_data['apr_outcome'] = enums.apr_values.ACTION_PLAN
        institution_data['tef_outcome'] = enums.tef_values.SILVER
        institution = Institution(data, 'en')
        self.assertTrue(institution.apr_is_action_plan)
        self.assertTrue(institution.tef_is_silver)

        institution_data['apr_outcome'] = enums.apr_values.PENDING
        institution_data['tef_outcome'] = enums.tef_values.BRONZE
        institution = Institution(data, 'en')
        self.assertTrue(institution.apr_is_pending)
        self.assertTrue(institution.tef_is_bronze)

        institution_data['apr_outcome'] = enums.apr_values.NOT_MET
        institution_data['tef_outcome'] = enums.tef_values.PROVISIONAL
        institution = Institution(data, 'en')
        self.assertTrue(institution.apr_is_not_met)
        self.assertTrue(institution.tef_is_provisional)

        institution_data['tef_outcome'] = enums.tef_values.WITHDRAWN
        institution = Institution(data, 'en')
        self.assertTrue(institution.tef_is_withdrawn)

    def test_student_union_display_falls_back_to_available_language(self):
        union = InstitutionStudentUnions({
            'name': {'english': 'Students Union', 'welsh': ''},
            'link': {'english': 'https://union.example', 'welsh': ''},
        }, 'cy')

        self.assertEqual(union.display_name(), 'Students Union')
        self.assertEqual(union.display_url(), 'https://union.example')


@tag('azure')
class InstitutionRequestHandlerTests(SimpleTestCase):

    @patch('institutions.request_handler.requests.get')
    def test_load_institution_data_formats_url_and_subscription_header(self, get):
        with patch('institutions.request_handler.settings.DATASETAPIHOST', 'https://dataset.example'), \
                patch('institutions.request_handler.settings.DATASETAPIKEY', 'test-api-key-not-real'):
            request_handler.load_institution_data('10002718')

        get.assert_called_once_with(
            url='https://dataset.example/institutions/10002718',
            headers={'Ocp-Apim-Subscription-Key': 'test-api-key-not-real'},
            timeout=(3.05, 10),
        )


@tag('azure')
class InstitutionJsonTests(SimpleTestCase):

    @patch('institutions.utils.get_json_file')
    def test_load_institution_json_deduplicates_names_and_handles_failures(self, get_json_file):
        successful = Mock(ok=True)
        successful.json.return_value = [
            {'name': 'College A', 'id': 1},
            {'name': 'College A', 'id': 2},
            {'name': 'College B', 'id': 3},
        ]
        failed = Mock(ok=False)
        failed.json.return_value = [{'name': 'Unavailable', 'id': 4}]
        get_json_file.side_effect = [successful, failed]

        institutions = institution_utils.load_institution_json()

        self.assertEqual(institutions['en'], [
            {'name': 'College A', 'id': 1},
            {'name': 'College B', 'id': 3},
        ])
        self.assertEqual(institutions['cy'], {})
        self.assertEqual(get_json_file.call_count, 2)


@tag('azure')
class InstitutionEndpointTests(TestCase):

    def test_institution_details_url_resolves_to_its_view(self):
        resolved = resolve('/institution-details/123/')

        self.assertIs(resolved.func, institution_detail)

    @patch('institutions.views.Institution.find', return_value=(None, Mock(status_code=404)))
    def test_failed_institution_lookup_redirects_to_language_landing_page(self, find):
        response = self.client.get('/cy/institution-details/123/')

        self.assertRedirects(response, '/cy/?load_error=true&error_type=0', fetch_redirect_response=False)
        find.assert_called_once_with('123', 'cy')

    @patch('institutions.views.render', return_value=HttpResponse('not found', status=404))
    @patch('institutions.views.get_page_for_language', return_value=None)
    @patch('institutions.views.Institution.find', return_value=(Mock(), None))
    def test_missing_institution_page_renders_404(self, find, get_page, render):
        response = self.client.get('/institution-details/123/')

        self.assertEqual(response.status_code, 404)
        render.assert_called_once_with(response.wsgi_request, '404.html')
        get_page.assert_called_once()
        find.assert_called_once_with('123', 'en')

    @patch('institutions.views.term_for_key', return_value='Courses: {}')
    @patch('institutions.views.render', return_value=HttpResponse('institution'))
    @patch('institutions.views.generate_tef_context', return_value={'status': 'tef'})
    @patch('institutions.views.get_page_for_language')
    @patch('institutions.views.Institution.find')
    def test_successful_institution_detail_renders_context_and_translated_url(
        self, find, get_page, generate_tef_context, render, term_for_key
    ):
        institution = Mock(pub_ukprn_name='College A', total_number_of_courses=30)
        find.return_value = institution, None
        page = Mock(tef_report_link='Report for {{institution_name}}')
        page.get_context.return_value = {'existing': 'value'}
        get_page.return_value = page

        response = self.client.get('/institution-details/123/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(page.tef_report_link, 'Report for College A')
        context = render.call_args.args[2]
        self.assertIs(context['page'], page)
        self.assertIs(context['institution'], institution)
        self.assertEqual(context['translated_url'], '/cy/institution-details/123/')
        self.assertEqual(context['totals_string'], 'Courses: 30')
        generate_tef_context.assert_called_once()
        term_for_key.assert_called_once_with('courses_at_this_uni', language='en')


@tag('azure')
class InstitutionViewHelperTests(SimpleTestCase):

    def test_tef_status_for_english_and_non_english_institutions(self):
        institution = Mock(pub_ukprn_country_code='XF', tef_outcome=[{'id': 1}])
        self.assertEqual(institution_views.get_tef_status(institution), 'affiliated')

        institution.tef_outcome = None
        self.assertEqual(institution_views.get_tef_status(institution), 'no_tef')

        institution.tef_outcome = {'overall_rating': 'Pending'}
        self.assertEqual(institution_views.get_tef_status(institution), 'pending')

        institution.tef_outcome = {'overall_rating': 'Bronze'}
        self.assertEqual(institution_views.get_tef_status(institution), 'tef')

        institution.pub_ukprn_country_code = 'XI'
        self.assertEqual(institution_views.get_tef_status(institution), 'XI')

    def test_tef_image_uses_special_png_for_bronze_silver_bronze(self):
        path, alt_text = institution_views.get_tef_image('Bronze', 'Silver', 'Bronze')

        self.assertEqual(path, 'images/tef_images/bronze_silver_bronze.png')
        self.assertIn('Overall Rating: Bronze', alt_text)
        self.assertTrue(institution_views.get_tef_image('Gold', 'Silver', 'Bronze')[0].endswith('.svg'))

    def test_logo_path_maps_country_and_tef_statuses(self):
        institution = Mock(tef_outcome={
            'overall_rating': 'Gold',
            'student_experience_rating': 'Silver',
            'student_outcomes_rating': 'Bronze',
        })

        self.assertEqual(institution_views.get_logo_path(institution, 'tef')[0], 'images/tef_images/gold_silver_bronze.svg')
        self.assertEqual(institution_views.get_logo_path(institution, 'pending')[0], 'images/tef_logo.svg')
        self.assertEqual(institution_views.get_logo_path(institution, 'XI')[0], 'images/medr.svg')
        self.assertEqual(institution_views.get_logo_path(institution, 'XH')[0], 'images/sfc.svg')
        self.assertEqual(institution_views.get_logo_path(institution, 'XG')[0], 'images/department_of_economy_logo.svg')

    @patch('institutions.views.term_for_key', side_effect=lambda key, **kwargs: '{0} {1}' if key == 'tef_affiliate_left' else ' and ')
    def test_create_affiliate_copy_formats_one_two_and_three_affiliates(self, term_for_key):
        for count in (1, 2, 3):
            affiliates = [{'name': f'College {index}', 'du_url': f'/institution/{index}/'} for index in range(count)]

            with self.subTest(count=count):
                result = institution_views.create_affiliate_copy(Mock(), 'en', affiliates, 'Parent College')

                self.assertIn('Parent College', result)
                self.assertEqual(result.count('<a '), count)

    @patch('institutions.views.Institution.find')
    @patch('institutions.views.term_for_key', return_value='translated')
    def test_generate_tef_context_loads_and_links_affiliate_institutions(self, term_for_key, find):
        institution = Mock(
            pub_ukprn_name='Parent College',
            tef_outcome=[{'report_ukprn': '1001'}],
        )
        affiliate = Mock(pub_ukprn_name='Affiliate College')
        find.return_value = affiliate, None

        context = institution_views.generate_tef_context(institution, 'en', 'affiliated')

        self.assertTrue(context['jms'])
        self.assertEqual(context['affiliates'][0]['name'], 'Affiliate College')
        self.assertEqual(context['affiliates'][0]['du_url'], '/institution-details/1001/')
        find.assert_called_once_with('1001', 'en')