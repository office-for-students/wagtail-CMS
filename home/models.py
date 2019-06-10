from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


class HomePage(Page):
    header = RichTextField(blank=True, features=['h1'])
    subtitle = RichTextField(blank=True)
    page_links = StreamField([
        ('link', blocks.StructBlock([
            ('page', blocks.PageChooserBlock()),
            ('title', blocks.CharBlock()),
            ('subtitle', blocks.CharBlock())
        ]))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('subtitle', classname="full"),
        StreamFieldPanel('page_links', classname="full")
    ]
