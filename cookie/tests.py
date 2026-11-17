from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from django.template import Context, Engine
from django.test import TestCase


class CookieBannerTemplateTests(TestCase):
    def test_cookie_settings_has_visible_status_region_and_unique_heading_id(self) -> None:
        template_dir = Path(__file__).parent / 'templates'
        engine = Engine(
            dirs=[str(template_dir)],
            libraries={'discover_uni_tags': 'core.templatetags.discover_uni_tags'},
        )
        page = SimpleNamespace(get_language='en', is_english=True)

        with patch('core.templatetags.discover_uni_tags.translations.term_for_key', return_value='Translation'):
            rendered = engine.get_template('cookie-banner.html').render(Context({'page': page}))

        self.assertIn('id="cookie-status" class="__status" role="status" aria-live="polite"', rendered)
        self.assertEqual(rendered.count('id="cookie-settings"'), 1)
        self.assertIn('aria-labelledby="cookie-settings-title"', rendered)
        self.assertIn('id="cookie-settings-title"', rendered)
