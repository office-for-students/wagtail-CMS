import logging

from core.models import DiscoverUniBasePage
from django.db.models.fields import TextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField

logger = logging.getLogger(__name__)

STUDENT_SATISFACTION_KEY = 'student_satisfaction'
ENTRY_INFO_KEY = 'entry_information'
AFTER_ONE_YEAR_KEY = 'after_one_year'
EARNINGS_AFTER_COURSE_KEY = 'earnings_after_the_course'
EMPLOYMENT_AFTER_COURSE_KEY = 'employment_after_the_course'
ACCREDITATION_KEY = 'professional_accreditation'

# New accordion section ('Graduate Perceptions) added; various sections of this file are affected.
# TODO: In order for the new accordion section to be rendered in the UI, an instance of the corresponding
#   accordion panel must be created in the Wagtail admin site (http://0.0.0.0:8000/admin/);
#   go to Pages > Home > Course Details > 'ACCORDIONS' section > Add (+ icon) > add a panel of the new type.
#   Then Save Draft, then Publish.
GRADUATE_PERCEPTIONS_KEY = 'graduate_perceptions'
LINKS_TO_THE_INSTITUTION_WEBSITE_KEY = 'links_to_the_institution_website'


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)


class SatisfactionDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return STUDENT_SATISFACTION_KEY


class EntryInfoDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ENTRY_INFO_KEY


class AfterOneYearDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return AFTER_ONE_YEAR_KEY


class EarningsAfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return EARNINGS_AFTER_COURSE_KEY


class EmploymentAfterCourseDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return EMPLOYMENT_AFTER_COURSE_KEY


class AccreditationDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return ACCREDITATION_KEY


class GraduatePerceptionsDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return GRADUATE_PERCEPTIONS_KEY


class LinksToTheInstitutionWebsiteDataSet(blocks.StructValue):
    @staticmethod
    def data_set():
        return LINKS_TO_THE_INSTITUTION_WEBSITE_KEY


class SatisfactionBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)
    teaching_stats_header = blocks.CharBlock(required=False)
    learning_opportunities_stats_header = blocks.CharBlock(required=False)
    assessment_stats_header = blocks.CharBlock(required=False)
    support_stats_header = blocks.CharBlock(required=False)
    organisation_stats_header = blocks.CharBlock(required=False)
    learning_resources_stats_header = blocks.CharBlock(required=False)
    learning_community_stats_header = blocks.CharBlock(required=False)
    student_voice_stats_header = blocks.CharBlock(required=False)
    nhs_placement_stats_header = blocks.CharBlock(required=False)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = SatisfactionDataSet


class EntryInformationBlock(AccordionPanel):
    qualification_heading = blocks.CharBlock(required=False)
    qualification_intro = blocks.CharBlock(required=False)
    qualification_label_explanation_heading = blocks.CharBlock(required=False)
    qualification_label_explanation_body = blocks.RichTextBlock(blank=True)
    qualification_data_source = blocks.RichTextBlock(blank=True)

    tariffs_heading = blocks.CharBlock(required=False)
    tariffs_intro = blocks.CharBlock(required=False)
    tariffs_data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EntryInfoDataSet


class AfterOneYearBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.CharBlock(required=False)
    lead = blocks.CharBlock(required=False)
    label_explanation_heading = blocks.CharBlock(required=False)
    label_explanation_body = blocks.RichTextBlock(blank=True)
    data_source = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = AfterOneYearDataSet


class EarningsAfterCourseBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)
    intro = blocks.RichTextBlock(blank=True)

    average_earnings_inst_heading = blocks.RichTextBlock(blank=True)
    institution_graduates_heading = blocks.RichTextBlock(blank=True)

    after_fifteen_months_earnings_heading = blocks.CharBlock(required=False)
    after_fifteen_months_range_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_respondents_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_no_of_graduates_explanation = blocks.RichTextBlock(blank=True)
    after_fifteen_months_data_source = blocks.RichTextBlock(blank=True)
    leo_respondents_explanation = blocks.RichTextBlock(blank=True)

    after_three_years_earnings_heading = blocks.CharBlock(required=False)
    after_five_years_earnings_heading = blocks.CharBlock(required=False)
    after_three_five_years_data_source = blocks.RichTextBlock(blank=True)

    average_earnings_sector_heading = blocks.RichTextBlock(blank=True)
    # respondents_live_in_explanation_go = blocks.RichTextBlock(blank=True)
    # respondents_live_in_explanation_leo = blocks.RichTextBlock(blank=True)
    respondents_live_in_explanation = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EarningsAfterCourseDataSet


class EmploymentAfterCourseBlock(AccordionPanel):
    six_month_employment_lead = blocks.CharBlock(required=False)
    six_month_employment_data_source = blocks.RichTextBlock(blank=True)

    section_heading = blocks.RichTextBlock(required=False)
    intro = blocks.CharBlock(blank=True)

    six_month_employment_roles_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_label_explanation_heading = blocks.CharBlock(required=False)
    six_month_employment_roles_data_source = blocks.RichTextBlock(blank=True)

    occupation_types_label_explanation_heading = blocks.CharBlock(required=False)
    occupation_types_label_explanation_body = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = EmploymentAfterCourseDataSet


class AccreditationBlock(AccordionPanel):
    section_heading = blocks.CharBlock(required=False)

    class Meta:
        value_class = AccreditationDataSet


class GraduatePerceptionsBlock(AccordionPanel):
    lead_text = blocks.CharBlock(required=False)
    intro_body = blocks.RichTextBlock(blank=True)

    perception_of_work_heading = blocks.CharBlock(required=False)
    data_source = blocks.RichTextBlock(blank=True)

    usefulness_explanation_heading = blocks.CharBlock(required=False)
    usefulness_explanation = blocks.RichTextBlock(blank=True)

    meaningfulness_explanation_heading = blocks.CharBlock(required=False)
    meaningfulness_explanation = blocks.RichTextBlock(blank=True)

    future_explanation_heading = blocks.CharBlock(required=False)
    future_explanation = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = GraduatePerceptionsDataSet


class LinksToTheInstitutionWebsiteBlock(AccordionPanel):
    course_information_on_website_header = blocks.RichTextBlock(blank=True)

    class Meta:
        value_class = LinksToTheInstitutionWebsiteDataSet


class CourseDetailPage(DiscoverUniBasePage):
    accordions = StreamField([
        ('satisfaction_panel', SatisfactionBlock(required=True, icon='collapse-down')),
        ('entry_information_panel', EntryInformationBlock(required=True, icon='collapse-down')),
        ('after_one_year_panel', AfterOneYearBlock(required=True, icon='collapse-down')),
        ('accreditation_panel', AccreditationBlock(required=True, icon='collapse-down')),
        ('earningsafter_course_panel', EarningsAfterCourseBlock(required=True, icon='collapse-down')),
        ('employment_after_course_panel', EmploymentAfterCourseBlock(required=True, icon='collapse-down')),
        ('graduate_perceptions_panel', GraduatePerceptionsBlock(required=True, icon='collapse-down')),
        ('links_to_the_institution_website_panel',
         LinksToTheInstitutionWebsiteBlock(required=True, icon='collapse-down'))
    ], use_json_field=True)
    uni_site_links_header = TextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('accordions'),
        FieldPanel('uni_site_links_header'),
    ]


class CourseComparisonPage(DiscoverUniBasePage):
    heading = TextField(blank=True)
    lead = TextField(blank=True)
    remove_text = RichTextField(blank=True)
    save_text = RichTextField(blank=True)
    compare_heading = TextField(blank=True)
    accordions = StreamField([
        ('satisfaction_panel', SatisfactionBlock(required=True, icon='collapse-down')),
        ('entry_information_panel', EntryInformationBlock(required=True, icon='collapse-down')),
        ('after_one_year_panel', AfterOneYearBlock(required=True, icon='collapse-down')),
        ('accreditation_panel', AccreditationBlock(required=True, icon='collapse-down')),
        ('earningsafter_course_panel', EarningsAfterCourseBlock(required=True, icon='collapse-down')),
        ('employment_after_course_panel', EmploymentAfterCourseBlock(required=True, icon='collapse-down')),
        ('graduate_perceptions_panel', GraduatePerceptionsBlock(required=True, icon='collapse-down')),
        ('links_to_the_institution_website_panel',
         LinksToTheInstitutionWebsiteBlock(required=True, icon='collapse-down'))
    ], use_json_field=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        FieldPanel('remove_text'),
        FieldPanel('save_text'),
        FieldPanel('compare_heading'),
        FieldPanel('accordions'),
    ]


class CourseManagePage(DiscoverUniBasePage):
    heading = TextField(blank=True)
    lead = TextField(blank=True)
    save_text = RichTextField(blank=True)
    compare_text = RichTextField(blank=True)
    none_selected_text = RichTextField(blank=True)
    one_selected_text = RichTextField(blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('lead'),
        FieldPanel('save_text'),
        FieldPanel('compare_text'),
        FieldPanel('none_selected_text'),
        FieldPanel('one_selected_text'),
    ]
