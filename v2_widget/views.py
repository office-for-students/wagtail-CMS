from django.shortcuts import render

# Create your views here.
import requests
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
"""
test endpoint: http://127.0.0.1:8000/widget/v2/10003614/BACTSINGW9F/FullTime/en
"""
WIDGET_HOST = settings.V2_WIDGET_HOST

def configurator_view(request):
    return render(request=request, template_name='v2_widget/configurator.html', context={'WIDGET_HOST': WIDGET_HOST})


@xframe_options_exempt
@csrf_exempt
def v2_widget_embed(request, institution:str, course:str, mode:str, lang:str):
    try:
       return proxy_content(target_url=f"{WIDGET_HOST}widget/v2/{institution}/{course}/{mode}/{lang}",request=request)

    except requests.exceptions.RequestException as e:
        # TODO: check if in debug
        return HttpResponse(f"Error: {str(e)}", status=502)



@xframe_options_exempt
@csrf_exempt
def v2_widget_placeholder_embed(request, placeholder:str, lang:str):
    try:
        return proxy_content(target_url=f"{WIDGET_HOST}widget/v2/{placeholder}/{lang}", request=request)

    except requests.exceptions.RequestException as e:
        # TODO: check if in debug
        return HttpResponse(f"Error: {str(e)}", status=502)



def proxy_content(request, target_url:str):
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
        content_type=response.headers.get("Content-Type", "text/html")
    )