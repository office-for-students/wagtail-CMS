from django.urls import path

from institutions.views import institution_detail

urlpatterns = [
    path('<institution_id>/', institution_detail, name='institution_detail'),
]
