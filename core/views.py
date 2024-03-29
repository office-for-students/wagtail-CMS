import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from core.request_handler import get_json_file
from core.request_handler import get_sitemap_file
from core.request_handler import send_feedback
from institutions.utils import load_institution_json


def submit_feedback(request):
    post_body = request.POST

    # Always returns is_useful True as this field is required by the API but no longer in the form
    feedback_obj = {'is_useful': True, 'questions': []}
    for key, value in post_body.items():
        if key == 'page':
            feedback_obj[key] = value
        elif key == 'user_feedback':
            feedback_obj.get('questions').append({
                'title': 'howwasthisuseful',
                'feedback': value
            })
            # Always returns title howwasthisuseful as this field is expected by the API and the  current one isn't

    response = send_feedback(json.dumps(feedback_obj))

    if response.ok:
        response_body = {}
    else:
        response_body = response.json()
    return JsonResponse(response_body, status=response.status_code)


def get_subjects_json(request):
    response = get_json_file("subjects.json")

    if response.ok:
        response_body = response.json()
    else:
        response_body = {}

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


def sitemap_new(request, **kwargs):
    return render(request, 'sitemap_primary.xml', content_type='text/xml')


def content_sitemap(request, **kwargs):
    response = get_sitemap_file()

    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type='text/xml'
    )
