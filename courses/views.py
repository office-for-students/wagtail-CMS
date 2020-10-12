from django.shortcuts import render, redirect

from CMS.enums import enums
from CMS.translations import DICT
from core.utils import get_page_for_language

from courses.models import CourseDetailPage, Course, CourseComparisonPage, CourseManagePage
from site_search.models import SearchLandingPage
 
from django.http import JsonResponse
import json


def regional_earnings(request):
    if 'region' in request.POST and request.is_ajax():
        region = request.POST['region']
        institution_id = request.POST['institution_id']
        course_id = request.POST['course_id']
        kis_mode = request.POST['kis_mode']
        subject_code = request.POST['subject_code']
        course, error = Course.find(institution_id, course_id, kis_mode, language=enums.languages.ENGLISH)
        language = request.POST['language']

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

        salaries_aggregate = [element for element in course.salary_aggregates if element.subject_code == subject_code][0]

        unavail_msgs_go = salaries_aggregate.aggregated_salaries_sector[0].display_unavailable_info()
        unavail_msgs_leo = salaries_aggregate.aggregated_salaries_sector[1].display_unavailable_info()
        salary_sector_15_unavail_text = ""
        salary_sector_3_unavail_text = ""
        salary_sector_5_unavail_text = ""
        unavailable_region_not_exists = ""
        unavailable_region_not_nation = ""
        unavailable_region_is_ni = ""

        if 'unavailable_region_not_exists' in unavail_msgs_leo and unavail_msgs_leo['unavailable_region_not_exists'] != "":
            unavailable_region_not_exists = unavail_msgs_leo['unavailable_region_not_exists']
        if 'unavailable_region_not_nation' in unavail_msgs_go and unavail_msgs_go['unavailable_region_not_nation'] != "":
            unavailable_region_not_nation = unavail_msgs_go['unavailable_region_not_nation']
        if 'unavailable_region_is_ni' in unavail_msgs_leo and unavail_msgs_leo['unavailable_region_is_ni'] != "":
            unavailable_region_is_ni = unavail_msgs_leo['unavailable_region_is_ni']

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[0], "med"+region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[0], "med"+region) == "" or getattr(salaries_aggregate.aggregated_salaries_sector[0], "med"+region) is None:
                salary_sector_15_unavail_text = unavailable_region_not_exists
            elif region not in ('_uk', '_e', '_s', '_w', '_ni'):
                salary_sector_15_unavail_text = unavailable_region_not_nation

            med = getattr(salaries_aggregate.aggregated_salaries_sector[0], "med"+region, None)
            if med is not None and med != "NA":
                salary_sector_15_med = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[0], "med"+region))
                salary_sector_15_lq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[0], "lq" + region))
                salary_sector_15_uq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[0], "uq" + region))
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

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[1], "med"+region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[1], "med"+region) == "" or getattr(salaries_aggregate.aggregated_salaries_sector[1], "med"+region) is None:
                salary_sector_3_unavail_text = unavailable_region_not_exists
            elif region == '_ni':
                salary_sector_3_unavail_text = unavailable_region_is_ni

            med = getattr(salaries_aggregate.aggregated_salaries_sector[1], "med"+region)
            if med is not None and med != "NA":
                salary_sector_3_med = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[1], "med"+region))
                salary_sector_3_lq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[1], "lq" + region))
                salary_sector_3_uq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[1], "uq" + region))
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

        attr = getattr(salaries_aggregate.aggregated_salaries_sector[2], "med"+region, None)
        if attr is not None:
            if getattr(salaries_aggregate.aggregated_salaries_sector[2], "med"+region) == "" or getattr(salaries_aggregate.aggregated_salaries_sector[2], "med"+region) is None:
                salary_sector_5_unavail_text = unavailable_region_not_exists
            elif region == '_ni':
                salary_sector_5_unavail_text = unavailable_region_is_ni

            med = getattr(salaries_aggregate.aggregated_salaries_sector[2], "med"+region)
            if med is not None and med != "NA":
                salary_sector_5_med = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[2], "med"+region))
                salary_sector_5_lq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[2], "lq" + region))
                salary_sector_5_uq = format_thousands(getattr(salaries_aggregate.aggregated_salaries_sector[2], "uq" + region))
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


        resp = {
            'typical_range_text': DICT.get('Typical range').get(language),
            'data_from_text': DICT.get('Data from').get(language),
            'respondents_text': DICT.get('respondents').get(language),
            'people_text': DICT.get('people').get(language),
            'of_those_asked_text': DICT.get('of those asked').get(language),
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
        }
        return JsonResponse(resp)
    else:
        return JsonResponse({'retval': 'unhandled error'}),


def courses_detail(request, institution_id, course_id, kis_mode, language=enums.languages.ENGLISH):
    course, error = Course.find(institution_id, course_id, kis_mode, language)
    if error:
        redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    page = get_page_for_language(language, CourseDetailPage.objects.all())

    page.uni_site_links_header = page.uni_site_links_header.replace('{{institution_name}}',
                                                                    course.institution.pub_ukprn_name)

    comparison_page = get_page_for_language(language, CourseComparisonPage.objects.all())
    bookmark_page = get_page_for_language(language, CourseManagePage.objects.all())

    if not page:
        return render(request, '404.html')

    full_path = '%s?%s' % (request.path, request.environ.get('QUERY_STRING'))
    welsh_url = '/cy' + full_path if language == enums.languages.ENGLISH else full_path
    english_url = full_path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'course': course,
        'comparison_link': comparison_page.url if comparison_page else '#',
        'manage_link': bookmark_page.url if bookmark_page else '#',
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    return render(request, 'courses/course_detail_page.html', context)


def compare_courses(request, language=enums.languages.ENGLISH):
    get_params = request.GET
    error1 = None
    error2 = None
    course1 = None
    course2 = None

    course1_params = get_params.get('course1').split(',') if 'course1' in get_params else None
    course2_params = get_params.get('course2').split(',') if 'course2' in get_params else None

    page = get_page_for_language(language, CourseComparisonPage.objects.all())

    if course1_params:
        course1, error1 = Course.find(course1_params[0], course1_params[1], course1_params[2], language)
    if course2_params:
        course2, error2 = Course.find(course2_params[0], course2_params[1], course2_params[2], language)

    if error1 or error2:
        redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    if not page:
        return render(request, '404.html')

    query_string = request.environ.get('QUERY_STRING')
    english_url = page.get_english_url() + query_string
    welsh_url = page.get_welsh_url() + query_string

    context = page.get_context(request)
    context.update({
        'page': page,
        'course1': course1,
        'course2': course2,
        'english_url': english_url,
        'welsh_url': welsh_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    return render(request, 'courses/course_comparison_page.html', context)
