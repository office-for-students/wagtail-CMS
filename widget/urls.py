from django.conf.urls import url

from widget.views import widget_iframe

urlpatterns = [
    url(r'(?P<uk_prn>[\w\-]+)/(?P<kis_course_id>[\w\-]+)/(?P<orientation>[\w\-]+)/(?P<language>[\w\-]+)/('
        r'?P<kis_mode>[\w\-]+)/', widget_iframe, name='widget_iframe'),
]
