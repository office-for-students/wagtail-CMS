from django.urls import path

from v2_widget.views import configurator_view
from v2_widget.views import v2_api
from v2_widget.views import v2_widget_embed
from v2_widget.views import v2_widget_placeholder_embed

urlpatterns = [
    path('configurator/', configurator_view, name='v2_widget_configurator'),
path('configurator/guidance', configurator_view, name='v2_widget_configurator_guidance'),
    path('<placeholder>/<lang>', v2_widget_placeholder_embed, name='v2_widget_embed_placeholder'),
    path('<institution>/<course>/<mode>/<lang>', v2_widget_embed, name='v2_widget_embed'),
    path('api/<uni_id>/<course_id>/<mode>/<first_stat>/<second_stat>/<third_stat>', v2_api, name='v2_widget_api'),
]