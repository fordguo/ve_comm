from django.conf import settings
from django.shortcuts import redirect


def redirect_wechat(request):
    # TODO: build_absolute_uri，对于https的url，返回的是http
    # https://djangodeployment.com/2017/01/24/fix-djangos-https-redirects-nginx/ 这个配置无效，可能跟SLB有关
    url = f'{settings.WEIXIN_AUTH_URL}?appid={settings.WEIXIN_APPID}&target={request.build_absolute_uri()}'
    print(url)
    return redirect(url)


def check_wechat(request):
    return request.user_agent.is_wechat and not bool(request.session.get('openid'))
