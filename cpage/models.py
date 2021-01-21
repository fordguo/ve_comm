from django.conf import settings
from django.shortcuts import redirect
from django.db import models
from django.core.cache import cache

from .snippet import *

from wagtail.core.models import Page
from cmedia.models import BaseMediaInfo

# Create your models here.


class BaseSummitEnrollmentQuerySet(models.QuerySet):
    def is_enrolled(self, user, code):
        if not user.is_authenticated:
            return False
        key = f'summit_enroll_{user.id}_{code}'
        res = cache.get(key)
        if res is None:
            res = self.model.objects.filter(
                user=user, summit_code=code).exists()
            if res:
                cache.set(key, res, 300)
        return res


class BaseSummitEnrollment(BaseMediaInfo):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    summit_code = models.CharField(max_length=128, db_index=True)
    summit_name = models.CharField(max_length=128, blank=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.get_label_name()}({self.summit_code})'

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['user', 'summit_code']),
        ]
        unique_together = ['user', 'summit_code']


class CheckLoginMixin:
    login_url = '/'

    def serve(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and self.is_enrollment(user):
            return super().serve(request, *args, **kwargs)
        else:
            return redirect(self.login_url)

    def is_enrollment(self, user):
        ''''
        应该根据会议编码检查报名状态
        '''
        return True


class AdaptivePageMixin:
    def get_template(self, request):
        template = super().get_template(request)
        if request.user_agent.is_mobile:
            idx = template.rfind("/")
            if idx != -1:
                return f"{template[:idx]}/mobile_{template[idx+1:]}"
            else:
                return f"mobile_{template}"
        return template
