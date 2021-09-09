from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from post_office.models import Email


class SmsLog(models.Model):
    phones = models.CharField(max_length=512)
    template = models.CharField(max_length=128)
    params = models.CharField(max_length=2048)
    sign_name = models.CharField(max_length=128)
    send_result = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("SMS Log")
        verbose_name_plural = _("SMS Logs")


class BatchEmail(Email):
    class Meta:
        proxy = True
        # verbose_name = _("Batch Email")
        # verbose_name_plural = _("Batch Email")


class ImportLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='+')
    file_name = models.CharField(max_length=128)
    resource_cls = models.CharField(max_length=128)
    totals = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Import Log")
        verbose_name_plural = _("Import Logs")


class WechatMsgLog(models.Model):
    openid = models.CharField(max_length=32)
    template = models.CharField(max_length=128)
    url = models.CharField(max_length=1024, blank=True, null=True)
    data = models.CharField(max_length=2048)
    send_result = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wechat Log")
        verbose_name_plural = _("Wechat Logs")


class MobileLocation(models.Model):
    num = models.PositiveBigIntegerField("号段", unique=True)
    province = models.CharField("省", max_length=64)
    city = models.CharField("市", max_length=128)
    isp = models.CharField("运营商", max_length=64, blank=True)
    area_code = models.CharField("区域编码", max_length=64, blank=True)
    city_code = models.CharField("区号", max_length=64, blank=True)
    zip_code = models.CharField("邮政编码", max_length=64, blank=True)
    types = models.CharField("类型", max_length=64, blank=True)

    class Meta:
        verbose_name = _("Mobile Location")
        verbose_name_plural = _("Mobile Locations")
