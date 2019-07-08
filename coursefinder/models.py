from django.db.models.fields import TextField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from coursefinder import request_handler
from errors.models import ApiError


class CourseFinderLandingPage(Page):
    header = TextField(blank=True)
    subheader = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('subheader', classname="full")
    ]


class CourseFinderChooseCountry(Page):
    page_order = 1
    question = TextField(blank=True)
    next_section = StreamField([
        ('section', blocks.PageChooserBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full"),
        StreamFieldPanel('next_section', classname="full")
    ]


class CourseFinderModeOfStudy(Page):
    page_order = 2
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]


class CourseFinderChooseSubject(Page):
    page_order = 3
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]


class CourseFinderNarrowSearch(Page):
    page_order = 4
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]


class CourseFinderTownCity(Page):
    page_order = 5
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]


class CourseFinderUni(Page):
    page_order = 6
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]


class CourseFinderPostcode(Page):
    page_order = 7
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]


class CourseFinderSummary(Page):
    page_order = 8
    header = TextField(blank=True)
    country_section_title = TextField(blank=True)
    mode_of_study_section_title = TextField(blank=True)
    subjects_section_title = TextField(blank=True)
    narrow_by_section_title = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('country_section_title', classname="full"),
        FieldPanel('mode_of_study_section_title', classname="full"),
        FieldPanel('subjects_section_title', classname="full"),
        FieldPanel('narrow_by_section_title', classname="full")
    ]


class CourseFinderResults(Page):
    page_order = 9
    header = TextField(blank=True)
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('related_links_title'),
        StreamFieldPanel('related_links', classname="full"),
    ]


class CourseSearch:

    def __init__(self, course_query, institution_query):
        self.course_query = course_query
        self.institution_query = institution_query
        self.total_courses = None
        self.total_institutions = None
        self.results = None

    def execute(self):
        response = request_handler.query_course_and_institution(self.course_query, self.institution_query)
        error = None

        if response.ok:
            data = response.json()
            self.total_courses = data.get('total_number_of_courses')
            self.total_institutions = data.get('total_results')
            self.results = data.get('items')
        else:
            error = ApiError(response.status_code, 'searching courses for %s %s' %
                             (self.institution_query, self.course_query))

        return error
