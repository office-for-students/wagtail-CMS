from django.urls import path

from courses.views import courses_detail
from courses.views.translate import get_translations

urlpatterns = [
    path('<institution_id>/<course_id>/<kis_mode>/', courses_detail, name='courses_detail'),
    path('translations/', get_translations, name='course_translation')
]
