from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from . import get_channel_url, get_user_channel_url, LiveVendor, ChannelType


class BaseMiniLiveChannel(index.Indexed, models.Model):
    vendor = models.CharField(
        _("Live Vendor"), max_length=128, choices=LiveVendor.choices)
    channel_type = models.CharField(
        _("Channel Type"), max_length=16, choices=ChannelType.choices)
    cid = models.CharField(_("Channel ID"), max_length=255, db_index=True)
    wid = models.CharField(
        _("Watch ID"), max_length=512, db_index=True, blank=True)
    token = models.CharField(_("Token"), max_length=128, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('vendor', classname="col6"),
                FieldPanel('channel_type', classname="col6"),
                FieldPanel('cid', classname="col6"),
                FieldPanel('token', classname="col6"),
                FieldPanel('wid', classname="col12"),
            ],
            heading=_("Base Info"),
            classname="collapsible"
        )
    ]
    search_fields = [
        index.SearchField("cid", partial_match=True),
        index.SearchField("wid", partial_match=True),
    ]

    def __str__(self):
        return f'{self.cid}({self.get_vendor_display()}-{self.get_channel_type_display()})'

    @property
    def is_live(self):
        return self.channel_type == ChannelType.LIVE

    @property
    def channel_url(self):
        return get_channel_url(self)

    def get_user_channel_url(self, user):
        return get_user_channel_url(self, user)

    @classmethod
    def get_by_cid_or_wid(cls, cid, wid):
        try:
            if cid:
                return cls.objects.get(cid=cid)
            if wid:
                return cls.objects.get(wid=wid)
        except cls.DoesNotExist:
            return None

    class Meta:
        abstract = True
        verbose_name = _("Mini Live Channel")
        verbose_name_plural = _("Mini Live Channels")


@register_snippet
class MiniLiveChannel(BaseMiniLiveChannel):
    class Meta:
        verbose_name = _("Mini Live Channel")
        verbose_name_plural = _("Mini Live Channels")
