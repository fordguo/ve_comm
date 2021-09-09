import logging
import requests
from django.conf import settings

from .models import MobileLocation

logger = logging.getLogger(__name__)


def query_mobile_location(mobile):
    mlen = len(mobile)
    num = 0
    if mlen == 11:
        num = int(mobile[0:8])
    elif mlen == 13:
        num = int(mobile[2:10])
    elif mlen == 14:
        num = int(mobile[3:11])
    else:
        logger.error(f"wrong mobile{mobile}")
        return None
    try:
        return MobileLocation.objects.get(num=num)
    except MobileLocation.DoesNotExist:
        url = "https://hcapi02.api.bdymkt.com/mobile"
        params = {"mobile": mobile}
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-Bce-Signature": f"AppCode/{settings.BD_API['MOBILE_LOCATION']['APP_CODE']}"
        }
        resp = requests.get(url, params=params, headers=headers, verify=False)
        print(resp.text)
        resj = resp.json()
        print(resj)
        if resj["code"] == 200:
            data = resj['data']
            ml = MobileLocation.objects.create(
                num=data['num'], province=data['prov'], city=data['city'],
                area_code=data['area_code'], city_code=data['city_code'], zip_code=data['zip_code'],
                isp=data['isp'], types=data['types'])
            return ml
        else:
            logger.error(f"{mobile} with error:{resp.text}")
            return None
