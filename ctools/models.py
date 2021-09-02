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
