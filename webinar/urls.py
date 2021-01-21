from django.urls import path

from . import ajax_views

app_name = 'webinar'
urlpatterns = [
    path('ajax-live-info/<content_type>/<int:pk>/<stream_attr>/<parent_block_type>/<parent_id>/',
         ajax_views.get_live_info),
]
