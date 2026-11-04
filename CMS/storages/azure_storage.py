"""Custom storage backends for Azure Blob Storage."""

import os
from typing import Any

from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):  # type: ignore[misc]
    """Storage backend for media files stored in Azure Blob Storage.

    Dynamically reads container, account name, and account key from Django settings
    or environment variables.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "azure_container" not in kwargs:
            container = getattr(settings, "AZURE_CONTAINER", None) or os.environ.get("AZURE_CONTAINER")
            if container:
                kwargs["azure_container"] = container
        if "account_name" not in kwargs:
            account_name = getattr(settings, "AZURE_ACCOUNT_NAME", None) or os.environ.get("AZURE_ACCOUNT_NAME")
            if account_name:
                kwargs["account_name"] = account_name
        if "account_key" not in kwargs:
            account_key = getattr(settings, "AZURE_ACCOUNT_KEY", None) or os.environ.get("AZURE_ACCOUNT_KEY")
            if account_key:
                kwargs["account_key"] = account_key
        super().__init__(*args, **kwargs)


class AzureStaticStorage(AzureStorage):  # type: ignore[misc]
    """Deprecated: Static files are served via WhiteNoise from the website domain."""

    location = "static"
