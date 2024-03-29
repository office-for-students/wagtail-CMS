import json
import logging

from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from CMS import translations
from CMS.enums import enums
from CMS.translations.dictionaries.unavailable import UNAVAILABLE
from core.utils import get_new_landing_page_for_language
from core.utils import get_page_for_language
from courses.models import Course
from courses.models import CourseComparisonPage
from courses.models import CourseDetailPage
from courses.models import CourseManagePage

logger = logging.getLogger(__name__)


def regional_earnings(request):
    if 'region' in request.POST and request.is_ajax():
        region = request.POST['region']
        institution_id = request.POST['institution_id']
        course_id = request.POST['course_id']
        kis_mode = request.POST['kis_mode']
        subject_code = request.POST['subject_code']
        language = request.POST['language']
        course, error = Course.find(institution_id, course_id, kis_mode, language)

        with open("./CMS/static/jsonfiles/regions.json", "r") as f:
            regions = f.read()
        region_full_name = "region unknown"
        region_dict = json.loads(regions)
        for region_elem in region_dict:
            elem_id = region_elem['id']
            if elem_id == region:
                if language == 'cy':
                    region_full_name = region_elem['name_cy']
                else:
                    region_full_name = region_elem['name_en']

                if region_full_name[:2] == "- ":
                    region_full_name = region_full_name[2:]
                break

        def format_thousands(earnings):
            return f'{int(earnings):,}'

        if language == 'cy':
            # inst_prov_pc_delimiter_go = "wedi'u cyflogi yn"
            inst_prov_pc_delimiter_go = "wedi'u cyflogi yn"
            inst_prov_pc_delimiter_leo = "wedi'u lleoli yn"
            inst_prov_pc_prefix = "Mae "
        else:
            # inst_prov_pc_delimiter_go = "are employed in"
            inst_prov_pc_delimiter_go = "are employed in"
            inst_prov_pc_delimiter_leo = "are based in"
            inst_prov_pc_prefix = ""

        salaries_aggregate = [element for element in course.salary_aggregates if element.subject_code == subject_code][
            0]

        unavail_msgs_go = salaries_aggregate.aggregated_salaries_sector[0].display_unavailable_info(language)
        unavail_msgs_leo = salaries_aggregate.aggregated_salaries_sector[1].display_unavailable_info(language)
        salary_sector_15_unavail_text = ""
        salary_sector_3_unavail_text = ""
        salary_sector_5_unavail_text = ""
        unavailable_region_not_exists = ""
        unavailable_region_not_nation = ""
        unavailable_region_is_ni = ""

        if 'unavailable_region_not_exists' in unavail_msgs_leo and unavail_msgs_leo[
            'unavailable_region_not_exists'] != "":
            unavailable_region_not_exists = unavail_msgs_leo['unavailable_region_not_exists']
        if 'unavailable_region_not_nation' in unavail_msgs_go and unavail_msgs_go[
            'unavailable_region_not_nation'] != "":
            unavailable_region_not_nation = unavail_msgs_go['unavailable_region_not_nation']
        if 'unavailable_region_is_ni' in unavail_msgs_leo and unavail_msgs_leo['unavailable_region_is_ni'] != "":
            unavailable_region_is_ni = unavail_msgs_leo['unavailable_region_is_ni']

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[0], "med" + region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[0], "med" + region) == "" or getattr(
                    salaries_aggregate.aggregated_salaries_sector[0], "med" + region) is None:
                salary_sector_15_unavail_text = unavailable_region_not_exists
            elif region not in ('_uk', '_e', '_s', '_w', '_ni'):
                salary_sector_15_unavail_text = unavailable_region_not_nation

            med = getattr(salaries_aggregate.aggregated_salaries_sector[0], "med" + region, None)
            if med is not None and med != "NA":
                salary_sector_15_med = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[0], "med" + region))
                salary_sector_15_lq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[0], "lq" + region))
                salary_sector_15_uq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[0], "uq" + region))
                salary_sector_15_pop = getattr(salaries_aggregate.aggregated_salaries_sector[0], "pop" + region)
                inst_prov_pc_go = getattr(salaries_aggregate.aggregated_salaries_inst[0], 'prov_pc' + region)
            else:
                salary_sector_15_unavail_text = unavailable_region_not_exists
                salary_sector_15_med = None
                salary_sector_15_lq = None
                salary_sector_15_uq = None
                salary_sector_15_pop = None
                inst_prov_pc_go = None
        else:
            if region in ('_uk', '_e', '_s', '_w', '_ni'):
                salary_sector_15_unavail_text = unavailable_region_not_exists
            else:
                salary_sector_15_unavail_text = unavailable_region_not_nation
            salary_sector_15_med = None
            salary_sector_15_lq = None
            salary_sector_15_uq = None
            salary_sector_15_pop = None
            inst_prov_pc_go = None

        if not inst_prov_pc_go:
            inst_prov_pc_go = 0

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[1], "med" + region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[1], "med" + region) == "" or getattr(
                    salaries_aggregate.aggregated_salaries_sector[1], "med" + region) is None:
                salary_sector_3_unavail_text = unavailable_region_not_exists
            elif region == '_ni':
                salary_sector_3_unavail_text = unavailable_region_is_ni

            med = getattr(salaries_aggregate.aggregated_salaries_sector[1], "med" + region)
            if med is not None and med != "NA":
                salary_sector_3_med = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[1], "med" + region))
                salary_sector_3_lq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[1], "lq" + region))
                salary_sector_3_uq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[1], "uq" + region))
                salary_sector_3_pop = getattr(salaries_aggregate.aggregated_salaries_sector[1], "pop" + region)
                inst_prov_pc_leo3 = getattr(salaries_aggregate.aggregated_salaries_inst[1], 'prov_pc' + region)
            else:
                salary_sector_3_unavail_text = unavailable_region_not_exists
                salary_sector_3_med = None
                salary_sector_3_lq = None
                salary_sector_3_uq = None
                salary_sector_3_pop = None
                inst_prov_pc_leo3 = None
        else:
            if region == "_ni":
                salary_sector_3_unavail_text = unavailable_region_is_ni
            else:
                salary_sector_3_unavail_text = unavailable_region_not_exists
            salary_sector_3_med = None
            salary_sector_3_lq = None
            salary_sector_3_uq = None
            salary_sector_3_pop = None
            inst_prov_pc_leo3 = None

        if (not inst_prov_pc_leo3 or inst_prov_pc_leo3 == '') and (inst_prov_pc_go != ''):
            inst_prov_pc_leo3 = inst_prov_pc_go

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[2], "med" + region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[2], "med" + region) == "" or getattr(
                    salaries_aggregate.aggregated_salaries_sector[2], "med" + region) is None:
                salary_sector_5_unavail_text = unavailable_region_not_exists
            elif region == '_ni':
                salary_sector_5_unavail_text = unavailable_region_is_ni

            med = getattr(salaries_aggregate.aggregated_salaries_sector[2], "med" + region)
            if med is not None and med != "NA":
                salary_sector_5_med = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[2], "med" + region))
                salary_sector_5_lq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[2], "lq" + region))
                salary_sector_5_uq = format_thousands(
                    getattr(salaries_aggregate.aggregated_salaries_sector[2], "uq" + region))
                salary_sector_5_pop = getattr(salaries_aggregate.aggregated_salaries_sector[2], "pop" + region)
                inst_prov_pc_leo5 = getattr(salaries_aggregate.aggregated_salaries_inst[2], 'prov_pc' + region)
            else:
                salary_sector_5_unavail_text = unavailable_region_not_exists
                salary_sector_5_med = None
                salary_sector_5_lq = None
                salary_sector_5_uq = None
                salary_sector_5_pop = None
                inst_prov_pc_leo5 = None
        else:
            if region == "_ni":
                salary_sector_5_unavail_text = unavailable_region_is_ni
            else:
                salary_sector_5_unavail_text = unavailable_region_not_exists
            salary_sector_5_med = None
            salary_sector_5_lq = None
            salary_sector_5_uq = None
            salary_sector_5_pop = None
            inst_prov_pc_leo5 = None

        if (not inst_prov_pc_leo5 or inst_prov_pc_leo5 == '') and (inst_prov_pc_leo3 != ''):
            inst_prov_pc_leo5 = inst_prov_pc_leo3

        resp = {
            'typical_range_text': translations.term_for_key(key='typical_range', language=language),
            'data_from_text': translations.term_for_key(key='Data from', language=language),
            'respondents_text': translations.term_for_key(key='respondents', language=language),
            'people_text': translations.term_for_key(key='people', language=language),
            'of_those_asked_text': translations.term_for_key(key='of those asked', language=language),
            'region_full_name': region_full_name,

            'salary_sector_15_med': salary_sector_15_med,
            'salary_sector_15_lq': salary_sector_15_lq,
            'salary_sector_15_uq': salary_sector_15_uq,
            'salary_sector_15_pop': salary_sector_15_pop,
            'salary_sector_15_unavail_text': salary_sector_15_unavail_text,

            'salary_sector_3_med': salary_sector_3_med,
            'salary_sector_3_lq': salary_sector_3_lq,
            'salary_sector_3_uq': salary_sector_3_uq,
            'salary_sector_3_pop': salary_sector_3_pop,
            'salary_sector_3_unavail_text': salary_sector_3_unavail_text,

            'salary_sector_5_med': salary_sector_5_med,
            'salary_sector_5_lq': salary_sector_5_lq,
            'salary_sector_5_uq': salary_sector_5_uq,
            'salary_sector_5_pop': salary_sector_5_pop,
            'salary_sector_5_unavail_text': salary_sector_5_unavail_text,

            'inst_prov_pc_go': inst_prov_pc_go,
            'inst_prov_pc_leo3': inst_prov_pc_leo3,
            'inst_prov_pc_leo5': inst_prov_pc_leo5,
            'inst_prov_pc_delimiter_go': inst_prov_pc_delimiter_go,
            'inst_prov_pc_delimiter_leo': inst_prov_pc_delimiter_leo,
            'inst_prov_pc_prefix': inst_prov_pc_prefix
        }
        return JsonResponse(resp)
    else:
        return JsonResponse({'retval': 'unhandled error'}),


def courses_detail(request, institution_id, course_id, kis_mode, language=enums.languages.ENGLISH):
    course, error = Course.find(institution_id, course_id, kis_mode, language)
    if error:
        redirect_page = get_new_landing_page_for_language(language)
        # redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')
    institution_name = course.institution.pub_ukprn_name
    if ", the" in institution_name:
        institution_name = f"The {institution_name.replace(', the', '')}"
    course_title = course.satisfaction_stats[0].display_subject_name
    if course.satisfaction_stats[0].aggregation_level == 14:
        course_title = course.display_title()


    page = get_page_for_language(language, CourseDetailPage.objects.all())
    page.uni_site_links_header = page.uni_site_links_header.replace('{{institution_name}}',
                                                                    course.institution.pub_ukprn_name)

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    if not page:
        return render(request, '404.html')

    path = request.path.replace("/en/", "/")
    if language == enums.languages.ENGLISH:
        translated_url = '/cy' + path if language == enums.languages.ENGLISH else path
    else:
        translated_url = path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'course': course,
        'comparison_link': comparison_page.url if comparison_page else '#',
        'manage_link': bookmark_page.url if bookmark_page else '#',
        'translated_url': translated_url,
        "course_title": course_title,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies'),
        "has_summary": has_summary_stats(course),
        "institution_name": institution_name
    })

    if course.institution.pub_ukprn == "10007762":
        context["gcu"] = True

    salary_data = course.go_salaries_inst[0]
    salary_agg = salary_data.aggregate if salary_data.aggregate else course.leo3_salaries_inst[0].aggregate

    if salary_agg in ["1", "2", "11", "12", "21", "22"]:
        header = UNAVAILABLE["new_course_earnings_unavail_header"][language].format(salary_data.display_subject_name())
        new_course_unavail = {"header": header, "body": UNAVAILABLE["new_course_earnings_unavail_body"][language]}
        context.update({"new_course_unavail": new_course_unavail})

    return render(request, 'courses/new_course_details/course_detail_page.html', context)


def compare_courses(request, language=enums.languages.ENGLISH):
    page = get_page_for_language(language, CourseComparisonPage.objects.all())

    if not page:
        return render(request, '404.html')

    context = page.get_context(request)

    context.update(
        dict(
            page=page,
            cookies_accepted=request.COOKIES.get('discoverUniCookies'),
        )
    )

    return render(request, 'courses/course_comparison_page.html', context)


def get_summary_stats(course):
    data_points = [
        course.go_salaries_inst[0].med,
        course.employment_stats[0].in_work_or_study,
        course.graduate_perceptions[0].go_work_skills,
        course.satisfaction_stats[0].question_23.agree_or_strongly_agree,
        course.satisfaction_stats[0].question_16.agree_or_strongly_agree,
    ]
    if course.country.code == "XF":
        data_points.append(course.satisfaction_stats[0].question_28.agree_or_strongly_agree)
    else:
        data_points.append(course.satisfaction_stats[0].question_9.agree_or_strongly_agree)
    return data_points


def has_summary_stats(course):
    if any(data is not None and data != '' for data in get_summary_stats(course)):
        return True
    return False
