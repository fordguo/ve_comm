from django import template
from django.templatetags import static
from django.conf import settings
from datetime import date, datetime

register = template.Library()


@register.simple_tag
def vstatic(path):
    url = static.static(path)
    static_version = getattr(settings, 'STATIC_VERSION', f'{date.today()}')
    return f'{url}?v={static_version}'


@register.inclusion_tag('lib_tags/matomo.html')
def matomo_config():
    return {
        "matomo_host": getattr(settings, "MATOMO_HOST"),
        "matomo_site_id": getattr(settings, "MATOMO_SITE_ID"),
    }


@register.inclusion_tag('lib_tags/wechat_share.html')
def wechat_share_config(title, desc, link=None, image="default.png"):
    oss_root = getattr(settings, "OSS_URL_PREFIX")
    return {
        "wechat_appid": getattr(settings, "WECHAT_APPID"),
        "wechat_sid": getattr(settings, "WECHAT_SID"),
        "wechat_debug": bool(getattr(settings, "WECHAT_SHARE_DEBUG", False)),
        "wechat_signature_url": getattr(settings, "WECHAT_SIGNATURE_URL"),
        "wechat_h5_url": getattr(settings, "WECHAT_H5_URL"),
        "share_title": title,
        "share_desc": desc,
        "share_link": link or getattr(settings, "WECHAT_DEFAULT_LINK"),
        "share_image": f'{oss_root}/wechat_share/{image}',
        "noncestr": f've-{datetime.now().timestamp()}',
    }
