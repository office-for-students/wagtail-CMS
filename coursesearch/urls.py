from django.urls import path

from coursesearch import views

urlpatterns = [
    path('results/', views.course_finder_results_new, name='course_finder_results'),
    path('results/institution', views.course_finder_results_new),
    path('results/subject', views.course_finder_results_new),
]
