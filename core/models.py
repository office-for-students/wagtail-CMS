from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import PageChooserPanel
from wagtail.blocks import CharBlock
from wagtail.blocks import PageChooserBlock
from wagtail.blocks import StreamBlock
from wagtail.blocks import StructBlock
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from CMS.enums import enums
from core import utils
from core.utils import get_page_for_language


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
        return utils.get_language(self.url)

    def is_english(self):
        return self.get_language() == enums.languages.ENGLISH

    def url_for_language(self):
        language = enums.languages.WELSH if self.is_english() else enums.languages.ENGLISH
        return self.translated_page.url if self.translated_page else get_page_for_language(language,
                                                                                           self.__class__.objects.all()).url

    class Meta:
        abstract = True

    def manage_link(self):
        from courses.models import CourseManagePage
        bookmark_page = get_page_for_language(self.get_language(), CourseManagePage.objects.all())
        if not bookmark_page:
            return '#'
        return bookmark_page.url

    def get_context(self, request):
        context = super().get_context(request)
        context['page'] = self
        context['translated_url'] = self.url_for_language()
        context['cookies_accepted'] = request.COOKIES.get('discoverUniCookies')
        context['load_error'] = request.GET.get('load_error', '')
        context['error_type'] = request.GET.get('error_type', '')
        return context


class SimpleMenuItem(StructBlock):
    label = CharBlock(required=False, help_text='Leave blank to use the page name')
    link_page = PageChooserBlock(required=False)

    class Meta:
        icon = 'link'


class MultiMenuItem(StructBlock):
    label = CharBlock(required=True)
    menu_items = StreamBlock([
        ('simple_menu_item', SimpleMenuItem())
    ], icon='arrow-left', label='Items')


class Menu(models.Model):
    name = models.CharField(max_length=255)
    menu_items = StreamField([
        ('simple_menu_item', SimpleMenuItem()),
        ('multi_menu_item', MultiMenuItem())
    ])

    panels = [
        FieldPanel('name'),
        FieldPanel('menu_items')
    ]

    def __str__(self):
        return self.name


class Footer(models.Model):
    name = models.CharField(max_length=255)
    footer_items = StreamField([
        ('footer_item', SimpleMenuItem()),
    ])

    panels = [
        FieldPanel('name'),
        FieldPanel('footer_items')
    ]

    def __str__(self):
        return self.name
