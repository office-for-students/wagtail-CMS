from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class InstitutionDetailPage(Page):
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


class Institution:

    def __init__(self, data_obj):
        self.pub_ukprn_name = data_obj.get('pub_ukprn_name').title()
        self.pub_ukprn = data_obj.get('pub_ukprn')
        self.ukprn_name = data_obj.get('ukprn_name')
        self.ukprn = data_obj.get('ukprn')
