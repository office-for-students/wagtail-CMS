from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    header_title = RichTextField(blank=True)
    header_subtitle = RichTextField(blank=True)
    info_headline = RichTextField(blank=True)
    info_points = RichTextField(blank=True)
    help_title = RichTextField(blank=True)
    help_text = RichTextField(blank=True)
    find_title = RichTextField(blank=True)
    find_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_title', classname="full"),
        FieldPanel('header_subtitle', classname="full"),
        FieldPanel('info_headline', classname="full"),
        FieldPanel('info_points', classname="full"),
        FieldPanel('help_title', classname="full"),
        FieldPanel('help_text', classname="full"),
        FieldPanel('find_title', classname="full"),
        FieldPanel('find_text', classname="full"),
    ]
