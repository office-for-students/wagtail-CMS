from django.db.models.fields import TextField
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import CharBlock
from wagtail.blocks import ChoiceBlock
from wagtail.blocks import PageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.blocks import StructBlock
from wagtail.fields import RichTextField
from wagtail.fields import StreamField

from CMS import translations
from CMS.settings.base import APPLICATION_VERSION
from core.models import DiscoverUniBasePage
from institutions.models import InstitutionList

NAV_ICON_OPTIONS = (
    ('magnify_glass', 'Magnify glass'),
    ('info', "Info 'i'"),
    ('institution', 'Institution'),
    ('payment', 'Payment'),
    ('clipboard', 'Clipboard'),
)


class NavPanel(StructBlock):
    link = PageChooserBlock()
    icon = ChoiceBlock(choices=NAV_ICON_OPTIONS,
                       default='standard',
                       label="Variant",
                       classname='dct-meta-field')
    label = RichTextBlock()
    button_text = CharBlock(required=False)
    button_description = CharBlock(required=False)


class HomePage(DiscoverUniBasePage):
    header = TextField(blank=True)
    intro = RichTextField(blank=True)
    informational_title = TextField(blank=True)
    informational_text = TextField(blank=True)
    informational_text_link = TextField(blank=True)
    course_wizard_link = TextField(blank=True)
    box_1_title = TextField(blank=True)
    box_1_content = TextField(blank=True)
    box_1_link = TextField(blank=True)
    box_2_title = TextField(blank=True)
    box_2_content = TextField(blank=True)
    box_2_link = TextField(blank=True)
    box_3_title = TextField(blank=True)
    box_3_content = TextField(blank=True)
    box_3_link = TextField(blank=True)
    page_links = StreamField([
        ('link', StructBlock([
            ('page', PageChooserBlock()),
            ('title', CharBlock())
        ]))
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('intro', classname="full"),
        FieldPanel('informational_title', classname="full"),
        FieldPanel('informational_text', classname="full"),
        FieldPanel('informational_text_link', classname="full"),
        FieldPanel('course_wizard_link', classname="full"),
        FieldPanel('box_1_title', classname="full"),
        FieldPanel('box_1_content', classname="full"),
        FieldPanel('box_1_link', classname="full"),
        FieldPanel('box_2_title', classname="full"),
        FieldPanel('box_2_content', classname="full"),
        FieldPanel('box_2_link', classname="full"),
        FieldPanel('box_3_title', classname="full"),
        FieldPanel('box_3_content', classname="full"),
        FieldPanel('box_3_link', classname="full"),
        FieldPanel('page_links', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        language = self.get_language()
        context['institutions_list'] = InstitutionList.get_options()[language]
        context['language'] = language
        context['search_info'] = {
            'institutions': "",
            'number_options_selected': translations.term_for_key('number_options_selected', language),
            'institution_name': translations.term_for_key('institution_name', language),
            'select_all_results': translations.term_for_key('select_all_results', language),
            'select_all_institutions': translations.term_for_key('select_all_institutions', language)
        }
        context['version'] = APPLICATION_VERSION
        return context


class UserNavPage(DiscoverUniBasePage):
    header = TextField()
    nav_panels = StreamField([
        ('nav_panel', NavPanel(required=True, icon='link')),
    ])

    content_panels = DiscoverUniBasePage.content_panels + [
        FieldPanel('header', classname="full"),
        FieldPanel('nav_panels', classname="full"),
    ]
