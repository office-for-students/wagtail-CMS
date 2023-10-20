import json
import requests

from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField

from CMS.enums import enums
from CMS.translations import term_for_key
from core.models import DiscoverUniBasePage
from core.request_handler import get_json_file
from errors.models import ApiError
from institutions import request_handler
from institutions.utils import load_institution_json


class InstitutionList:

    def get_latest_version():
        response = get_json_file("version.json")

        if response.ok:
            return response.json()["version"]
        else:
            return ""

    @staticmethod
    def get_options():
        response = get_json_file("version.json")

        if response.ok:
            version = response.json()["version"]
        else:
            version = ""

        if version != InstitutionList.version:
            InstitutionList.options = load_institution_json()

        return InstitutionList.options

    version = get_latest_version()
    options = load_institution_json()


class InstitutionDetailPage(DiscoverUniBasePage):
    qa_heading = TextField(blank=True)
    qa_body = RichTextField(blank=True)
    qa_report_link = TextField(blank=True)
    qa_explanation_link = TextField(blank=True)
    qa_explanation_heading = TextField(blank=True)
    qa_explanation_body = RichTextField(blank=True)
    tef_heading = TextField(blank=True)
    tef_gold_body = RichTextField(blank=True)
    tef_silver_body = RichTextField(blank=True)
    tef_bronze_body = RichTextField(blank=True)
    tef_provisional_body = RichTextField(blank=True)
    tef_not_participated_body = RichTextField(blank=True)
    tef_withdrawn_body = RichTextField(blank=True)
    tef_report_link = TextField(blank=True)
    tef_explanation_link = TextField(blank=True)
    tef_explanation_heading = TextField(blank=True)
    tef_explanation_body = RichTextField(blank=True)
    apr_heading = TextField(blank=True)
    apr_met_body = RichTextField(blank=True)
    apr_action_plan_body = RichTextField(blank=True)
    apr_pending_body = RichTextField(blank=True)
    apr_not_met_body = RichTextField(blank=True)
    apr_explanation_link = TextField(blank=True)
    apr_explanation_heading = TextField(blank=True)
    apr_explanation_body = RichTextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('qa_heading'),
        FieldPanel('qa_body'),
        FieldPanel('qa_report_link'),
        FieldPanel('qa_explanation_link'),
        FieldPanel('qa_explanation_heading'),
        FieldPanel('qa_explanation_body'),
        FieldPanel('tef_heading'),
        FieldPanel('tef_gold_body'),
        FieldPanel('tef_silver_body'),
        FieldPanel('tef_bronze_body'),
        FieldPanel('tef_provisional_body'),
        FieldPanel('tef_not_participated_body'),
        FieldPanel('tef_withdrawn_body'),
        FieldPanel('tef_report_link'),
        FieldPanel('tef_explanation_link'),
        FieldPanel('tef_explanation_heading'),
        FieldPanel('tef_explanation_body'),
        FieldPanel('apr_heading'),
        FieldPanel('apr_met_body'),
        FieldPanel('apr_action_plan_body'),
        FieldPanel('apr_pending_body'),
        FieldPanel('apr_not_met_body'),
        FieldPanel('apr_explanation_link'),
        FieldPanel('apr_explanation_heading'),
        FieldPanel('apr_explanation_body'),
    ]


class InstitutionOverview:

    def __init__(self, data_obj, language):
        self.pub_ukprn_name = data_obj.get('pub_ukprn_name') if language == enums.languages.ENGLISH else data_obj.get('pub_ukprn_welsh_name')
        self.ukprn_name = data_obj.get('ukprn_name') if language == enums.languages.ENGLISH else data_obj.get('ukprn_welsh_name')
        self.pub_ukprn = data_obj.get('pub_ukprn')
        self.ukprn = data_obj.get('ukprn')


class Institution:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.id = data_obj.get('_id')
        self.created_at = data_obj.get('created_at')
        institution_data = data_obj.get('institution')
        if institution_data:
            self.apr_outcome = institution_data.get('apr_outcome')
            self.pub_ukprn_country_code = institution_data.get("pub_ukprn_country").get('code')
            self.pub_ukprn_country_name = institution_data.get("pub_ukprn_country").get('name')
            self.pub_ukprn_name = institution_data.get("pub_ukprn_name") if language == enums.languages.ENGLISH else institution_data.get("pub_ukprn_welsh_name")
            self.pub_ukprn = institution_data.get("pub_ukprn")
            self.website = institution_data.get('links').get('institution_homepage') if institution_data.get('links') else None
            self.tef_outcome = institution_data.get("tef_outcome")
            self.total_number_of_courses = institution_data.get("total_number_of_courses")
            self.ukprn_country = institution_data.get("ukprn_country")
            self.ukprn_name = institution_data.get("ukprn_name") if language == enums.languages.ENGLISH else institution_data.get("ukprn_welsh_name")
            self.ukprn = institution_data.get("ukprn")
            self.qaa_url = institution_data.get("qaa_url")
            self.qaa_report_type = institution_data.get("qaa_report_type")
            self.qaa_report_type_string = None
            if self.pub_ukprn_country_name == "Wales":
                if not self.qaa_report_type:
                    self.qaa_report_type_string = term_for_key("qaa_report_type_blank", language)
                elif self.qaa_report_type == "Gateway Quality Review (Wales)":
                    self.qaa_report_type_string = term_for_key("gateway_quality_review_wales", language)
                elif self.qaa_report_type == "Quality Enhancement Review":
                    self.qaa_report_type_string = term_for_key("quality_enhancement_review", language)
            elif self.pub_ukprn_country_name == "Scotland":
                self.qaa_report_type_string = term_for_key("more_about_qaa_scotland", language)
            else:
                self.qaa_report_type_string = term_for_key("ni_previous_model", language)
            if 'contact_details' in institution_data:
                self.contact_details = InstitutionContactDetails(institution_data.get('contact_details'))

            self.student_unions = []
            if 'student_unions' in institution_data:
                for union in institution_data.get('student_unions'):
                    self.student_unions.append(InstitutionStudentUnions(union, self.display_language))

    @property
    def is_irish(self):
        return self.pub_ukprn_country_code == enums.countries.IRELAND

    @property
    def is_english(self):
        return self.pub_ukprn_country_code == enums.countries.ENGLAND

    @property
    def is_scottish(self):
        return self.pub_ukprn_country_code == enums.countries.SCOTLAND

    @property
    def is_welsh(self):
        return self.pub_ukprn_country_code == enums.countries.WALES

    def show_qa_report_link(self):
        return self.is_scottish or self.is_welsh

    @property
    def apr_is_met(self):
        return self.apr_outcome and self.apr_outcome == enums.apr_values.MET

    @property
    def apr_is_action_plan(self):
        return self.apr_outcome and self.apr_outcome == enums.apr_values.ACTION_PLAN

    @property
    def apr_is_pending(self):
        return self.apr_outcome and self.apr_outcome == enums.apr_values.PENDING

    @property
    def apr_is_not_met(self):
        return self.apr_outcome and self.apr_outcome == enums.apr_values.NOT_MET

    @property
    def tef_is_gold(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.GOLD

    @property
    def tef_is_silver(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.SILVER

    @property
    def tef_is_bronze(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.BRONZE

    @property
    def tef_is_provisional(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.PROVISIONAL

    @property
    def tef_is_not_participate(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.NOT_PARTICIPATE

    @property
    def tef_is_withdrawn(self):
        return self.tef_outcome and self.tef_outcome == enums.tef_values.WITHDRAWN

    def show_tef_logo(self):
        return self.tef_is_gold or self.tef_is_silver or self.tef_is_bronze

    @classmethod
    def find(cls, institution_id, language):
        institution = None
        error       = None

        response = request_handler.load_institution_data(institution_id)

        if type(response) == requests.models.Response:
            if response.ok:
                institution = cls(response.json(), language)
            else:
                error = ApiError(response.status_code, 'Loading institution %s failed' % institution_id)
        elif type(response) == dict:
            institution = cls(response, language)
            if institution is None:
                error = ApiError(None, 'Institution %s does not exist in MongoDB' % institution_id)

        return institution, error


class InstitutionContactDetails:

    def __init__(self, contact_data):
        self.address = contact_data.get('address')
        self.phone_number = contact_data.get('telephone')


class InstitutionStudentUnions:

    def __init__(self, su_data, language):
        self.display_language = language
        self.english_name = ''
        self.welsh_name = ''
        self.english_website = ''
        self.welsh_website = ''

        name_data = su_data.get('name')
        link_data = su_data.get('link')

        if name_data:
            self.english_name = name_data.get('english','')
            self.welsh_name = name_data.get('welsh', '')

        if link_data:
            self.english_website = link_data.get('english', '')
            self.welsh_website = link_data.get('welsh', '')

    def display_name(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_name if self.english_name else self.welsh_name
        return self.welsh_name if self.welsh_name else self.english_name

    def display_url(self):
        if self.display_language == enums.languages.ENGLISH:
            return self.english_website if self.english_website else self.welsh_website
        return self.welsh_website if self.welsh_website else self.english_website
