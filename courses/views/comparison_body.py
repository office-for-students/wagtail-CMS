import logging

from django.shortcuts import render

from CMS.enums import enums
from core import utils
from core.utils import get_new_landing_page_for_language
from courses import renderer
from courses.models import Course
from institutions.models import InstitutionList

logger = logging.getLogger(__name__)


def show_has_no_bookmarked_courses(request, language):
    context = dict(institutions_list=InstitutionList.get_options()[utils.get_language(request.get_full_path())])
    return render_with_language_context(request, 'courses/comparison/has_no_saved_courses.html', context, language)


def show_not_enough_saved(request, language):
    return render_with_language_context(request, 'courses/comparison/has_no_compare_courses.html', {}, language)


def show_courses_selected_for_comparison(courses_list, request, language):
    courses_array = []
    if courses_list:
        # Ignore anything more than 7 (avoid malicious activity)
        for course in courses_list[0:7]:
            if course:
                course = course.split(',')
                print("course = course");
                course, error = Course.find(institution_id=course[0], course_id=course[1], mode=course[2],
                                            language=language)

                if error:
                    logger.warning(f"Failed to fetch course, Error fetching course: {error} for {course}")
                    redirect_page = get_new_landing_page_for_language(language)
                    # TODO: Update how errors ar handled as simply redirecting to the home page in this content is not the right answer at all
                    # return redirect(redirect_page + '?load_error=true&error_type=0')

                courses_array.append(course)

    courses = renderer.dataset_for_comparison_view(courses_array, language)

    context = dict(
        courses=courses_array,
        courses_data=courses,
    )

    return render_with_language_context(request, 'courses/comparison/comparison_has_courses.html', context, language)


def compare_courses_body(request, language=enums.languages.ENGLISH):
    url_params = request.GET
    if url_params.get('hasStorage', 0) == "0":
        return show_has_no_bookmarked_courses(request, language)

    stored = url_params.getlist('courses') if 'courses' in url_params else None
    if len(stored) <= 1:
        return show_not_enough_saved(request, language)

    return show_courses_selected_for_comparison(stored, request, language)


def render_with_language_context(request, template, context, language):
    default = dict(page={"get_language": language})
    return render(request, template, {**default, **context})
