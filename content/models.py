from core.models import DiscoverUniBasePage
from django.db.models.fields import TextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField


class ContentLandingPage(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    options = StreamField([
        ('sections', blocks.PageChooserBlock())
    ], use_json_field=True)

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('intro'),
        FieldPanel('options', classname="full")
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]


class Section(DiscoverUniBasePage):
    intro = RichTextField(blank=True)
    subsections = StreamField([
        ('subsection', blocks.StructBlock([
            ('subsection_title', blocks.TextBlock()),
            ('subsection_content',
             blocks.RichTextBlock(features=['h3', 'h4', 'bold', 'underline', 'italic', 'embed', 'link',
                                            'image', 'ol', 'ul', 'hr', 'blockquote']))
        ]))
    ], use_json_field=True)
    related_links_title = TextField(blank=True)
    related_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], use_json_field=True, blank=True)
    lateral_link_title = TextField(blank=True)
    lateral_links = StreamField([
        ('links', blocks.PageChooserBlock(required=False)),
    ], use_json_field=True, blank=True)

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
    content_body = RichTextField(blank=True, features=['h1', 'h2', 'h3', 'bold', 'italic', 'embed', 'link',
                                                       'document-link', 'image', 'ol', 'ul', 'hr'])
    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('content_body'),
    ]

    def get_breadcrumbs(self):
        return self.get_ancestors().live()[1:]
