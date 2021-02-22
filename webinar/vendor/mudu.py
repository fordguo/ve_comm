from hashlib import md5
from urllib.parse import urlparse, urlunparse, parse_qs
from django.http import QueryDict
from django.conf import settings

from ctools.avatar import get_avatar_url, get_default_avatar

# MUDU_ASSIGN_URL = "http://mudu.tv/activity.php?a=userAssign"
MUDU_ASSIGN_URL = f"{settings.MUDU_ROOT}/activity.php?a=userAssign"

# http://mudu.tv/watch/5920781
MUDU_WATCH_URL = f"{settings.MUDU_ROOT}/watch/"


def get_url(channel):
    return generate_watch_url(channel.wid)


def generate_assign_url(channel, user):
    uid = user.id
    key = md5("{}{}".format(uid, channel.token).encode()).hexdigest()
    url_parts = urlparse(MUDU_ASSIGN_URL)
    queries = QueryDict(url_parts.query, mutable=True)
    queries.update({'id': channel.cid, 'userid': uid, 'name': user.get_label_name(),
                    'avatar': gen_gravatar(user), 'expire': 2147483647, 'key': key,
                    'skipWxAuth': 1})
    new_url = urlunparse((url_parts.scheme, url_parts.netloc, url_parts.path,
                          url_parts.params, queries.urlencode(), url_parts.fragment))
    return new_url


get_user_url = generate_assign_url


def generate_watch_url(watch_id):
    return f"{MUDU_WATCH_URL}/{watch_id}?skipWxAuth=1"


def gen_gravatar(user):
    try:
        return get_avatar_url(user)
    except Exception:
        return get_default_avatar(user.id)


# http://mudu.tv/watch/5920781
# http://mudu.tv/?c=activity&a=live&id=347693
# http://live.sapevent.cn/?c=activity&a=live&id=374496&referVisitorId=92034140&channel=invite_card
def parse_mudu_url(url):
    try:
        if url:
            result = urlparse(url)
            path = result.path
            params = parse_qs(result.query)
            if path.find('/watch'):
                pid = params.get('id')
                if pid:
                    return {'watch_id': pid[0]}
                return {'watch_id': path[7:]}

            cid = params.get('id')
            if cid:
                return {'channel_id': cid[0]}
    except Exception as e:
        print(f'parse_mudu_url: {url}, error: {e}')

    return None
