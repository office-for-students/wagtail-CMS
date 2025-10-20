from axes.models import AccessAttempt
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
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


class AccessAttemptAdmin(ModelAdmin):
    model = AccessAttempt
    menu_label = 'Access'
    menu_icon = 'code'
    menu_order = 5
    add_to_settings_menu = True


modeladmin_register(MenuAdmin)
modeladmin_register(FooterAdmin)
modeladmin_register(AccessAttemptAdmin)


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


@hooks.register('register_rich_text_features')
def register_underline(features):
    feature_name = "underline"
    type_ = "UNDERLINE"
    tag = "span"

    control = {
        "type": type_,
        "label": "U",
        "description": "Underline",
        "style": {
            "text-decoration": "underline"
        },
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            tag: InlineStyleElementHandler(type_)
        },
        "to_database_format": {
            "style_map": {
                type_: {
                    'element': tag,
                    'props': {
                        "style": "text-decoration: underline;"
                    }
                }
            }
        }
    }

    features.register_converter_rule(
        "contentstate",
        feature_name,
        db_conversion
    )

    features.default_features.append(feature_name)


@hooks.register("construct_main_menu")
def hide_documents_menu_item(request, menu_items):
    # Remove the Documents menu item by its name
    menu_items[:] = [item for item in menu_items if item.name != "documents"]
