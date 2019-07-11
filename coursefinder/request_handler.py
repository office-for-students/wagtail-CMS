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
        url = "%s/search/institution-courses?limit=%s&offset=%s&subjects=%s" % (settings.SEARCHAPIHOST, limit, offset,
                                                                                subject)
        if institution != '':
            url = url + "&institutions=%s" % institution
        if 'Full-time,Part-time' not in mode and mode != '':
            url = url + "&filters=%s" % (mode.lower().replace('-', '_').replace(' ', '_'))
        if countries != '':
            url = url + "&countries=%s" % (countries.lower().replace(' ', '_'))

        return requests.get(url=url)
