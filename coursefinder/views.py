from django.shortcuts import render
from django.http import HttpResponseRedirect

from coursefinder.models import CourseSearch, CourseFinderSearch
from coursefinder.models import CourseFinderResults
from django.conf import settings
import requests


def results(request):
    query_params = request.GET
    course_search = CourseSearch(query_params.get('courseQuery', ""), query_params.get('institutionQuery', ""),
                                 query_params.get('page', 1), query_params.get('count', 20))
    course_search.execute()

    page = CourseFinderResults.objects.get()

    context = {
        'page': page,
        'search': course_search,
        'pagination_url': 'results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)


def narrow_search(request):
    selection = request.POST.get('radioGroup', None)
    subject_query = request.POST.get('subject_query', None)
    mode_query = request.POST.get('mode_query', None)
    countries_query = request.POST.get('countries_query', None)
    url = "%s/search/institution-courses?" % settings.SEARCHAPIHOST
    if subject_query != '':
        url = url + "subjects=%s" % subject_query
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
    query_params = request.GET
    course_finder_search = CourseFinderSearch(query_params.get('subject_query', None),
                                              query_params.get('institution_query', None),
                                              query_params.get('mode_query', None),
                                              query_params.get('countries_query', None),
                                              query_params.get('page', 1),
                                              query_params.get('count', 20))
    course_finder_search.execute()

    page = CourseFinderResults.objects.get()

    context = {
        'page': page,
        'search': course_finder_search,
        'pagination_url': 'course_finder_results'
    }

    return render(request, 'coursefinder/course_finder_results.html', context)
