from corsheaders.signals import check_request_enabled


def cors_allow_widget_to_everyone(sender, request, **kwargs):
    return request.path.startswith('/widget/')


check_request_enabled.connect(cors_allow_widget_to_everyone)
