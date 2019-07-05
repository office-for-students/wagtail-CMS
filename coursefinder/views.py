from django.shortcuts import render
from django.http import HttpResponseRedirect
from coursefinder.models import CourseFinderResults
from django.conf import settings
import requests


def results(request):
    course_query = request.GET.get('courseQuery', "")
    institution_query = request.GET.get('institutionQuery', "")
    r = requests.get(url="%s/search/institution-courses?q=%s&institutions=%s" %
                         (settings.SEARCHAPIHOST, course_query, institution_query))
    data = r.json()
    total_courses = data['total_number_of_courses']
    total_institutions = data['total_results']
    results = data['items']
    page = CourseFinderResults.objects.get()

    return render(request, 'coursefinder/course_finder_results.html', {
        'page': page,
        'results': results,
        'total_courses': total_courses,
        'total_institutions': total_institutions
    })


def narrow_search(request):
    selection = request.POST.get('radioGroup', None)
    subject_query = request.POST.get('subject_query', None)
    mode_query = request.POST.get('mode_query', None)
    countries_query = request.POST.get('countries_query', None)
    url = "%s/search/institution-courses?" % (settings.SEARCHAPIHOST)
    if subject_query != '':
        url = url + "subjects=%s" % (subject_query)
    if 'Full-time,Part-time' not in mode_query and mode_query != '':
        url = url + "&filters=%s" % (mode_query.lower().replace('-', '_').replace(' ', '_'))
    if countries_query != '':
        url = url + "&countries=%s" % (countries_query.lower().replace(' ', '_'))
    r = requests.get(url=url)
    data = r.json()
    total_courses = data['total_number_of_courses']
    total_institutions = data['total_results']
    results = data['items']
    page = CourseFinderResults.objects.get()

    if selection == "uni":
        return HttpResponseRedirect("/course-finder/uni")
    elif selection == "city":
        return HttpResponseRedirect("/course-finder/towncity")
    elif selection == "home":
        return HttpResponseRedirect("/course-finder/postcode")
    else:
        return render(request, 'coursefinder/course_finder_results.html', {
            'page': page,
            'results': results,
            'total_courses': total_courses,
            'total_institutions': total_institutions
        })


def course_finder_results(request):
    subject_query = request.GET.get('subject_query', None)
    institution_query = request.GET.get('institution_query', None)
    mode_query = request.GET.get('mode_query', None)
    countries_query = request.GET.get('countries_query', None)
    url = "%s/search/institution-courses?subjects=%s" % (settings.SEARCHAPIHOST, subject_query)
    if institution_query != '':
        url = url + "&institutions=%s" % (institution_query)
    if 'Full-time,Part-time' not in mode_query and mode_query != '':
        url = url + "&filters=%s" % (mode_query.lower().replace('-', '_').replace(' ', '_'))
    if countries_query != '':
        url = url + "&countries=%s" % (countries_query.lower().replace(' ', '_'))
    r = requests.get(url=url)
    data = r.json()
    total_courses = data['total_number_of_courses']
    total_institutions = data['total_results']
    results = data['items']
    page = CourseFinderResults.objects.get()

    return render(request, 'coursefinder/course_finder_results.html', {
        'page': page,
        'results': results,
        'total_courses': total_courses,
        'total_institutions': total_institutions
    })
