from django.shortcuts import render, redirect

from CMS.enums import enums
from CMS.translations import term_for_key
from core.utils import get_page_for_language, get_new_landing_page_for_language
from institutions.models import InstitutionDetailPage, Institution


def institution_detail(request, institution_id, language=enums.languages.ENGLISH):
    institution, error = Institution.find(institution_id, language)
    if error:
        redirect_page = get_new_landing_page_for_language(language)
        #redirect_page = get_page_for_language(language, SearchLandingPage.objects.all()).url
        return redirect(redirect_page + '?load_error=true&error_type=0')

    page = get_page_for_language(language, InstitutionDetailPage.objects.all())

    jms = [99999998, 99999997, 99999999, 90000451]

    if not page:
        return render(request, '404.html')

    page.tef_report_link = page.tef_report_link.replace('{{institution_name}}', institution.pub_ukprn_name)
    path = request.path.replace("/en/", "/")
    if language == enums.languages.ENGLISH:
        translated_url = '/cy' + path if language == enums.languages.ENGLISH else path
    else:
        translated_url = path.replace('/cy/', '/')

    context = page.get_context(request)
    context.update({
        'page': page,
        'institution': institution,
        'jms': jms,
        'translated_url': translated_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies')
    })

    if institution.tef_outcome:
        tef_image = get_tef_image(
            institution.tef_outcome.overall_rating,
            institution.tef_outcome.student_experience_rating,
            institution.tef_outcome.outcomes_rating
        )
        context["tef_image"] = tef_image
    context["totals_string"] = term_for_key("courses_at_this_uni", language=language).format(institution.total_number_of_courses)

    return render(request, 'institution/institution_detail.html', context)


def get_tef_image(outcome_1, outcome_2, outcome_3) -> str:
    return f"images/tef_images/{outcome_1.lower()}_{outcome_2.lower()}_{outcome_3.lower()}.svg"

