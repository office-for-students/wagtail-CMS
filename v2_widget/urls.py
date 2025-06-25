from django.urls import path

from v2_widget.views import configurator_view
from v2_widget.views import v2_api_institution_courses
from v2_widget.views import v2_api_institutions
from v2_widget.views import v2_widget_embed
from v2_widget.views import v2_widget_placeholder_embed

urlpatterns = [
    path('configurator/', configurator_view, name='v2_widget_configurator'),
    path('configurator/guidance', configurator_view, name='v2_widget_configurator_guidance'),
    path('configurator/help', configurator_view, name='v2_widget_configurator_help'),
    path('configurator/privacy', configurator_view, name='v2_widget_configurator_privacy'),
    path('<placeholder>/<lang>', v2_widget_placeholder_embed, name='v2_widget_embed_placeholder'),
    path('api/all_institutions/', v2_api_institutions, name='v2_widget_api_institutions'),
    path('api/institution/<institution>/courses', v2_api_institution_courses, name='v2_widget_api_courses'),
    path('<institution>/<course>/<mode>/<lang>', v2_widget_embed, name='v2_widget_embed'),
]