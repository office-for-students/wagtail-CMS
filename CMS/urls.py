from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls

from core import views as core_views
from core.views import content_sitemap
from core.views import robots
from core.views import sitemap_new
from coursefinder import views as coursefinder_views
from courses import urls as courses_urls
from courses import views as course_views
# apw added.
from courses.views import regional_earnings
from institutions import urls as institution_urls
from search import views as search_views
from . import welsh_urls

urlpatterns = [
    path('robots.txt', robots, name='robots'),
    path('sitemap.xml', sitemap_new, name='sitemap'),
    path('sitemaps/content.xml', content_sitemap, name='content_sitemap'),
    path('sitemaps/general.xml', sitemap, name='cms_sitemap'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^results/$', coursefinder_views.results, name='results'),
    url(r'^feedback', core_views.submit_feedback, name='submit_feedback'),
    url(r'^jsonfiles/subjects', core_views.get_subjects_json, name='jsonfiles_subjects'),
    url(r'^jsonfiles/institutions/(?P<language>[\w\-]+?)/', core_views.get_institutions_json,
        name='jsonfiles_institutions'),

    url(r'^narrow-search/$', coursefinder_views.narrow_search, name='narrow_search'),
    url(r'^course-finder/results/$', coursefinder_views.course_finder_results, name='course_finder_results'),

    url(r'^widget/', include('widget.urls')),
    url(r'^Widget/', include('widget.urls')),
    url(r'^v2/widget/', include('widget.v2_urls')),
    url(r'^v2/Widget/', include('widget.v2_urls')),
    url(r'^course-details/', include(courses_urls)),
    url(r'^institution-details/', include(institution_urls)),
    url(r'^course-comparison/', course_views.compare_courses, name="course_comparison"),
    url(r'^ajax/course-comparison/', course_views.compare_courses_body),

    url(r'(?P<language>[\w\-]+?)/', include(welsh_urls)),

    url(r'', include(wagtail_urls)),

    # apw added.
    url(r'^regional_earnings$', regional_earnings, name='regional_earnings'),
]

# TODO: remove the True clause below when going live.
if True or not settings.READ_ONLY:
    urlpatterns.insert(0, url(r'^admin/', include(wagtailadmin_urls)))
    urlpatterns.insert(0, url(r'^django-admin/', admin.site.urls))

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)