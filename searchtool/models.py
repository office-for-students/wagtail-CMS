from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

# Create your models here.

class SearchTool(Page):
    pass

class WhereToStudy(Page):
    header = RichTextField(blank=True)
    options = StreamField([
        ('option', blocks.TextBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('options', classname="full")
    ]
