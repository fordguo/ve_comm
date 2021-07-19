from django.urls import path

from . import ajax_views

app_name = 'webinar'
urlpatterns = [
    path('ajax-live-info/<content_type>/<int:pk>/<stream_attr>/<parent_block_type>/<parent_id>/',
         ajax_views.ajax_get_live_info),
    path('ajax-vhall/js-md5-sign/', ajax_views.vhall_js_md5_sign),
    path('ajax-vhall/api-md5-sign/', ajax_views.vhall_api_md5_sign),
]
