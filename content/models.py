from django.db.models.fields import TextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import PageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.blocks import StructBlock
from wagtail.blocks import TextBlock
from wagtail.fields import RichTextField
from wagtail.fields import StreamField

from core.models import DiscoverUniBasePage


class ContentLandingPage(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    options = StreamField([
        ('sections', PageChooserBlock())
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('options', classname="full")
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]


class Section(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    subsections = StreamField([
        ('subsection', StructBlock([
            ('subsection_title', TextBlock()),
            ('subsection_content',
             RichTextBlock(features=['h3', 'h4', 'bold', 'underline', 'italic', 'embed', 'link', 'document-link',
                                     'image', 'ol', 'ul', 'hr', 'blockquote']))
        ]))
    ])
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', PageChooserBlock(required=False)),
    ], blank=True)
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', PageChooserBlock(required=False)),
    ], blank=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('subsections'),
        FieldPanel('related_links_title'),
        FieldPanel('related_links'),
        FieldPanel('lateral_link_title'),
        FieldPanel('lateral_links')
    ]

    @property
    def has_lateral_links(self):
        return self.lateral_links or self.lateral_link_title

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]


class FlatContent(DiscoverUniBasePage):
    content_body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'bold', 'italic', 'underline', 'embed', 'link',
                                                       'document-link', 'image', 'ol', 'ul', 'hr'])
    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('content_body'),
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]
