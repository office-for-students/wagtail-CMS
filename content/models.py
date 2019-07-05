from django.db.models.fields import TextField
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from content import request_handler


class ContentLandingPage(Page):
    options = StreamField([
        ('sections', blocks.PageChooserBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('options', classname="full")
    ]


class Section(Page):
    subsections = StreamField([
        ('subsection', blocks.StructBlock([
            ('subsection_title', blocks.TextBlock()),
            ('subsection_content', blocks.RichTextBlock())
        ]))
    ])
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('subsections'),
        FieldPanel('related_links_title'),
        StreamFieldPanel('related_links'),
        FieldPanel('lateral_link_title'),
        StreamFieldPanel('lateral_links')
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

        if response.ok:
            data = response.json()
            self.total_courses = data.get('total_number_of_courses')
            self.total_institutions = data.get('total_results')
            self.results = data.get('items')
        else:
            # handle error
            pass
