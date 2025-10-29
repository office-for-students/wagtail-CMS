from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

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
    path('documents/', include(wagtaildocs_urls)),
    path('robots.txt', robots, name='robots'),
    path('sitemap.xml', sitemap_new, name='sitemap'),
    path('sitemaps/content.xml', content_sitemap, name='content_sitemap'),
    path('sitemaps/general.xml', sitemap, name='cms_sitemap'),
    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'^results/$', coursefinder_views.results, name='results'),
    re_path(r'^feedback', core_views.submit_feedback, name='submit_feedback'),
    re_path(r'^jsonfiles/subjects', core_views.get_subjects_json, name='jsonfiles_subjects'),
    re_path(r'^jsonfiles/institutions/(?P<language>[\w\-]+?)/', core_views.get_institutions_json,
            name='jsonfiles_institutions'),

    re_path(r'^narrow-search/$', coursefinder_views.narrow_search, name='narrow_search'),
    re_path(r'^course-finder/results/$', coursefinder_views.course_finder_results, name='course_finder_results'),

    re_path(r'^widget/', include('widget.urls')),
    re_path(r'^Widget/', include('widget.urls')),
    re_path(r'^v2/widget/', include('v2_widget.urls')),
    re_path(r'^v2/Widget/', include('v2_widget.urls')),
    re_path(r'^course-details/', include(courses_urls)),
    re_path(r'^institution-details/', include(institution_urls)),
    re_path(r'^course-comparison/', course_views.compare_courses, name="course_comparison"),
    re_path(r'^ajax/course-comparison/', course_views.compare_courses_body),

    re_path(r'(?P<language>[\w\-]+?)/', include(welsh_urls)),

    re_path(r'', include(wagtail_urls)),

    # apw added.
    re_path(r'^regional_earnings$', regional_earnings, name='regional_earnings'),
]

# TODO: remove the True clause below when going live.
if True or not settings.READ_ONLY:
    urlpatterns.insert(0, re_path(r'^admin/', include(wagtailadmin_urls)))
    urlpatterns.insert(0, re_path(r'^django-admin/', admin.site.urls))

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
