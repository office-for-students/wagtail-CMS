from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet

from CMS.enums import enums
from core.utils import parse_menu_item


class DiscoverUniBasePage(Page):

    def get_language(self):
        if '/cy/' in self.get_full_url():
            return 'cy'
        return 'en'

    def is_english(self):
        return self.get_language() == 'en'

    @property
    def menu(self):
        menu_name = enums.languages_map.get(self.get_language()).capitalize()
        menu_data = Menu.objects.filter(name=menu_name).first()
        if not menu_data:
            menu_name = enums.languages_map.get(enums.languages.ENGLISH).capitalize()
            menu_data = Menu.objects.filter(name=menu_name).first()
        menu = []
        if menu_data:
            for item in menu_data.menu_items:
                menu.append(parse_menu_item(item))
        return menu

    class Meta:
        abstract = True


class SimpleMenuItem(blocks.StructBlock):
    label = blocks.CharBlock(required=False, help_text='Leave blank to use the page name')
    link_page = blocks.PageChooserBlock(required=False)

    class Meta:
        icon = 'link'


class MultiMenuItem(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    menu_items = blocks.StreamBlock([
        ('simple_menu_item', SimpleMenuItem())
    ], icon='arrow-left', label='Items')


@register_snippet
class Menu(models.Model):
    name = models.CharField(max_length=255)
    menu_items = StreamField([
        ('simple_menu_item', SimpleMenuItem()),
        ('multi_menu_item', MultiMenuItem())
    ])

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('menu_items')
    ]

    def __str__(self):
        return self.name
