from django.conf import settings
from django.http import QueryDict


def get_url(channel):
    if channel.is_live:
        return f'{settings.GENSEE_URL}/webcast/site/entry/join-{channel.wid}'
    else:
        return f'{settings.GENSEE_URL}/webcast/site/vod/play-{channel.wid}'


def get_user_url(channel, user):
    params = QueryDict(mutable=True)
    params.update(uid=f'1000000000{user.id}', nickName=user.get_label_name(
    ), company='null', email='null', mobile='null')
    if channel.token:
        params['token'] = channel.token
    return f'{get_url(channel)}?{params.urlencode()}'
