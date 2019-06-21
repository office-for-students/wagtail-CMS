from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests

# Create your views here.

def results(request):
    course_query = request.GET.get('courseQuery', "")
    institution_query = request.GET.get('institutionQuery', "")
    r = requests.get(url="http://host.docker.internal:10100/search/institution-courses?q=%s&institutions=%s" % (course_query, institution_query))
    data = r.json()
    total_courses = data['total_number_of_courses']
    total_institutions = data['total_results']
    results = data['items']

    return render(request, 'coursefinder/results.html', {
        'results': results,
        'total_courses': total_courses,
        'total_institutions': total_institutions
    })

def narrow_search(request):
    selection = request.POST.get('radioGroup', None)
    if selection == "uni":
        return HttpResponseRedirect("/course-finder/uni")
    elif selection == "city":
        return HttpResponseRedirect("/course-finder/towncity")
    elif selection == "home":
        return HttpResponseRedirect("/course-finder/postcode")
    else:
        return render(request, 'coursefinder/results.html')
