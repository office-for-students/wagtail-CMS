from django.db import models
from django.db.models.fields import TextField

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

# Create your models here.

class CourseFinderLandingPage(Page):
    header = TextField(blank=True)
    subheader = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('subheader', classname="full")
    ]

class CourseFinderChooseCountry(Page):
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]

class CourseFinderModeOfStudy(Page):
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]

class CourseFinderChooseSubject(Page):
    question = TextField(blank=True)
    helper_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full"),
        FieldPanel('helper_text', classname="full")
    ]

class CourseFinderNarrowSearch(Page):
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]

class CourseFinderTownCity(Page):
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]

class CourseFinderUni(Page):
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]

class CourseFinderPostcode(Page):
    question = TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('question', classname="full")
    ]
