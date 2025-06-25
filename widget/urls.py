from django.conf.urls import include
from django.conf.urls import url

from widget.views import widget_embed
from widget.views import widget_iframe

urlpatterns = [
    url(r'(?P<uk_prn>[\w\-]+?)/(?P<kis_course_id>[\w\-\~]+?)/', include([
            url(r'^small/$(?i)', widget_iframe, name='widget_iframe'),
            url(r'^small/(?P<optional_1>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            url(r'^small/(?P<optional_1>[\w\-]+?)/(?P<optional_2>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            url(r'^(?P<optional_1>[\w\-]+?)/small/$(?i)', widget_iframe, name='widget_iframe'),
            url(r'^(?P<optional_1>[\w\-]+?)/small/(?P<optional_2>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
            url(r'^(?P<optional_1>[\w\-]+?)/small/(?P<optional_2>[\w\-]+?)/(?P<optional_3>[\w\-]+?)/$(?i)',
                widget_iframe, name='widget_iframe'),
        ])),
    url(r'^embed-script$(?i)', widget_embed, name='widget_embed'),
    url(r'^embed-script/$(?i)', widget_embed, name='widget_embed'),
    url(r'^embed-script.js$(?i)', widget_embed, name='widget_embed'),
    url(r'^embed-script.js/$(?i)', widget_embed, name='widget_embed')
]