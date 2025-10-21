from django.conf.urls import include
from django.urls import re_path

from widget.views import widget_embed
from widget.views import widget_iframe

urlpatterns = [
    re_path(r'(?P<uk_prn>[\w\-]+?)/(?P<kis_course_id>[\w\-\~]+?)/', include([
            re_path(r'^small/$(?i)', widget_iframe, name='widget_iframe'),
            re_path(r'^small/(?P<optional_1>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            re_path(r'^small/(?P<optional_1>[\w\-]+?)/(?P<optional_2>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            re_path(r'^(?P<optional_1>[\w\-]+?)/small/$(?i)', widget_iframe, name='widget_iframe'),
            re_path(r'^(?P<optional_1>[\w\-]+?)/small/(?P<optional_2>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            re_path(r'^(?P<optional_1>[\w\-]+?)/small/(?P<optional_2>[\w\-]+?)/(?P<optional_3>[\w\-]+?)/$(?i)',
                widget_iframe, name='widget_iframe'),
        ])),
    re_path(r'^embed-script$(?i)', widget_embed, name='widget_embed'),
    re_path(r'^embed-script/$(?i)', widget_embed, name='widget_embed'),
    re_path(r'^embed-script.js$(?i)', widget_embed, name='widget_embed'),
    re_path(r'^embed-script.js/$(?i)', widget_embed, name='widget_embed')
]