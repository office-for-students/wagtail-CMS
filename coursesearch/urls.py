import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from coursesearch import views
from django.urls import path


urlpatterns = [
    path('results/', views.course_finder_results_new, name='course_finder_results'),
    path('results/institution', views.course_finder_results_new),
    path('results/subject', views.course_finder_results_new),
]
