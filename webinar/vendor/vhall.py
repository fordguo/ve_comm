import hashlib
import time
from django.conf import settings


def md5_sign(params):
    params['app_key'] = settings.VHALL['appKey']
    secret_key = settings.VHALL['secretKey']
    arg_list = [secret_key]
    for k in sorted(params.keys()):
        arg_list.append(k)
        arg_list.append(params[k])
    arg_list.append(secret_key)
    params['sign'] = hashlib.md5(''.join(str(x)
                                         for x in arg_list).encode()).hexdigest()
    return params


def api_md5_sign(params):
    params['sign_type'] = 0  # MD5
    params['signed_at'] = int(time.time())
    return md5_sign(params)


def js_md5_sign(params):
    params['signedat'] = int(time.time())
    return md5_sign(params)
