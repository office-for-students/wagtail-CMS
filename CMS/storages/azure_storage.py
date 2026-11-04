from storages.backends.azure_storage import AzureStorage


class AzureStaticStorage(AzureStorage):
    azure_container = "uploadedimages"
    location = "static"


class AzureMediaStorage(AzureStorage):
    azure_container = "uploadedimages"
