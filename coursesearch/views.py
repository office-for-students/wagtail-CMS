from django.shortcuts import render

from CMS.enums import enums
from core.utils import get_page_for_language
from coursesearch.models import CourseFinderResults

def course_finder_results_new(request, language=enums.languages.ENGLISH):
    page = get_page_for_language(language, CourseFinderResults.objects.all())
    path = request.path.replace("/en/", "/")
    if language == enums.languages.ENGLISH:
        translated_url = "/cy" + path if language == enums.languages.ENGLISH else path
    else:
        translated_url = path.replace("/cy/", "/")
    context = {
        "page": page,
        "lang": language,
        "translated_url": translated_url
    }

    return render(request, "coursefinder/course_finder_results.html", context)

