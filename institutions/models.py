from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from CMS.enums import enums
from core.models import DiscoverUniBasePage
from errors.models import ApiError
from institutions import request_handler


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

    def __init__(self, data_obj):
        self.pub_ukprn_name = data_obj.get('pub_ukprn_name')
        self.pub_ukprn = data_obj.get('pub_ukprn')
        self.ukprn_name = data_obj.get('ukprn_name')
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
            self.pub_ukprn_name = institution_data.get("pub_ukprn_name")
            self.pub_ukprn = institution_data.get("pub_ukprn")
            self.website = institution_data.get('links').get('institution_homepage')
            self.tef_outcome = institution_data.get("tef_outcome")
            self.total_number_of_courses = institution_data.get("total_number_of_courses")
            self.ukprn_country = institution_data.get("ukprn_country")
            self.ukprn_name = institution_data.get("ukprn_name")
            self.ukprn = institution_data.get("ukprn")

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
        error = None

        response = request_handler.load_institution_data(institution_id)

        if response.ok:
            institution = cls(response.json(), language)
        else:
            error = ApiError(response.status_code, 'Loading details for institution %s ' % institution_id)

        return institution, error


class InstitutionContactDetails:

    def __init__(self, contact_data):
        address = contact_data.get('address')
        if address:
            self.address_1 = address.get('line_1')
            self.address_2 = address.get('line_2')
            self.address_3 = address.get('line_3')
            self.address_4 = address.get('line_4')
            self.town = address.get('town')
            self.county = address.get('county')
            self.postcode = address.get('post_code')
        self.phone_number = contact_data.get('telephone')

    @property
    def address(self):
        address_arr = filter(None, [self.address_1, self.address_2, self.address_3, self.address_4,
                             self.town, self.county, self.postcode])
        return ', '.join(address_arr)


class InstitutionStudentUnions:

    def __init__(self, su_data, language):
        self.display_language = language
        self.english_website = su_data.get('link').get('english')
        self.welsh_website = su_data.get('link').get('welsh')
        self.english_name = su_data.get('name').get('english')
        self.welsh_name = su_data.get('name').get('welsh')

    def display_name(self):
        return self.english_name if self.display_language == enums.languages.ENGLISH else self.welsh_name

    def display_url(self):
        return self.english_website if self.display_language == enums.languages.ENGLISH else self.welsh_website
