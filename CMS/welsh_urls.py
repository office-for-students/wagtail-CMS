from coursefinder import views as coursefinder_views
from courses import urls as courses_urls
from courses import views as course_views
from django.conf.urls import include
from django.urls import re_path
from institutions import urls as institution_urls
from search import views as search_views

urlpatterns = [
    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'^results/$', coursefinder_views.results, name='results'),

    re_path(r'^narrow-search/$', coursefinder_views.narrow_search, name='narrow_search'),
    re_path(r'^course-finder/results/$', coursefinder_views.course_finder_results, name='course_finder_results'),

    re_path(r'^course-details/', include(courses_urls)),
    re_path(r'^institution-details/', include(institution_urls)),
    re_path(r'^cymharu-cyrsiau/', course_views.compare_courses),
    re_path(r'^ajax/course-comparison/', course_views.compare_courses_body),
]
