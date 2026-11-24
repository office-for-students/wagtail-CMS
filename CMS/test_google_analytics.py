"""Regression tests for Google Analytics consent wiring (base.html -> cookie.js).

GA stopped reporting because the site still used a Universal Analytics (UA-*) ID, which Google
no longer processes. These tests pin the GA4 ID plumbing and run cookie.js's behaviour tests.
"""

import json
import os
import shutil
import subprocess  # nosec B404 - runs the local Node test runner with fixed arguments only
from pathlib import Path
from typing import Any
from unittest import SkipTest
from unittest.mock import patch

from django.core.cache import cache
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest, Response

from CMS.context_processors import environment
from institutions.models import InstitutionList

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_TEMPLATE = PROJECT_ROOT / "CMS" / "templates" / "base.html"
COOKIE_JS = PROJECT_ROOT / "cookie" / "static" / "cookie.js"
COOKIE_JS_TESTS = PROJECT_ROOT / "cookie" / "js_tests"
GA4_ID = "G-9XTF7DN7MG"
LEGACY_UA_ID = "UA-147556197-1"


def _fake_http_send(adapter: HTTPAdapter, request: PreparedRequest, **kwargs: Any) -> Response:
    """Stands in for HTTPAdapter.send so rendering a page never touches the network."""
    url = request.url or ""
    payload: Any
    if url.endswith("/version.json"):
        payload = {"version": "release-1"}
    elif url.endswith(("/institutions_en.json", "/institutions_cy.json")):
        payload = [{"name": "Example Institution"}]
    else:
        raise AssertionError(f"Unexpected outbound HTTP request: {url}")
    response = Response()
    response.status_code = 200
    response._content = json.dumps(payload).encode("utf-8")
    response.encoding = "utf-8"
    response.url = url
    response.request = request
    return response


class EnvironmentContextProcessorTests(SimpleTestCase):
    @override_settings(GOOGLE_ANALYTICS_ID="G-TEST123")
    def test_exposes_google_analytics_id_from_settings(self) -> None:
        context = environment(RequestFactory().get("/"))

        self.assertEqual(context["google_analytics_id"], "G-TEST123")
        self.assertIn("is_production", context)

    @override_settings()
    def test_missing_setting_disables_analytics(self) -> None:
        from django.conf import settings

        del settings.GOOGLE_ANALYTICS_ID
        context = environment(RequestFactory().get("/"))

        self.assertEqual(context["google_analytics_id"], "")


class AnalyticsSourceTests(SimpleTestCase):
    def test_legacy_universal_analytics_id_is_gone(self) -> None:
        for path in (BASE_TEMPLATE, COOKIE_JS):
            with self.subTest(path=path.name):
                self.assertNotIn(LEGACY_UA_ID, path.read_text(encoding="utf-8"))

    def test_cookie_js_defaults_to_ga4_id(self) -> None:
        self.assertIn(f'const DEFAULT_GA_ID = "{GA4_ID}";', COOKIE_JS.read_text(encoding="utf-8"))


class BaseTemplateAnalyticsTests(TestCase):
    """Renders the home page through base.html with outbound HTTP faked."""

    def setUp(self) -> None:
        cache.clear()
        patcher: Any
        for patcher in (
            patch.object(HTTPAdapter, "send", new=_fake_http_send),
            patch.dict(os.environ, {"JSONFILES_STORAGE_CONTAINER": "https://storage.example.test"}),
            patch.object(InstitutionList, "version", "release-0"),
            patch.object(InstitutionList, "options", {"en": [], "cy": []}),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

        settings_patcher = override_settings(
            DATASETAPIHOST="https://dataset.example.test",
            DATASETAPIKEY="test-api-key-not-real",
            JSONFILES_STORAGE_CONTAINER="https://storage.example.test",
            LOCAL="False",
        )
        settings_patcher.enable()
        self.addCleanup(settings_patcher.disable)

    def _home_html(self) -> str:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        content: bytes = response.content
        return content.decode("utf-8")

    @override_settings(GOOGLE_ANALYTICS_ID=GA4_ID)
    def test_ga4_id_is_passed_to_cookie_js(self) -> None:
        html = self._home_html()

        self.assertRegex(html, rf'<script[^>]*cookie\.js[^>]*\s+data-ga-id="{GA4_ID}"[^>]*defer')

    @override_settings(GOOGLE_ANALYTICS_ID=GA4_ID)
    def test_gtag_is_not_loaded_before_consent(self) -> None:
        html = self._home_html()

        self.assertNotIn("googletagmanager.com/gtag/js", html)
        self.assertNotIn(LEGACY_UA_ID, html)

    @override_settings(GOOGLE_ANALYTICS_ID='"><script>alert(1)</script>')
    def test_ga_id_is_html_escaped(self) -> None:
        html = self._home_html()

        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn('data-ga-id="&quot;&gt;&lt;script&gt;', html)

    @override_settings(GOOGLE_ANALYTICS_ID="")
    def test_empty_setting_renders_empty_attribute_which_disables_analytics(self) -> None:
        self.assertIn('data-ga-id=""', self._home_html())


class CookieJsBehaviourTests(SimpleTestCase):
    """Runs cookie/js_tests with Node's built-in test runner (no npm dependencies)."""

    def test_cookie_js_behaviour(self) -> None:
        node = shutil.which("node")
        if node is None:
            raise SkipTest("Node.js is not installed; run `node --test cookie/js_tests/` where it is available")

        # Fixed argv, no shell, no user input.
        result = subprocess.run(  # noqa: S603  # nosec B603
            [node, "--test", str(COOKIE_JS_TESTS)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
