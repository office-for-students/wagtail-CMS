from django.conf.urls import url

from courses.views import courses_detail

urlpatterns = [
    url(r'(?P<institution_id>[\w\-]+)/(?P<course_id>[\w\-\~]+)/(?P<kis_mode>[\w\-]+)/', courses_detail,
        name='courses_detail'),
]
