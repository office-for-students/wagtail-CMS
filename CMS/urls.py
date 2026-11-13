import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from core import views as core_views
from core.views import (
    content_sitemap,
    robots,
    sitemap_new,
)
from courses import (
    urls as courses_urls,
    views as course_views,
)
# apw added.
from courses.views import regional_earnings
from coursesearch import views as coursefinder_views
from institutions import urls as institution_urls
from . import welsh_urls

urlpatterns = [
    path('documents/', include(wagtaildocs_urls)),
    path('robots.txt', robots, name='robots'),
    path('sitemap.xml', sitemap_new, name='sitemap'),
    path('sitemaps/content.xml', content_sitemap, name='content_sitemap'),
    path('sitemaps/general.xml', sitemap, name='cms_sitemap'),
    path('feedback', core_views.submit_feedback, name='submit_feedback'),
    path('jsonfiles/subjects', core_views.get_subjects_json, name='jsonfiles_subjects'),
    path('jsonfiles/institutions/<str:language>/', core_views.get_institutions_json, name='jsonfiles_institutions'),
    path('course-finder/results/', coursefinder_views.course_finder_results_new, name='course_finder_results'),
    path('course-finder/results/institution', coursefinder_views.course_finder_results_new),
    path('course-finder/results/subject', coursefinder_views.course_finder_results_new),
    path('v2/widget/', include('v2_widget.urls')),
    path('v2/Widget/', include('v2_widget.urls')),
    path('course-details/', include(courses_urls)),
    path('institution-details/', include(institution_urls)),
    path('course-comparison/', course_views.compare_courses, name="course_comparison"),
    path('ajax/course-comparison/', course_views.compare_courses_body),

    path('<str:language>/', include(welsh_urls)),

    path(r'', include(wagtail_urls)),

    # apw added.
    path('regional_earnings', regional_earnings, name='regional_earnings'),
    # path('api/', api.urls)
]

if not settings.READ_ONLY:
    urlpatterns.insert(0, path('admin/', include(wagtailadmin_urls)))
    urlpatterns.insert(0, path('django-admin/', admin.site.urls))

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
