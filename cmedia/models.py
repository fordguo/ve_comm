from django.conf import settings
from django.http import QueryDict
from django.db import models

# Create your models here.


class MediaDeviceType(models.IntegerChoices):
    MOBILE = 1
    PC = 2
    TABLET = 3
    OTHER = 9

    @classmethod
    def get_by_request(cls, request):
        if request is None:
            return cls.OTHER
        if request.user_agent.is_mobile:
            return cls.MOBILE
        elif request.user_agent.is_tablet:
            return cls.TABLET
        else:
            return cls.PC


def is_poster(pk_source):
    return pk_source == 'poster' or pk_source == 'sales_tool'


def get_media_info(request):
    info = dict(device_type=MediaDeviceType.get_by_request(request))
    pk_source = request.session.get('pk_source', '')
    info.update(pk_source=pk_source, pk_campaign=request.session.get('pk_campaign', ''),
                pk_kwd=request.session.get('pk_kwd', ''),
                pk_medium=request.session.get('pk_medium', ''),
                pk_content=request.session.get('pk_content', ''))
    return info


class SalePosterUserQuerySet(models.QuerySet):
    def create_poster_user(self, request):
        pk_source = request.session.get('pk_source', '')
        pk_content = request.session.get('pk_content', '')
        if is_poster(pk_source) and pk_content:
            # cid=1222
            qd = QueryDict(pk_content)
            if 'cid' in qd:
                self.model.objects.create(
                    user=request.user, poster_id=qd['cid'])


class SalePosterUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='+')
    poster_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SalePosterUserQuerySet.as_manager()


class BaseMediaInfo(models.Model):
    pk_campaign = models.CharField(max_length=255, blank=True)
    pk_kwd = models.CharField(max_length=128, blank=True)
    pk_source = models.CharField(max_length=255, blank=True)
    pk_medium = models.CharField(max_length=255, blank=True)
    pk_content = models.CharField(max_length=255, blank=True)
    device_type = models.PositiveSmallIntegerField(
        choices=MediaDeviceType.choices)

    def is_poster(self):
        return is_poster(self.pk_source)

    class Meta:
        abstract = True
