from django.conf.urls import url

from courses.views import courses_detail

urlpatterns = [
    url(r'(?P<uk_prn>[\w\-]+)/(?P<kis_course_id>[\w\-]+)/(?P<kis_mode>[\w\-]+)/', courses_detail,
        name='courses_detail'),
]
