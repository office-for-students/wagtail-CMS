import requests
from django.conf import settings

from CMS.test.mocks import SearchMocks


def query_course_and_institution(course, institution):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        base_url = "%s/search/institution-courses?q=%s&institutions=%s"
        return requests.get(url=base_url % (settings.SEARCHAPIHOST, course, institution))
