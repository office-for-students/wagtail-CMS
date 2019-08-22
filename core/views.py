import json

from django.http import JsonResponse

from core.request_handler import send_feedback


def submit_feedback(request):
    post_body = request.POST
    feedback_obj = {'questions': []}
    for key, value in post_body.items():
        if key == 'is_useful':
            feedback_obj[key] = value == 'yes'
        elif key == 'page':
            feedback_obj[key] = value
        elif key != 'csrfmiddlewaretoken':
            feedback_obj.get('questions').append({
                'title': key,
                'feedback': value
            })

    response = send_feedback(json.dumps(feedback_obj))

    if response.ok:
        response_body = {}
    else:
        response_body = response.json()
    return JsonResponse(response_body, status=response.status_code)
