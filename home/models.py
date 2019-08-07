from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.db.models.fields import TextField

from core.models import DiscoverUniBasePage


class HomePage(DiscoverUniBasePage):

    header = TextField(blank=True)
    intro = RichTextField(blank=True)
    page_links = StreamField([
        ('link', blocks.StructBlock([
            ('page', blocks.PageChooserBlock()),
            ('title', blocks.CharBlock())
        ]))
    ])

    content_panels = Page.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('intro', classname="full"),
        StreamFieldPanel('page_links', classname="full"),
    ]
