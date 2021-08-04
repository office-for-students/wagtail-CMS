import logging

from django.shortcuts import render

from CMS.enums import enums
from core import utils
from core.utils import get_new_landing_page_for_language
from core.utils import get_page_for_language
from courses import renderer
from courses.models import Course
from courses.models import CourseComparisonPage
from institutions.models import InstitutionList

logger = logging.getLogger(__name__)


def compare_courses_body(request, language=enums.languages.ENGLISH):
    url_params = request.GET

    page = get_page_for_language(language, CourseComparisonPage.objects.all())

    if not page:
        return render(request, '404.html')

    courses_array = []

    courses_list = url_params.getlist('courses') if 'courses' in url_params else None
    print("url_params ::", courses_list)

    if courses_list:
        # Ignore anything more than 7 (avoid malicious activity)
        for course in courses_list[0:7]:
            if course:
                course = course.split(',')
                print("course = course");
                course, error = Course.find(institution_id=course[0], course_id=course[1], mode=course[2], language=language)

                if error:
                    logger.warning(f"Failed to fetch course, Error fetching course: {error} for {course}")
                    redirect_page = get_new_landing_page_for_language(language)
                    # TODO: Update how errors ar handled as simply redirecting to the home page in this content is not the right answer at all
                    # return redirect(redirect_page + '?load_error=true&error_type=0')

                courses_array.append(course)

    courses = renderer.dataset_for_comparison_view(courses_array, language)

    query_string = request.environ.get('QUERY_STRING')

    context = page.get_context(request)

    context.update(
        dict(
            courses=courses_array,
            courses_data=courses,
            english_url=f"{page.get_english_url()}?{query_string}",
            welsh_url=f"{page.get_welsh_url()}?{query_string}",
            get_params=url_params,
            institutions_list=InstitutionList.get_options()[utils.get_language(request.get_full_path())]
        )
    )

    return render(request, 'courses/course_comparison_body.html', context)
