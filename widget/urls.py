from django.urls import include
from django.urls import path
from django.urls import register_converter

from widget.views import widget_embed
from widget.views import widget_iframe


class CaseInsensitiveConverter:
    regex = '[\w\-]+'

    def to_python(self, value):
        return value.lower()  # Normalize to lowercase

    def to_url(self, value):
        return value


register_converter(CaseInsensitiveConverter, 'ci')

urlpatterns = [
    path('<ci:uk_prn>/<ci:kis_course_id>/', include([
        path('small/', widget_iframe, name='widget_iframe'),
        path('small/<ci:optional_1>/', widget_iframe, name='widget_iframe'),
        path('small/<ci:optional_1>/<ci:optional_2>/', widget_iframe, name='widget_iframe'),
        path('<ci:optional_1>/small/', widget_iframe, name='widget_iframe'),
        path('<ci:optional_1>/small/<ci:optional_2>/', widget_iframe, name='widget_iframe'),
        path('<ci:optional_1>/small/<ci:optional_2>/<ci:optional_3>/', widget_iframe, name='widget_iframe'),
    ])),
    path('embed-script', widget_embed, name='widget_embed'),
    path('embed-script/', widget_embed, name='widget_embed'),
    path('embed-script.js', widget_embed, name='widget_embed'),
    path('embed-script.js/', widget_embed, name='widget_embed')
]