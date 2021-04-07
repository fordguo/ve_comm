from webinar.snippet import MiniLiveChannel
from django.conf import settings
from django.shortcuts import redirect
from django.db import models
from django.core.cache import cache


from wagtail.core.models import Orderable
from wagtail.search import index
from wagtail.core.fields import RichTextField, StreamField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, StreamFieldPanel

from cmedia.models import BaseMediaInfo
from cpage.blocks import SpeakerBlock
from webinar.blocks import LiveBlock

from .snippet import *

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
        return f'{self.user.get_full_name()}({self.summit_code})'

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


class SummitAgenda(ClusterableModel, index.Indexed,  models.Model):
    summit_app = models.CharField("峰会内部名", max_length=128)
    name = models.CharField("内部名", max_length=128)
    title = models.CharField("议程名", max_length=255)
    sub_title = models.CharField("副议程名", max_length=255, blank=True)
    description = RichTextField("描述", blank=True)
    start = models.DateTimeField('开始', null=True, blank=True)
    end = models.DateTimeField('结束', null=True, blank=True)
    webinars = StreamField(
        [
            ('webinar', LiveBlock())
        ], verbose_name="直播", null=True, blank=True)

    panels = [
        FieldRowPanel(
            [
                FieldPanel('summit_app'),
                FieldPanel('name'),
            ]),
        FieldRowPanel(
            [
                FieldPanel('title'),
                FieldPanel('sub_title'),
            ]),
        FieldRowPanel(
            [
                FieldPanel('start'),
                FieldPanel('end'),
            ]),
        FieldPanel('description', classname="full"),
        StreamFieldPanel('webinars'),
        InlinePanel('items', label="议程项"),
    ]
    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('name', partial_match=True),
        index.FilterField('summit_app'),
    ]

    def __str__(self):
        return f"{self.title}({self.name})"

    class Meta:
        verbose_name = "峰会议程"
        verbose_name_plural = "峰会议程"
        unique_together = ['summit_app', 'name']


class AgendaItem(Orderable):
    agenda = ParentalKey(SummitAgenda, on_delete=models.CASCADE,
                         related_name='items')
    topic = models.CharField("主题", max_length=255)
    subtopic = models.CharField("子主题", max_length=255, blank=True)
    description = RichTextField("描述", blank=True)
    start = models.DateTimeField('开始', null=True, blank=True)
    end = models.DateTimeField('结束', null=True, blank=True)
    speakers = StreamField(
        [
            ('speaker', SpeakerBlock())
        ], verbose_name="演讲嘉宾", null=True, blank=True)

    panels = [
        FieldPanel('topic'),
        FieldRowPanel(
            [
                FieldPanel('start'),
                FieldPanel('end'),
            ]),
        FieldPanel('subtopic'),
        FieldPanel('description'),
        StreamFieldPanel('speakers'),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "议程项"
        verbose_name_plural = "议程项"


class SummitWebinar(MiniLiveChannel):
    summit_app = models.CharField("峰会内部名", max_length=128)

    panels = [
        FieldPanel('summit_app'),
        MultiFieldPanel(
            [
                FieldPanel('vendor', classname="col6"),
                FieldPanel('channel_type', classname="col6"),
                FieldPanel('cid', classname="col6"),
                FieldPanel('token', classname="col6"),
                FieldPanel('wid', classname="col12"),
            ],
            heading="基本信息",
            classname="collapsible"
        )
    ]

    class Meta:
        verbose_name = "峰会直播间"
        verbose_name_plural = "峰会直播间"
