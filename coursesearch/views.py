from django.shortcuts import render

from CMS.enums import enums
from core.utils import get_page_for_language
from coursesearch.models import CourseFinderResults

# page not in wagtail, so needs to have the language set for some shared parts to render correctly
class Page:
    language = "en"

    def get_language(self):
        return self.language


def course_finder_results_new(request, language=enums.languages.ENGLISH):
    get_page_for_language(language, CourseFinderResults.objects.all())
    path = request.path.replace("/en/", "/")

    page = Page()
    page.language = language

    if language == enums.languages.ENGLISH:
        translated_url = "/cy" + path if language == enums.languages.ENGLISH else path
    else:
        translated_url = path.replace("/cy/", "/")
    context = {
        "lang": language,
        "translated_url": translated_url,
        "page": page
    }

    return render(request, "coursefinder/course_finder_results.html", context)

