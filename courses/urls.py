from django.conf.urls import url
from django.urls import path

from courses.views import courses_detail
from courses.views.translate import get_translations

urlpatterns = [
    url(r'(?P<institution_id>[\w\-]+?)/(?P<course_id>[\w\-\~\$()]+?)/(?P<kis_mode>[\w\-]+?)/', courses_detail,
        name='courses_detail'),
    path('translations/', get_translations, name='course_translation')
]
