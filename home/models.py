from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.db.models.fields import TextField

from core.models import DiscoverUniBasePage


NAV_ICON_OPTIONS = (
    ('magnify_glass', 'Magnify glass'),
    ('info', "Info 'i'"),
    ('institution', 'Institution'),
    ('payment', 'Payment'),
    ('clipboard', 'Clipboard'),
)


class NavPanel(blocks.StructBlock):
    link = blocks.PageChooserBlock()
    icon = blocks.ChoiceBlock(choices=NAV_ICON_OPTIONS,
                              default='standard',
                              label="Variant",
                              classname='dct-meta-field')
    label = blocks.RichTextBlock()
    button_text = blocks.CharBlock(required=False)
    button_description = blocks.CharBlock(required=False)


class HomePage(DiscoverUniBasePage):

    header = TextField(blank=True)
    intro = RichTextField(blank=True)
    course_wizard_link = TextField(blank=True)
    box_1_title = TextField(blank=True)
    box_1_content = TextField(blank=True)
    box_1_link = TextField(blank=True)
    box_2_title = TextField(blank=True)
    box_2_content = TextField(blank=True)
    box_2_link = TextField(blank=True)
    box_3_link = TextField(blank=True)
    page_links = StreamField([
        ('link', blocks.StructBlock([
            ('page', blocks.PageChooserBlock()),
            ('title', blocks.CharBlock())
        ]))
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('intro', classname="full"),
        FieldPanel('course_wizard_link', classname="full"),
        FieldPanel('box_1_title', classname="full"),
        FieldPanel('box_1_content', classname="full"),
        FieldPanel('box_1_link', classname="full"),
        FieldPanel('box_2_title', classname="full"),
        FieldPanel('box_2_content', classname="full"),
        FieldPanel('box_2_link', classname="full"),
        FieldPanel('box_3_link', classname="full"),
        StreamFieldPanel('page_links', classname="full"),
    ]


class UserNavPage(DiscoverUniBasePage):

    header = TextField()
    nav_panels = StreamField([
        ('nav_panel', NavPanel(required=True, icon='link')),
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        StreamFieldPanel('nav_panels', classname="full"),
    ]
