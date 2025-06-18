from django.urls import path


from widget.views.v2_views import v2_widget_embed
from widget.views.v2_views import v2_widget_placeholder_embed

urlpatterns = [
    path('<placeholder>/<lang>', v2_widget_placeholder_embed, name='v2_widget_embed_placeholder'),
    path('<institution>/<course>/<mode>/<lang>', v2_widget_embed, name='v2_widget_embed'),
]