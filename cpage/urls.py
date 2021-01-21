from django.urls import path

from . import ajax_views

app_name = 'cpage'
urlpatterns = [
    path('ajax-float-image/<code>/', ajax_views.get_float_image),
]
