import importlib
import os
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from CMS.storages.azure_storage import AzureMediaStorage, AzureStaticStorage


class StoragesConfigurationTests(TestCase):  # type: ignore[misc]
    def test_azure_media_storage_resolves_from_settings(self) -> None:
        with patch.object(settings, "AZURE_CONTAINER", "test-container", create=True), \
             patch.object(settings, "AZURE_ACCOUNT_NAME", "testaccount", create=True), \
             patch.object(settings, "AZURE_ACCOUNT_KEY", "fakekey123==", create=True):
            storage = AzureMediaStorage()
            self.assertEqual(storage.azure_container, "test-container")
            self.assertEqual(storage.account_name, "testaccount")
            self.assertEqual(storage.account_key, "fakekey123==")

    def test_azure_media_storage_resolves_from_env(self) -> None:
        with patch.dict(os.environ, {
            "AZURE_CONTAINER": "env-container",
            "AZURE_ACCOUNT_NAME": "envaccount",
            "AZURE_ACCOUNT_KEY": "envkey==",
        }):
            storage = AzureMediaStorage()
            self.assertEqual(storage.azure_container, "env-container")
            self.assertEqual(storage.account_name, "envaccount")
            self.assertEqual(storage.account_key, "envkey==")

    def test_azure_media_storage_accepts_explicit_kwargs(self) -> None:
        storage = AzureMediaStorage(
            azure_container="custom-container",
            account_name="customaccount",
            account_key="customkey",
        )
        self.assertEqual(storage.azure_container, "custom-container")
        self.assertEqual(storage.account_name, "customaccount")
        self.assertEqual(storage.account_key, "customkey")

    def test_azure_static_storage_location(self) -> None:
        storage = AzureStaticStorage(
            account_name="dummy",
            account_key="dummy",
            azure_container="dummy",
        )
        self.assertEqual(storage.location, "static")

    def test_dev_settings_storages(self) -> None:
        from CMS.settings import dev

        self.assertEqual(
            dev.STORAGES["default"]["BACKEND"],
            "django.core.files.storage.FileSystemStorage",
        )
        self.assertEqual(
            dev.STORAGES["staticfiles"]["BACKEND"],
            "django.contrib.staticfiles.storage.StaticFilesStorage",
        )
        self.assertEqual(dev.STATIC_URL, "/static/")

    def test_base_settings_storages(self) -> None:
        from CMS.settings import base

        self.assertEqual(
            base.STORAGES["default"]["BACKEND"],
            "django.core.files.storage.FileSystemStorage",
        )
        self.assertEqual(
            base.STORAGES["staticfiles"]["BACKEND"],
            "whitenoise.storage.CompressedStaticFilesStorage",
        )
        self.assertEqual(base.STATIC_URL, "/static/")

    def test_whitenoise_compressed_static_files_storage_url(self) -> None:
        from whitenoise.storage import CompressedStaticFilesStorage

        storage = CompressedStaticFilesStorage()
        url = storage.url("search_app/homepage_search/app-search-only-styles.css")
        self.assertEqual(url, "/static/search_app/homepage_search/app-search-only-styles.css")

    def test_pre_production_settings_storages(self) -> None:
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "AZURE_ACCOUNT_NAME": "teststorage",
            "AZURE_ACCOUNT_KEY": "testkey",
            "AZURE_CONTAINER": "testmedia",
        }):
            pre_prod_mod = importlib.import_module("CMS.settings.pre-production")
            importlib.reload(pre_prod_mod)

            self.assertEqual(
                pre_prod_mod.STORAGES["default"]["BACKEND"],
                "CMS.storages.azure_storage.AzureMediaStorage",
            )
            self.assertEqual(
                pre_prod_mod.STORAGES["staticfiles"]["BACKEND"],
                "whitenoise.storage.CompressedStaticFilesStorage",
            )
            self.assertEqual(pre_prod_mod.STATIC_URL, "/static/")
            self.assertEqual(
                pre_prod_mod.MEDIA_URL,
                "https://teststorage.blob.core.windows.net/testmedia/",
            )

    def test_production_settings_storages(self) -> None:
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "AZURE_ACCOUNT_NAME": "prodstorage",
            "AZURE_ACCOUNT_KEY": "prodkey",
            "AZURE_CONTAINER": "prodmedia",
        }):
            import CMS.settings.production as prod_mod
            importlib.reload(prod_mod)

            self.assertEqual(
                prod_mod.STORAGES["default"]["BACKEND"],
                "CMS.storages.azure_storage.AzureMediaStorage",
            )
            self.assertEqual(
                prod_mod.STORAGES["staticfiles"]["BACKEND"],
                "whitenoise.storage.CompressedStaticFilesStorage",
            )
            self.assertEqual(prod_mod.STATIC_URL, "/static/")
            self.assertEqual(
                prod_mod.MEDIA_URL,
                "https://prodstorage.blob.core.windows.net/prodmedia/",
            )
