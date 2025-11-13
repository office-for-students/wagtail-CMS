from django.conf.urls import include
from django.urls import path

from coursefinder import views as coursefinder_views
from courses import urls as courses_urls
from courses import views as course_views
from institutions import urls as institution_urls
from search import views as search_views

urlpatterns = [
    path('search/', search_views.search, name='search'),
    path('results/', coursefinder_views.results, name='results'),

    path('narrow-search/', coursefinder_views.narrow_search, name='narrow_search'),
    path('course-finder/results/', coursefinder_views.course_finder_results, name='course_finder_results'),

    path('course-details/', include(courses_urls)),
    path('institution-details/', include(institution_urls)),
    path('cymharu-cyrsiau/', course_views.compare_courses),
    path('ajax/course-comparison/', course_views.compare_courses_body),
]
