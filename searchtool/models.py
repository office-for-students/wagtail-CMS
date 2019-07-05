from django.db.models.fields import TextField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


class SearchTool(Page):
    pass


class WhereToStudy(Page):
    header = RichTextField(blank=True)
    options = StreamField([
        ('option', blocks.TextBlock())
    ])
    help_decide = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('options', classname="full"),
        FieldPanel('help_decide', classname="full")
    ]


class ChooseAUni(Page):
    header = RichTextField(blank=True)
    placeholder = TextField(blank=True)
    button = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('placeholder', classname="full"),
        FieldPanel('button', classname="full")
    ]


class WhatToStudy(Page):
    header = RichTextField(blank=True)
    placeholder = TextField(blank=True)
    button = TextField(blank=True)
    button_two = TextField(blank=True)
    help_decide = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('placeholder', classname="full"),
        FieldPanel('button', classname="full"),
        FieldPanel('button_two', classname="full"),
        FieldPanel('help_decide', classname="full")
    ]


class HowToStudy(Page):
    header = RichTextField(blank=True)
    options = StreamField([
        ('option', blocks.TextBlock(blank=True))
    ])
    button = TextField(blank=True)
    help_decide = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('options', classname="full"),
        FieldPanel('button', classname="full"),
        FieldPanel('help_decide', classname="full")
    ]


class ChooseALocation(Page):
    header = RichTextField(blank=True)
    tab_headings = StreamField([
        ('heading', blocks.TextBlock())
    ])
    country_options = StreamField([
        ('option', blocks.TextBlock(blank=True))
    ])
    tab_two_header = RichTextField(blank=True)
    tab_two_placeholder = TextField(blank=True)
    tab_three_header = RichTextField(blank=True)
    tab_three_placeholder = TextField(blank=True)
    button = TextField(blank=True)
    help_decide = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('tab_headings', classname="full"),
        StreamFieldPanel('country_options', classname="full"),
        FieldPanel('tab_two_header', classname="full"),
        FieldPanel('tab_two_placeholder', classname="full"),
        FieldPanel('tab_three_header', classname="full"),
        FieldPanel('tab_three_placeholder', classname="full"),
        FieldPanel('button', classname="full"),
        FieldPanel('help_decide', classname="full")
    ]
