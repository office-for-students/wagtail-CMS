from django.conf.urls import url

from institutions.views import institution_detail

urlpatterns = [
    url(r'(?P<institution_id>[\w\-]+?)/', institution_detail, name='institution_detail'),
]
