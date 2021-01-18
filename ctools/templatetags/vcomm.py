from django import template
from django.templatetags import static
from django.conf import settings
from datetime import date

register = template.Library()


@register.simple_tag
def vstatic(path):
    url = static.static(path)
    static_version = getattr(settings, 'STATIC_VERSION', f'{date.today()}')
    return f'{url}?v={static_version}'
