from django.conf.urls import include, url

from courses import urls as courses_urls
from institutions import urls as institution_urls

from search import views as search_views
from coursefinder import views as coursefinder_views
from courses import views as course_views

urlpatterns = [
    url(r'^search/$', search_views.search, name='search'),

    url(r'^narrow-search/$', coursefinder_views.narrow_search, name='narrow_search'),
    url(r'^course-finder/results/$', coursefinder_views.course_finder_results, name='course_finder_results'),

    url(r'^course-details/', include(courses_urls)),
    url(r'^institution-details/', include(institution_urls)),
    url(r'^cymharu-cyrsiau/', course_views.compare_courses),
]
