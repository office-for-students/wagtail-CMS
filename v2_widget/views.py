# Create your views here.
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

"""
test endpoint: http://127.0.0.1:8000/widget/v2/10003614/BACTSINGW9F/FullTime/en
"""
WIDGET_HOST = settings.V2_WIDGET_HOST


def configurator_view(request):
    return render(request=request, template_name='v2_widget/configurator.html', context={'WIDGET_HOST': WIDGET_HOST})


@xframe_options_exempt
@csrf_exempt
def v2_widget_embed(request, institution: str, course: str, mode: str, lang: str):
    try:
        return proxy_content(target_url=f"{WIDGET_HOST}widget/v2/{institution}/{course}/{mode}/{lang}", request=request)

    except requests.exceptions.RequestException as e:
        # TODO: check if in debug
        return HttpResponse(f"Error: {str(e)}", status=502)


@xframe_options_exempt
@csrf_exempt
def v2_widget_placeholder_embed(request, placeholder: str, lang: str):
    try:
        return proxy_content(target_url=f"{WIDGET_HOST}widget/v2/{placeholder}/{lang}", request=request)

    except requests.exceptions.RequestException as e:
        # TODO: check if in debug
        return HttpResponse(f"Error: {str(e)}", status=502)


def proxy_content(request, target_url: str, content_type="text/html"):
    print("method = ", request.method)

    headers = {
        "User-Agent": request.META.get("HTTP_USER_AGENT", "")
    }

    if request.method == "GET":
        params = request.GET.dict()
        response = requests.get(target_url, params=params, headers=headers)
    else:
        return HttpResponse("Method not allowed", status=405)

    return HttpResponse(
        content=response.content,
        status=response.status_code,
        content_type=response.headers.get("Content-Type", content_type)
    )


def v2_api(
        request,
        uni_id: str,
        course_id: str,
        mode: str,
        first_stat: str,
        second_stat: str,
        third_stat: str
):
    try:
        return proxy_content(
            target_url=f"{WIDGET_HOST}widget/v2/api/{uni_id}/{course_id}/{mode}/{first_stat}/{second_stat}/{third_stat}",
            request=request,
            content_type="application/json"
        )

    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error: {str(e)}", status=502)