from django.conf.urls import include
from django.urls import path

from courses import urls as courses_urls
from courses.views import (
    compare_courses,
    compare_courses_body,
)
from coursesearch.views import course_finder_results_new
from institutions import urls as institution_urls

urlpatterns = [
    path('course-finder/results/', course_finder_results_new, name='course_finder_results'),
    path('course-finder/results/institution', course_finder_results_new),
    path('course-finder/results/subject', course_finder_results_new),
    path('course-details/', include(courses_urls)),
    path('institution-details/', include(institution_urls)),
    path('cymharu-cyrsiau/', compare_courses),
    path('ajax/course-comparison/', compare_courses_body),
]
