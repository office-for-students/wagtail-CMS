from django.db import models
from django.db.models.fields import TextField
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


# Create your models here.
class ContentLandingPage(Page):
    options = StreamField([
        ('option', blocks.TextBlock())
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('options', classname="full")
    ]

class Section(Page):
    subsections = StreamField([
        ('subsection', blocks.RichTextBlock(features=['h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed']))
    ])
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock()),
    ])
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', blocks.PageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('subsections', classname="full"),
        FieldPanel('related_links_title', classname="full"),
        StreamFieldPanel('related_links', classname="full"),
        FieldPanel('lateral_link_title', classname="full"),
        StreamFieldPanel('lateral_links', classname="full")
    ]
