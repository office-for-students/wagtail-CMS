from django.urls import re_path

from institutions.views import institution_detail

urlpatterns = [
    re_path(r'(?P<institution_id>[\w\-]+?)/', institution_detail, name='institution_detail'),
]
