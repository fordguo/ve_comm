from pypinyin import pinyin, Style


_DEFAULT_NAME = "SS"
OSS_URL_PREFIX = "https://oss.sapevent.cn"


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
        return f"{first[0][0][0]}{last[0][0][0]}"
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


def get_avatar_url(user):
    name = _avatar_name(user.first_name, user.last_name, user.email)
    name = _check_black_name(name)
    return f'{OSS_URL_PREFIX}/avatar/{name.upper()}_{user.id % 3}.png'


def get_default_avatar(user_id):
    return f'{OSS_URL_PREFIX}/avatar/{_DEFAULT_NAME}_{user_id % 3}.png'


if __name__ == "__main__":
    print(_avatar_name('Xs', None, None))
    print(_avatar_name('测试', None, None))
    print(_avatar_name('X ', None, None))
    print(_avatar_name('', None, None))
    print(_avatar_name('John Ford', None, None))
