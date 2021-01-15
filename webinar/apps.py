from django.apps import AppConfig


class WebinarConfig(AppConfig):
    name = 'webinar'

    def ready(self):
        ...
