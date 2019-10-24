from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def widget_iframe(request, uk_prn, kis_course_id, optional_1=None, optional_2=None, optional_3=None):
    optional_params = [optional_1, optional_2, optional_3]
    orientation = 'vertical'
    language = 'en-GB'
    kis_mode = 'FullTime'

    for param in optional_params:
        if param:
            if param.lower() == 'horizontal' or param.lower() == 'vertical' or param.lower() == 'responsive':
                orientation = param
            if param.lower() == 'en-gb' or param.lower() == 'cy-gb':
                language = param
            if param.lower() == 'FullTime' or param.lower() == 'PartTime':
                kis_mode = param
    context = {
        'uk_prn': uk_prn,
        'kis_course_id': kis_course_id,
        'orientation': orientation,
        'language': language,
        'kis_mode': kis_mode,
        'size': 'small',
    }

    return render(request, 'widget/iframe_widget.html', context)


def widget_embed(request):
    with open('./widget/static/css/widget.css', 'r') as styling:
        css = styling.read()

    if not css:
        return HttpResponseNotFound('File not found')

    compressed_css = css.replace('\n', '')

    with open('./widget/static/js/widget.js', 'r') as file:
        script = file.read()

    if not script:
        return HttpResponseNotFound('File not found')

    final_script = script.replace('{% styles %}', compressed_css)
    final_script = final_script.replace('{{api_domain}}', settings.WIDGETAPIHOST)
    final_script = final_script.replace('{{api_key}}', settings.WIDGETAPIKEY)
    final_script = final_script.replace('{{domain_name}}', request.site.root_url)

    return HttpResponse(final_script, content_type='application/javascript')
