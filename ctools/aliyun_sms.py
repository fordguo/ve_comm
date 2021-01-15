from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
from .models import SmsLog


def send_sms(phones, sign_name, template_code, region='cn-shanghai', **params):
    # region:cn-hangzhou,cn-shanghai
    # https://help.aliyun.com/document_detail/31837.html?spm=a2c4g.11186623.6.585.8bff58d5wf0TKC

    client = AcsClient(settings.OSS_ACCESS_KEY_ID,
                       settings.OSS_ACCESS_KEY_SECRET, region)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', region)
    strphones = ','.join(phones)
    request.add_query_param('PhoneNumbers', strphones)
    request.add_query_param('SignName', sign_name,)
    request.add_query_param('TemplateCode', template_code)
    strparams = json.dumps(params)
    request.add_query_param('TemplateParam', strparams)

    response = client.do_action_with_exception(request)
    SmsLog.objects.create(
        phones=strphones, sign_name=sign_name, template=template_code, params=strparams, send_result=response)
