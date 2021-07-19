import hashlib
import time
from django.conf import settings


def md5_sign(params):
    params['app_key'] = settings.VHALL_APP_KEY
    params['sign_type'] = 0  # MD5
    arg_list = [settings.VHALL_SECRET_KEY]
    for k in sorted(params.keys()):
        arg_list.append(k)
        arg_list.append(params[k])
    arg_list.append(settings.VHALL_SECRET_KEY)
    params['sign'] = hashlib.md5(''.join(arg_list).encode()).hexdigest()
    return params


def api_md5_sign(params):
    params['signed_at'] = int(time.time())
    return md5_sign(params)


def js_md5_sign(params):
    params['signedat'] = int(time.time())
    return md5_sign(params)
