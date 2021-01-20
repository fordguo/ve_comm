from django.db import models
from django.utils.translation import gettext_lazy as _

from .vendor import mudu, gensee


class LiveVendor(models.TextChoices):
    MUDU = "mudu", _("Mudu")
    GENSEE = "gensee", _("Geensee")
    EXT_URL = "ext_url", _("External URL")
    SELF = "self", _("Self")
    POLYV = "polyv", _("Polyv")


class ChannelType(models.TextChoices):
    LIVE = "live", "Live"
    DEMAND = "demand", "Demand"


def get_channel_url(channel):
    # 根据vendor不同类型，获取去目的的URL。对于self类型，就是会议PRE和POST配置的页面ID
    if channel.vendor == LiveVendor.MUDU:
        return mudu.get_url(channel)
    elif channel.vendor == LiveVendor.GENSEE:
        return gensee.get_url(channel)
    # TODO(self) 处理self类型
    return channel.wid


def get_user_channel_url(channel, user):
    if user:
        if channel.vendor == LiveVendor.MUDU:
            # mudu ondemand 不需要身份赋予
            if not channel.token:
                return mudu.get_url(channel)
            return mudu.get_user_url(channel, user)
        elif channel.vendor == LiveVendor.GENSEE:
            return gensee.get_user_url(channel, user)
    return get_channel_url(channel)
