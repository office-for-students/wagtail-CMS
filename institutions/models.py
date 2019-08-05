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
    tef_report_link = TextField(blank=True)
    tef_explanation_link = TextField(blank=True)
    tef_explanation_heading = TextField(blank=True)
    tef_explanation_body = RichTextField(blank=True)
    apr_heading = TextField(blank=True)
    apr_body = RichTextField(blank=True)
    apr_explanation_link = TextField(blank=True)
    apr_explanation_heading = TextField(blank=True)
    apr_explanation_body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('qa_heading'),
        FieldPanel('qa_body'),
        FieldPanel('qa_report_link'),
        FieldPanel('qa_explanation_link'),
        FieldPanel('qa_explanation_heading'),
        FieldPanel('qa_explanation_body'),
        FieldPanel('tef_heading'),
        FieldPanel('tef_report_link'),
        FieldPanel('tef_explanation_link'),
        FieldPanel('tef_explanation_heading'),
        FieldPanel('tef_explanation_body'),
        FieldPanel('apr_heading'),
        FieldPanel('apr_body'),
        FieldPanel('apr_explanation_link'),
        FieldPanel('apr_explanation_heading'),
        FieldPanel('apr_explanation_body'),
    ]


class InstitutionOverview:

    def __init__(self, data_obj):
        self.pub_ukprn_name = data_obj.get('pub_ukprn_name').title()
        self.pub_ukprn = data_obj.get('pub_ukprn')
        self.ukprn_name = data_obj.get('ukprn_name')
        self.ukprn = data_obj.get('ukprn')


class Institution:

    def __init__(self, data_obj, language):
        self.display_language = language
        self.id = data_obj.get('_id')
        self.created_at = data_obj.get('created_at')
        institution_data = data_obj.get('institution')
        self.apr_outcome = institution_data.get('apr_outcome')
        self.contact_details = InstitutionContactDetails(institution_data.get('contact_details'))
        self.pub_ukprn_country = institution_data.get("pub_ukprn_country")
        self.pub_ukprn_name = institution_data.get("pub_ukprn_name")
        self.pub_ukprn = institution_data.get("pub_ukprn")
        self.website = institution_data.get('links').get('institution_homepage')
        self.tef_outcome = institution_data.get("tef_outcome").lower()
        self.total_number_of_courses = institution_data.get("total_number_of_courses")
        self.ukprn_country = institution_data.get("ukprn_country")
        self.ukprn_name = institution_data.get("ukprn_name")
        self.ukprn = institution_data.get("ukprn")
        self.student_unions = []
        for union in institution_data.get('student_unions'):
            self.student_unions.append(InstitutionStudentUnions(union, self.display_language))

    @property
    def is_irish(self):
        return self.pub_ukprn_country == 'Ireland'

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
