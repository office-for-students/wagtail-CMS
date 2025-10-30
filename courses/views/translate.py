import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from CMS import translations
from core.request_handler import is_ajax


@csrf_exempt
def get_translations(request):
    if is_ajax(request):
        if request.method == 'POST':
            response = []
            body = json.loads(request.body.decode('utf-8'))
            # print("body as json = ", body)
            language = body['language']
            if len(body['terms']) > 25:
                raise Exception("to big")
            terms = body['terms']
            for key in terms:
                response.append(translations.term_for_key(key, language=language))

            return JsonResponse(response, safe=False)

    return HttpResponse("invalid", status=400)