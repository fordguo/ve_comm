import re


class MarketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pk_campaign = request.GET.get('pk_campaign')
        pk_source = request.GET.get('pk_source')
        if pk_campaign or pk_source:
            if pk_campaign:
                request.session['pk_campaign'] = pk_campaign
            else:
                request.session.pop('pk_campaign', None)
            if pk_source:
                request.session['pk_source'] = pk_source
            else:
                request.session.pop('pk_source', None)

            pk_kwd = request.GET.get('pk_kwd')
            if pk_kwd:
                request.session['pk_kwd'] = pk_kwd
            else:
                request.session.pop('pk_kwd', None)
            pk_content = request.GET.get('pk_content')
            if pk_content:
                request.session['pk_content'] = pk_content
            else:
                request.session.pop('pk_content', None)
            pk_medium = request.GET.get('pk_medium')
            if pk_medium:
                request.session['pk_medium'] = pk_medium
            else:
                request.session.pop('pk_medium', None)
        response = self.get_response(request)
        return response


_ua_pattern = re.compile(r'.*(micromessenger|webbrowser).*')


class WechatUserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        openid = request.GET.get('openid')
        if openid:
            request.session['openid'] = openid
        ua = request.user_agent
        # print(dir(ua), ua.ua_string)
        # print(ua.browser, ua.device)
        ua.is_wechat = False
        if ua.is_mobile or ua.is_tablet:
            ua_str = ua.ua_string.lower()
            if ua_str.find('micromessenger') != -1 or ua_str.find('webbrowser') != -1:
                ua.is_wechat = True
        return self.get_response(request)
