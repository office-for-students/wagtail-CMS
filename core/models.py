from urllib.parse import urlparse

from django.apps import apps
from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    PageChooserPanel,
)
from wagtail.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.fields import StreamField
from wagtail.models import Page

from CMS.enums import enums
from core import utils
from core.utils import get_page_for_language


class DiscoverUniBasePage(Page):
    class Meta:
        abstract = True

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
        return self.translated_page.url if self.translated_page else get_page_for_language(
            language,
            self.__class__.objects.all(),
        ).url

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
        context['load_error'] = request.GET.get('load_error', '')
        context['error_type'] = request.GET.get('error_type', '')
        return context

    def _get_translation(self):
        """Return the linked page from either direction, or None."""
        if self.translated_page_id:
            return self.translated_page

        # Reverse lookup: the FK lives on each concrete subclass,
        # so check them all for a page pointing at this one.
        for model in apps.get_models():
            if issubclass(model, DiscoverUniBasePage) and not model._meta.abstract:
                match = model.objects.filter(translated_page=self.pk).first()
                if match:
                    return match
        return None

    def get_sitemap_urls(self, request=None):
        urls = super().get_sitemap_urls(request=request)
        if not urls:
            return urls

        translation = self._get_translation()
        if translation is None or not translation.live:
            return urls

        this_url = self.get_full_url(request)
        translated_url = translation.get_full_url(request)
        if not this_url or not translated_url:
            return urls

        this_is_welsh = urlparse(this_url).path.startswith("/cy/")
        en_url, cy_url = (translated_url, this_url) if this_is_welsh else (this_url, translated_url)

        urls[0]["alternates"] = [
            {
                "lang_code": "en",
                "location": en_url,
            },
            {
                "lang_code": "cy",
                "location": cy_url,
            },
            {
                "lang_code": "x-default",
                "location": en_url,
            },
        ]
        return urls


class SimpleMenuItem(StructBlock):
    label = CharBlock(required=False, help_text='Leave blank to use the page name')
    link_page = PageChooserBlock(required=False)

    class Meta:
        icon = 'link'


class MultiMenuItem(StructBlock):
    label = CharBlock(required=True)
    menu_items = StreamBlock(
        [
            ('simple_menu_item', SimpleMenuItem()),
        ], icon='arrow-left', label='Items',
    )


class Menu(models.Model):
    name = models.CharField(max_length=255)
    menu_items = StreamField(
        [
            ('simple_menu_item', SimpleMenuItem()),
            ('multi_menu_item', MultiMenuItem()),
        ],
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('menu_items'),
    ]

    def __str__(self):
        return self.name


class Footer(models.Model):
    name = models.CharField(max_length=255)
    footer_items = StreamField(
        [
            ('footer_item', SimpleMenuItem()),
        ],
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('footer_items'),
    ]

    def __str__(self):
        return self.name
