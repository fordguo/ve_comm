from django.conf import settings
from django.db import models

from post_office.models import Email


class SmsLog(models.Model):
    phones = models.CharField(max_length=512)
    template = models.CharField(max_length=128)
    params = models.CharField(max_length=2048)
    sign_name = models.CharField(max_length=128)
    send_result = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)


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
        verbose_name = "Import Log"
        verbose_name_plural = "Import Logs"
