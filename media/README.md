# Introduction

These files are he because they are used in testing

### What do you mean they are used in testing? They are just images

The storage backend for Azure deployments is `Azure Storage Accounts`. Now when running tests the loading of certain pages fails because it can't get the images for the page from the storage backend.

### But shouldn't this fail gracefully? (i.e. if the images are not there then it's just an empty image tag?)

That would be what would normally happen but unfortunately there are a number of variables *(in templates)* that use the wagtail specific tag `{{ ...|richtext }}`. This tag uses [django's storage library](https://docs.djangoproject.com/en/3.1/ref/files/storage/) to find where media files *(mostly image files)* are located *(and route the requests to them accordingly)*. This library in turn has been replaced by [django-storages](https://github.com/jschneier/django-storages) library *(found in the [requirements.txt](https://github.com/office-for-students/wagtail-CMS/blob/develop/requirements.txt#L27))*. In deployed environment this is set to Azure `Storage Accounts`. You can find the code [here](https://github.com/office-for-students/wagtail-CMS/blob/develop/CMS/settings/base.py#L219).

### So with the image files here pages will load for tests to run?

Exactly.
