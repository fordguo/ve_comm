import base64
import oss2

from django.conf import settings
from pypinyin import pinyin, Style

from . import isascii


_DEFAULT_NAME = "SS"
OSS_URL_PREFIX = f"{getattr(settings,'OSS_URL_PREFIX','')}"

DEF_AVATAR = {
    'default': {
        'bg_images': ['blue.png', 'orange.png', 'pink.png'],
        'style_fmt': 'image/watermark,text_{},type_ZmFuZ3poZW5naGVpdGk,color_FFFFFF,size_30,g_center,x_10,y_10,image/resize,w_32,h_32'
    }
}

AVATAR = getattr(settings, 'AVATAR', DEF_AVATAR)


def _check_black_name(name):
    if name in ['SB', 'BS']:
        return _DEFAULT_NAME
    return name


def _check_single_name(names):
    if len(names) > 1:
        return f"{names[0][0][0]}{names[1][0][0]}"
    elif len(names) == 1 and len(names[0][0]) >= 1:
        nm = names[0][0].strip()
        sn = nm.split(' ')
        if len(sn) > 1:
            return f"{sn[0][0]}{sn[1][0]}"
        n = nm[0:2]
        if len(n) == 1:
            n = f"{n}X"
        return n
    return _DEFAULT_NAME


def _avatar_name(first_name, last_name, email):
    # 李: [['l']]
    # Bruce Lee: [['Bruce Lee']]
    # 李四: [['l'], ['s']]
    if first_name and last_name:
        first = pinyin(first_name, style=Style.FIRST_LETTER)
        last = pinyin(last_name, style=Style.FIRST_LETTER)
        if isascii(last_name):
            return f"{first[0][0][0]}{last[0][0][0]}"
        else:
            return f"{last[0][0][0]}{first[0][0][0]}"
    elif first_name:
        first = pinyin(first_name, style=Style.FIRST_LETTER)
        return _check_single_name(first)
    elif last_name:
        last = pinyin(last_name, style=Style.FIRST_LETTER)
        return _check_single_name(last)
    elif email:
        names = email.split('@')[0].split('.')
        if len(names) > 1:
            return f'{names[0][0]}{names[-1][0]}'
        return f'{names[0][0:2]}'

    return _DEFAULT_NAME


def get_avatar_url(user, theme='default'):
    count = len(AVATAR[theme]['bg_images'])
    name = _avatar_name(user.first_name, user.last_name, user.email)
    name = _check_black_name(name)
    return f'{OSS_URL_PREFIX}/avatar/{theme}/{name.upper()}_{user.id % count}.png'


def get_default_avatar(user_id, theme='default'):
    count = len(AVATAR[theme]['bg_images'])
    return f'{OSS_URL_PREFIX}/avatar/{theme}/{_DEFAULT_NAME}_{user_id % count}.png'


def gen_avatar(bucket, name, theme='default'):
    style = AVATAR[theme]['style_fmt']
    bg_images = AVATAR[theme]['bg_images']
    bucket_name = settings.OSS_BUCKET_NAME
    encode_text = base64.urlsafe_b64encode(oss2.compat.to_bytes(name))
    style = style.format(encode_text.decode('ascii').strip('='))
    for i in range(len(bg_images)):
        target_image_name = f'avatar/{theme}/{name}_{i}.png'
        osstname = oss2.compat.to_string(base64.urlsafe_b64encode(
            oss2.compat.to_bytes(target_image_name)))
        ossbname = oss2.compat.to_string(base64.urlsafe_b64encode(
            oss2.compat.to_bytes(bucket_name)))
        process = f"{style}|sys/saveas,o_{osstname},b_{ossbname}"
        bucket.process_object(f'avatar/{theme}/bg/' + bg_images[i], process)


def get_bucket():
    auth = oss2.Auth(settings.OSS_ACCESS_KEY_ID,
                     settings.OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.OSS_ENDPOINT,
                         settings.OSS_BUCKET_NAME)
    return bucket


if __name__ == "__main__":
    print(_avatar_name('Xs', None, None))
    print(_avatar_name('测试', None, None))
    print(_avatar_name('X ', None, None))
    print(_avatar_name('', None, None))
    print(_avatar_name('John Ford', None, None))
