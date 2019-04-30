from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    header = RichTextField(blank=True)
    left_CTA = RichTextField(blank=True)
    right_CTA = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('left_CTA', classname="full"),
        FieldPanel('right_CTA', classname="full"),
    ]
