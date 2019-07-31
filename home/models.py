from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.db.models.fields import TextField

from core.models import DiscoverUniBasePage


class HomePage(DiscoverUniBasePage):

    header = RichTextField(blank=True, features=['h1'])
    page_links = StreamField([
        ('link', blocks.StructBlock([
            ('page', blocks.PageChooserBlock()),
            ('title', blocks.CharBlock())
        ]))
    ])
    search_header = RichTextField(blank=True, features=['h1'])
    course_field_label = TextField(blank=True)
    institution_field_label = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('page_links', classname="full"),
        FieldPanel('search_header', classname="full"),
        FieldPanel('course_field_label', classname="full"),
        FieldPanel('institution_field_label', classname="full"),
    ]
