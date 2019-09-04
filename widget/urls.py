from django.conf.urls import url

from widget.views import widget_iframe, widget_embed

urlpatterns = [
    url(r'(?P<uk_prn>[\w\-]+?)/(?P<kis_course_id>[\w\-\~]+?)/(?P<orientation>[\w\-]+?)/(?P<size>[\w\-]+?)/'
        r'(?P<language>[\w\-]+?)/(?P<kis_mode>[\w\-]+?)/$(?i)', widget_iframe, name='widget_iframe'),
    url(r'^embed-script/$(?i)', widget_embed, name='widget_embed'),
]
