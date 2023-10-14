from typing import Tuple

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from CMS.enums import enums
from CMS.translations import term_for_key
from core.utils import get_new_landing_page_for_language
from core.utils import get_page_for_language
from institutions.models import Institution
from institutions.models import InstitutionDetailPage

AFFILIATE_INSTITUTIONS = "affiliated"
PENDING_INSTITUTIONS = "pending"
TEF_INSTITUTIONS = "tef"
WALES_INSTITUTIONS = "XI"
SCOTTISH_INSTITUTIONS = "XH"
NORTHERN_IRISH_INSTITUTIONS = "XG"
ENGLISH_INSTITUTIONS = "XF"


# from django.core.urlresolvers import reverse
def get_tef_status(institution):
    if institution.pub_ukprn_country_code == ENGLISH_INSTITUTIONS:
        # England
        if type(institution.tef_outcome) == list:
            # Affiliate
            return AFFILIATE_INSTITUTIONS
        else:
            if institution.tef_outcome['overall_rating'] == "Pending":
                # Pending
                return PENDING_INSTITUTIONS
            else:
                # Institution has tef data
                return TEF_INSTITUTIONS
    else:
        return institution.pub_ukprn_country_code



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

    tef_context = generate_tef_context(institution, language, status=get_tef_status(institution))

    context = page.get_context(request)
    context.update({
        'page': page,
        'institution': institution,
        'jms': jms,
        'translated_url': translated_url,
        'cookies_accepted': request.COOKIES.get('discoverUniCookies'),
        "tef": tef_context
    })

    context["totals_string"] = term_for_key("courses_at_this_uni", language=language).format(
        institution.total_number_of_courses)

    return render(request, 'institution/institution_detail.html', context)


def get_tef_image(outcome_1, outcome_2, outcome_3) -> Tuple[str, str]:
    return (f"images/tef_images/{outcome_1.lower()}_{outcome_2.lower()}_{outcome_3.lower()}.svg",
            f"TEF awards as follows: \nOverall Rating: {outcome_1}; \nStudent Expreience Rating: {outcome_2}; \nand Student Outcomes Rating: {outcome_3}.")

    # https://www.officeforstudents.org.uk/advice-and-guidance/the-tef/


def get_tef_body_copy_context(institution, language, status, tef_context, affiliates=[]):
    if status == AFFILIATE_INSTITUTIONS:
        tef_context["left_copy"] = None
        tef_context["left_button"] = None
        tef_context["left_link"] = None
        tef_context["right_copy"] = create_affiliate_copy(
            institution=institution,
            language=language,
            affiliates=affiliates,
            institution_name=tef_context["name"]
        )
        tef_context["right_button"] = term_for_key("find_out_more_about_tef", language=language)
        tef_context["right_link"] = "https://www.officeforstudents.org.uk/advice-and-guidance/the-tef/"
    if status == TEF_INSTITUTIONS:
        tef_context["head_copy"] = term_for_key("participated_in_tef_awarded", language=language)
        tef_context["left_copy"] = None
        tef_context["left_button"] = term_for_key("participated_in_tef_awarded_left", language=language)
        tef_context["left_link"] = institution.tef_outcome["outcome_url"]
        tef_context["right_copy"] = None
        tef_context["right_button"] = None #term_for_key("participated_in_tef_awarded_right", language=language)
        tef_context["right_link"] = None # institution.tef_outcome["outcome_url"]
    if status == PENDING_INSTITUTIONS:
        print("pending == true")
        tef_context["left_copy"] = None
        tef_context["left_button"] = None
        tef_context["left_link"] = None
        tef_context["right_copy"] = term_for_key("participated_in_tef_pending", language=language)
        tef_context["right_button"] = term_for_key("find_out_more_about_tef", language=language)
        tef_context["right_link"] = "https://TEF2023.officeforstudents.org.uk/"
    if status == WALES_INSTITUTIONS:
        tef_context["left_copy"] = term_for_key("hefcw_explanation", language=language)
        tef_context["left_button"] = term_for_key("more_about_hefcw", language=language)
        tef_context["left_link"] = term_for_key("hefcw_url", language=language)
        tef_context["right_copy"] = institution.qaa_report_type_string
        tef_context["right_button"] = term_for_key("more_about_hefcw_tef_href", language=language)
        tef_context["right_link"] = institution.qaa_url
        tef_context["wales"] = "true"
    if status == SCOTTISH_INSTITUTIONS:
        tef_context["left_copy"] = term_for_key("sfc_explanation", language=language)
        tef_context["left_button"] = term_for_key("more_about_sfc", language=language)
        tef_context["left_link"] = term_for_key("sfc_href", language=language)
        tef_context["right_copy"] = institution.qaa_report_type_string
        tef_context["right_button"] = term_for_key("more_about_qaa_scotland_btn", language=language)
        tef_context["right_link"] = institution.qaa_url
    if status == NORTHERN_IRISH_INSTITUTIONS:
        tef_context["left_copy"] = term_for_key("ni_explanation_economy", language=language)
        tef_context["left_button"] = term_for_key("ni_explanation_economy_btn", language=language)
        tef_context["left_link"] = term_for_key("ni_explanation_economy_href", language=language)
        tef_context["right_copy"] = term_for_key("institution.qaa_report_type_string", language=language)
        tef_context["right_button"] = term_for_key("ni_previous_model_btn", language=language)
        tef_context["right_link"] = institution.qaa_url

    tef_context["status"] = status

def generate_tef_context(institution, language, status):
    print("status", status)
    tef_context = {
        "name": institution.pub_ukprn_name,
        "tef_image": get_logo_path(institution=institution, status=status),
    }
    affiliates = []
    if status == AFFILIATE_INSTITUTIONS:
        # JMS institution returns a list that includes the rates of affiliated institutions.
        tef_context["jms"] = True
        print("is jms")
        for institution_tef_data in institution.tef_outcome:
            print("institution_tef_data", institution_tef_data)
            institution_id = institution_tef_data["report_ukprn"]
            institution, error = Institution.find(institution_id, language)
            affiliates.append(
                {
                    "name": institution.pub_ukprn_name,
                    "du_url": reverse(
                        'institution_detail',
                        kwargs={'institution_id': institution_id}
                    ),
                }
            )
        tef_context["affiliates"] = affiliates
    else:
        tef_context["jms"] = False

    get_tef_body_copy_context(
        institution=institution,
        language=language,
        status=status,
        tef_context=tef_context,
        affiliates=affiliates
    )

    return tef_context


def create_linked_institution(name, url) -> str:
    return f'<a href="{url}" style="all:unset; text-decoration:underline;" target="_blank" alt="Link to institution {name}, opens in new tab">{name}</a>'


def create_affiliate_copy(institution, language, affiliates, institution_name) -> str:
    base_str = term_for_key("tef_affiliate_left", language=language)
    end_str = ""
    if len(affiliates) == 3:
        and_str = term_for_key("and", language=language)
        end_str = f"{create_linked_institution(affiliates[0]['name'], affiliates[0]['du_url'])}, {create_linked_institution(affiliates[1]['name'], affiliates[1]['du_url'])}{and_str}{create_linked_institution(affiliates[2]['name'], affiliates[2]['du_url'])}"
    if len(affiliates) == 2:
        and_str = term_for_key("and", language=language)
        end_str = f"{create_linked_institution(affiliates[0]['name'], affiliates[0]['du_url'])}{and_str}{create_linked_institution(affiliates[1]['name'], affiliates[1]['du_url'])}"
    if len(affiliates) == 1:
        end_str = f"{create_linked_institution(affiliates[0]['name'], affiliates[0]['du_url'])}"

    return base_str.format(institution_name, end_str)


def get_logo_path(institution, status) -> Tuple[str, str]:
    """
    Returns a tuple of the path to the logo to the correct logo for the tef data for that institution
    and the appropriate alt text for the logo.
    """

    if status == TEF_INSTITUTIONS:
        # Affiliate
        tef_image = get_tef_image(
            institution.tef_outcome["overall_rating"],
            institution.tef_outcome["student_experience_rating"],
            institution.tef_outcome["student_outcomes_rating"]
        )
        return tef_image
    elif status == PENDING_INSTITUTIONS or status == AFFILIATE_INSTITUTIONS:
        return "images/tef_logo.svg", "Teaching Excellence Framework logo"
    elif status == WALES_INSTITUTIONS:
        # Wales
        return "images/hefcw.svg", "Higher Education Funding Council for Wales logo"
    elif status == SCOTTISH_INSTITUTIONS:
        # Scotland
        return "images/sfc.svg", "Scottish Funding Council logo"
    elif status == NORTHERN_IRISH_INSTITUTIONS:
        # Northern Ireland
        return "images/department_of_economy_logo.svg", "Department of Economy logo"
