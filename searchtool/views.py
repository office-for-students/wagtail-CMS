from django.shortcuts import render
import requests


def results(request):
    course_query = request.GET.get('subject_query', None)
    institution_query = request.GET.get('institution_query', None)
    r = requests.get(url="http://host.docker.internal:10100/search/institution-courses?q=%s&institutions=%s" %
                         (course_query, institution_query))
    data = r.json()
    total_courses = data['total_number_of_courses']
    total_institutions = data['total_results']
    results = data['items']

    return render(request, 'searchtool/results.html', {
        'results': results,
        'total_courses': total_courses,
        'total_institutions': total_institutions
    })
