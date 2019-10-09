from django.utils.html import escape

from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from wagtail.core import hooks
from wagtail.core.rich_text import LinkHandler

from .models import Menu, Footer


class MenuAdmin(ModelAdmin):

    model = Menu
    menu_label = 'Menu'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class FooterAdmin(ModelAdmin):

    model = Footer
    menu_label = 'Footer'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


modeladmin_register(MenuAdmin)
modeladmin_register(FooterAdmin)


class NewWindowExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]
        return '<a href="%s" target="_blank" rel="noopener noreferrer">' % escape(href)


@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NewWindowExternalLinkHandler)


@hooks.register('register_rich_text_features')
def unregister_document_feature(features):
    features.default_features.remove('document-link')


# Removing documents from the menu. Had to specify the index because searching for it breaks the urls
# TODO improve the way the  documents are removed
hooks._hooks['register_admin_menu_item'].pop(2)
