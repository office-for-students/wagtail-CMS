import json

from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render

from CMS.settings.base import ROOT_DOMAIN
from core.request_handler import (
    get_json_file,
    get_sitemap_file,
    send_feedback,
)
from institutions.utils import load_institution_json


def submit_feedback(request):
    post_body = request.POST

    # Always returns is_useful True as this field is required by the API but no longer in the form
    feedback_obj = {
        'is_useful': True,
        'questions': [],
    }
    for key, value in post_body.items():
        if key == 'page':
            feedback_obj[key] = value
        elif key == 'user_feedback':
            feedback_obj.get('questions').append(
                {
                    'title': 'howwasthisuseful',
                    'feedback': value,
                },
            )
            # Always returns title howwasthisuseful as this field is expected by the API and the  current one isn't

    response = send_feedback(json.dumps(feedback_obj))

    response_body = {} if response.ok else response.json()
    return JsonResponse(response_body, status=response.status_code)


def get_subjects_json(request):
    response = get_json_file("subjects.json")

    response_body = response.json() if response.ok else {}

    return JsonResponse(response_body, status=response.status_code, safe=False)


def not_already_in_list(name, existing):
    if name not in existing:
        existing.append(name)
        return True
    return False


def get_institutions_json(request, language):
    return JsonResponse(load_institution_json()[language], status=200, safe=False)


def robots(request, **kwargs):
    return render(request, 'robots.txt', content_type='text/plain')


def sitemap_primary(request, **kwargs):
    context = {
        "root_domain": ROOT_DOMAIN,
    }
    return render(
        request=request,
        template_name='sitemap_primary.xml',
        context=context,
        content_type='text/xml',
    )


def content_sitemap(request, **kwargs):
    response = get_sitemap_file()

    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type='text/xml',
    )
