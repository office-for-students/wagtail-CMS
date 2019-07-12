from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core import blocks


DATA_SET_KEYS = (
    ('student_satisfaction', 'Student satisfaction'),
    ('entry_information', 'Entry information'),
    ('after_one_year', 'After 1 year of study'),
    ('after_the_course', 'After the course'),
    ('professional_accreditation', 'Professional accreditation'),
)


class AccordionPanel(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    data_set = blocks.ChoiceBlock(choices=DATA_SET_KEYS,
                                  default='standard')


class CourseDetailPage(Page):
    accordions = StreamField([
        ('accordion_panel', AccordionPanel(required=True, icon='collapse-down'))
    ])
    uni_site_links_header = TextField(blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('accordions'),
        FieldPanel('uni_site_links_header'),
    ]
