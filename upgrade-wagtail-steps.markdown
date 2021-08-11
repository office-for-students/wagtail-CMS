# Upgrade wagtail to 2.14 steps

## Steps to upgrade:

- Run `docker compose up`
- In a new terminal run `docker container exec -it wagtail-cms_web_1 /bin/bash`
- From docker container bash upgrade python packages `pip install --upgrade wagtail django-axes django-sass-processor whitenoise`
- Requirements.txt has been updated already

## Changes:

Wagtail 2.14 now uses Django 3.2.6.

As of Django 3.0 `staticfiles` and `admin_static` have been removed.

Any of these:

```
{% load staticfiles %}
{% load static from staticfiles %}
{% load admin_static %}
```

Have been changed to:

```
{% load static %}
```

As of Wagtail 2.9 `SiteMiddleware` and `request.site` have been deprecated. As neither is being used in the project I
have just removed the line `'wagtail.core.middleware.SiteMiddleware'` from `CMS.settings.base.py`.

If they are required at some stage there are steps in the releases notes
here that will assist: https://docs.wagtail.io/en/stable/releases/2.9.html