import json
import os
from collections.abc import Callable
from time import perf_counter
from typing import (
    Any,
    cast,
)
from unittest.mock import patch

from django.core.cache import cache
from django.db import connection
from django.http import HttpResponse
from django.test import (
    override_settings,
    tag,
    TestCase,
)
from django.test.utils import CaptureQueriesContext
from requests.adapters import HTTPAdapter
from requests.models import (
    PreparedRequest,
    Response,
)

from courses.models.wagtail import CourseDetailPage
from courses.test_files.course_mocks import CourseMocks
from home.models import HomePage
from institutions.models import InstitutionList

MAX_OUTBOUND_HTTP_CALLS_WARM = 0
MAX_DB_QUERIES_WARM = 25
COURSE_DETAIL_PATH = "/course-details/10000055/AB20/1/"
HOME_PATH = "/"


@tag("performance")
class PageLoadBudgetTests(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.outbound_urls: list[str] = []
        self.remote_version = "release-1"

        adapter_patcher = patch.object(HTTPAdapter, "send", new=self._fake_http_send)
        adapter_patcher.start()
        self.addCleanup(adapter_patcher.stop)

        environment_patcher = patch.dict(
            os.environ,
            {"JSONFILES_STORAGE_CONTAINER": "https://storage.example.test"},
        )
        environment_patcher.start()
        self.addCleanup(environment_patcher.stop)

        settings_patcher = override_settings(
            DATASETAPIHOST="https://dataset.example.test",
            DATASETAPIKEY="test-api-key-not-real",
            JSONFILES_STORAGE_CONTAINER="https://storage.example.test",
            LOCAL="False",
        )
        settings_patcher.enable()
        self.addCleanup(settings_patcher.disable)

        version_patcher = patch.object(InstitutionList, "version", "release-0")
        version_patcher.start()
        self.addCleanup(version_patcher.stop)

        options_patcher: Any = patch.object(
            InstitutionList,
            "options",
            {"en": [], "cy": []},
        )
        options_patcher.start()
        self.addCleanup(options_patcher.stop)

        self._create_course_detail_page()

    def _create_course_detail_page(self) -> None:
        home_page = HomePage.objects.get(slug="home", depth=2)
        home_page.add_child(
            instance=CourseDetailPage(
                title="Course details",
                slug="course-details",
                uni_site_links_header="Visit {{institution_name}}",
            )
        )

    def _fake_http_send(self, request: PreparedRequest, **kwargs: Any) -> Response:
        url = request.url
        if url is None:
            raise AssertionError("Unexpected outbound HTTP request without a URL")
        self.outbound_urls.append(url)

        payload: dict[str, str] | list[dict[str, str]]
        if url.endswith("/version.json"):
            payload = {"version": self.remote_version}
        elif url.endswith("/institutions_en.json") or url.endswith("/institutions_cy.json"):
            payload = [{"name": "Example Institution"}]
        elif url.endswith("/institutions/10000055/courses/AB20/modes/1"):
            course_response_factory = cast(
                Callable[[], Response],
                CourseMocks.get_successful_course_load_response,
            )
            response = course_response_factory()
            response.url = url
            response.request = request
            return response
        else:
            raise AssertionError(f"Unexpected outbound HTTP request: {url}")

        response = Response()
        response.status_code = 200
        response._content = json.dumps(payload).encode("utf-8")
        response.encoding = "utf-8"
        response.url = url
        response.request = request
        return response

    def _measure_request(self, path: str) -> tuple[HttpResponse, tuple[str, ...], int, str]:
        self.outbound_urls.clear()
        with CaptureQueriesContext(connection) as queries:
            started_at = perf_counter()
            response = self.client.get(path)
            elapsed_ms = (perf_counter() - started_at) * 1000

        profile = (
            f"outbound URLs={self.outbound_urls!r}; "
            f"DB queries={len(queries)}; elapsed={elapsed_ms:.1f}ms"
        )
        return response, tuple(self.outbound_urls), len(queries), profile

    def test_course_details_cold_request_loads_successfully_and_calls_course_api_once(self) -> None:
        response, outbound_urls, _, profile = self._measure_request(COURSE_DETAIL_PATH)

        self.assertEqual(response.status_code, 200, profile)
        course_api_calls = [url for url in outbound_urls if "/courses/AB20/modes/1" in url]
        self.assertLessEqual(len(course_api_calls), 1, profile)

    def test_course_details_warm_request_stays_within_network_and_query_budgets(self) -> None:
        initial_response = self.client.get(COURSE_DETAIL_PATH)
        self.assertEqual(initial_response.status_code, 200)

        response, outbound_urls, query_count, profile = self._measure_request(COURSE_DETAIL_PATH)

        self.assertEqual(response.status_code, 200, profile)
        self.assertLessEqual(len(outbound_urls), MAX_OUTBOUND_HTTP_CALLS_WARM, profile)
        self.assertLessEqual(query_count, MAX_DB_QUERIES_WARM, profile)

    def test_home_warm_request_stays_within_network_and_query_budgets(self) -> None:
        initial_response = self.client.get(HOME_PATH)
        self.assertEqual(initial_response.status_code, 200)

        response, outbound_urls, query_count, profile = self._measure_request(HOME_PATH)

        self.assertEqual(response.status_code, 200, profile)
        self.assertLessEqual(len(outbound_urls), MAX_OUTBOUND_HTTP_CALLS_WARM, profile)
        self.assertLessEqual(query_count, MAX_DB_QUERIES_WARM, profile)

    def test_home_reloads_institutions_once_after_data_release(self) -> None:
        self.remote_version = "release-2"

        first_response, first_outbound_urls, _, first_profile = self._measure_request(HOME_PATH)
        self.assertEqual(first_response.status_code, 200, first_profile)
        self.assertTrue(
            any(url.endswith("/institutions_en.json") for url in first_outbound_urls),
            first_profile,
        )
        self.assertTrue(
            any(url.endswith("/institutions_cy.json") for url in first_outbound_urls),
            first_profile,
        )

        response, outbound_urls, _, profile = self._measure_request(HOME_PATH)

        self.assertEqual(response.status_code, 200, profile)
        self.assertLessEqual(len(outbound_urls), MAX_OUTBOUND_HTTP_CALLS_WARM, profile)
