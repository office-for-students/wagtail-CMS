from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet

from CMS.enums import enums
from core.utils import parse_menu_item, get_page_for_language, get_current_version


class DiscoverUniBasePage(Page):
    translated_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('translated_page'),
    ]

    def get_language(self):
        if self.url and '/cy/' in self.url:
            return 'cy'
        return 'en'

    def is_english(self):
        return self.get_language() == 'en'

    def is_welsh(self):
        return self.get_language() == 'cy'

    def get_english_url(self):
        from home.models import HomePage
        if self.is_english():
            return self.url
        return self.translated_page.url if self.translated_page \
            else get_page_for_language(enums.languages.ENGLISH, HomePage.objects.all()).url

    def get_welsh_url(self):
        from home.models import HomePage
        if self.is_english():
            return self.translated_page.url if self.translated_page \
                else get_page_for_language(enums.languages.WELSH, HomePage.objects.all()).url
        return self.url

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

    @property
    def footer(self):
        footer_name = enums.languages_map.get(self.get_language()).capitalize()
        footer_data = Footer.objects.filter(name=footer_name).first()
        if not footer_data:
            footer_name = enums.languages_map.get(enums.languages.ENGLISH).capitalize()
            footer_data = Footer.objects.filter(name=footer_name).first()
        footer = []
        if footer_data:
            for item in footer_data.footer_items:
                footer.append(parse_menu_item(item))
        return footer

    class Meta:
        abstract = True

    def manage_link(self):
        from courses.models import CourseManagePage
        bookmark_page = get_page_for_language(self.get_language(), CourseManagePage.objects.all())
        return bookmark_page.url

    def get_context(self, request):
        context = super().get_context(request)
        context['page'] = self
        context['english_url'] = self.get_english_url()
        context['welsh_url'] = self.get_welsh_url()
        context['cookies_accepted'] = request.COOKIES.get('discoverUniCookies')
        context['load_error'] = request.GET.get('load_error', '')
        context['error_type'] = request.GET.get('error_type', '')
        return context


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


@register_snippet
class Footer(models.Model):
    name = models.CharField(max_length=255)
    footer_items = StreamField([
        ('footer_item', SimpleMenuItem()),
    ])

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('footer_items')
    ]

    def __str__(self):
        return self.name
