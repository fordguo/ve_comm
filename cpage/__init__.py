from django.conf import settings


def oss_special_url(category, name, suffix, fmt='mp4'):
    if suffix and suffix[0] != '_':
        suffix = '_'+suffix
    # http://oss.sapevent.cn/video/unplugged/001_Karlie & Alicia_1080p.mp4
    return f"{settings.OSS_URL_PREFIX}/video/{category}/{name}{suffix}.{fmt}"


def video_url(category, name, suffix='1080p'):
    return oss_special_url(category, name, suffix)


def thumbnail_url(category, name, suffix='pc'):
    return oss_special_url(category, name, suffix, 'jpg')
