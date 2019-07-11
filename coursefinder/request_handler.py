import requests
from django.conf import settings

from CMS.test.mocks import SearchMocks


def query_course_and_institution(course, institution, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        base_url = "%s/search/institution-courses?limit=%s&offset=%sq=%s&institutions=%s"
        return requests.get(url=base_url % (settings.SEARCHAPIHOST, limit, offset, course, institution))


def course_finder_query(subject, institution, mode, countries, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        url = "%s/search/institution-courses?limit=%s&offset=%s" % (settings.SEARCHAPIHOST, limit, offset)
        if subject != '':
            url = f"{url}&subjects={subject}"
        if institution != '':
            url = f"{url}&institutions={institution}"
        if 'Full-time,Part-time' not in mode and mode != '':
            url = f"{url}&filters={mode.lower().replace('-', '_').replace(' ', '_')}"
        if countries != '':
            url = f"{url}&countries={countries.lower().replace(' ', '_')}"

        return requests.get(url=url)
