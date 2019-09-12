from django.db.models.fields import TextField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from core.models import DiscoverUniBasePage


class ContentLandingPage(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    options = StreamField([
        ('sections', blocks.PageChooserBlock())
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('options', classname="full")
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]


class Section(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    subsections = StreamField([
        ('subsection', blocks.StructBlock([
            ('subsection_title', blocks.TextBlock()),
            ('subsection_content', blocks.RichTextBlock(features=['h3', 'h4', 'bold', 'italic', 'embed', 'link',
                                                        'document-link', 'image', 'ol', 'ul', 'hr', 'blockquote']))
        ]))
    ])
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('intro'),
        StreamFieldPanel('subsections'),
        FieldPanel('related_links_title'),
        StreamFieldPanel('related_links'),
        FieldPanel('lateral_link_title'),
        StreamFieldPanel('lateral_links')
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]


class FlatContent(DiscoverUniBasePage):
    content_body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'bold', 'italic', 'embed', 'link',
                                                       'document-link', 'image', 'ol', 'ul', 'hr'])
    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('content_body'),
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]
