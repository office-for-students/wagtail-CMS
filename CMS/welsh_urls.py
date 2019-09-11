from django.conf.urls import include, url

from courses import urls as courses_urls
from institutions import urls as institution_urls
from home import views as home_views

from search import views as search_views
from coursefinder import views as coursefinder_views

urlpatterns = [
    url(r'', home_views.holding_page),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^results/$', coursefinder_views.results, name='results'),

    url(r'^narrow-search/$', coursefinder_views.narrow_search, name='narrow_search'),
    url(r'^course-finder/results/$', coursefinder_views.course_finder_results, name='course_finder_results'),

    url(r'^course-details/', include(courses_urls)),
    url(r'^institution-details/', include(institution_urls)),
]
