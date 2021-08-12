import requests
import json
from django.conf import settings

from .models import SmsLog
# 云极短信服务

ROOT_URL = "https://market.juncdt.com/smartmarket/"


def send_sms(phones, sign_code, template_code, verify=True, **params):
    url = f"{ROOT_URL}msgService/sendMessageToMulti"
    main = settings.UC['main']
    classification = main['verify_key'] if verify else main['notifKey']
    jdata = {"accessKey": main['accessKey'],
             "accessSecret": main['accessSecret'],
             "classificationSecret": classification,
             "signCode": sign_code, "templateCode": template_code,
             "phones": phones, "params": params,
             }
    res = requests.post(url, json=jdata)
    strphones = ','.join(phones)
    strparams = json.dumps(params)
    SmsLog.objects.create(
        phones=strphones, sign_name=sign_code, template=template_code, params=strparams, send_result=res.text)


def send_internation_sms(phones, template_code, **params):
    url = f"{ROOT_URL}internationalMsg/sendMsgToMultiple"
    inter = settings.UC['internation']
    jdata = {"accessKey": inter['accessKey'],
             "accessSecret": inter['accessSecret'],
             "templateCode": template_code,
             "phones": phones, "params": params,
             }
    res = requests.post(url, json=jdata)
    strphones = ','.join(phones)
    strparams = json.dumps(params)
    SmsLog.objects.create(
        phones=strphones, sign_name='', template=template_code, params=strparams, send_result=res.text)
