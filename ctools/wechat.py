from os import path
import json
import logging
from django.conf import settings
from django.shortcuts import redirect

import requests

from .models import WeixinMsgLog

logger = logging.getLogger(__name__)


def redirect_wechat(request):
    # TODO: build_absolute_uri，对于https的url，返回的是http
    # https://djangodeployment.com/2017/01/24/fix-djangos-https-redirects-nginx/ 这个配置无效，可能跟SLB有关
    path_info = request.get_full_path_info()
    if settings.BASE_URL[-1] == '/' and path_info[0] == '/':
        target = f"{settings.BASE_URL}{path_info[1:]}"
    else:
        target = f"{settings.BASE_URL}{path_info}"
    # request.build_absolute_uri()
    url = f'{settings.WECHAT_H5_URL}?appid={settings.WECHAT_APPID}&target={target}'
    print(url)
    return redirect(url)


def check_wechat(request):
    return request.user_agent.is_wechat and not bool(request.session.get('openid'))


with open(path.join(path.dirname(__file__), 'message_templates.json'), encoding="utf-8") as f:
    TEMPLATES = {t['template_id']: t for t in json.load(f)}
if hasattr(settings, "WECHAT_TEMPLATES"):
    for t in settings.WECHAT_TEMPLATES:
        TEMPLATES[t['template_id']] = t


def send_msg(openid: str, template_id: str, data, link_url='', verify_templateid=False):
    # https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html

    if openid and openid.strip() != '':
        if verify_templateid and not settings.DEBUG and template_id not in TEMPLATES:
            logger.error(f'invalid template_id:{template_id}')
            return
        url = f'{settings.WECHAT_UCP_URL}/cgi-bin/message/template/send?appid={settings.WECHAT_APPID}&apikey={settings.WECHAT_UCP_KEY}'
        headers = {'Content-Type': 'application/json'}
        params = {'touser': openid, 'template_id': template_id,
                  'url': link_url, 'data': data}
        res = requests.post(url=url, headers=headers, json=params)
        if res.status_code == 200:
            send_result = {'status': res.status_code, 'json': res.json()}
        else:
            send_result = {'status': res.status_code}
        WeixinMsgLog.objects.create(
            openid=openid, template=template_id,
            url=link_url,
            data=data, send_result=str(send_result)
        )
    else:
        logger.error(
            f'wrong arguments:openid={openid},template_id={template_id}')
