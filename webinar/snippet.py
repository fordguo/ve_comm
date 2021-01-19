from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField

from . import get_channel_url, get_user_channel_url, LiveVendor, ChannelType
from .blocks import NameLiveBlock


@register_snippet
class FloatImage(index.Indexed, models.Model):
    code = models.SlugField(verbose_name=_("Float Code"),  unique=True)
    image = models.ForeignKey(
        "wagtailimages.Image", verbose_name=_("Image"),
        null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    image_mobile = models.ForeignKey(
        "wagtailimages.Image", verbose_name=_("Mobile Image"),
        null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )
    url = models.URLField(_("Float URL"), blank=True)
    lives = StreamField([("meeting_live", NameLiveBlock(label=_("Meeting Live")))],
                        verbose_name=_("Lives"), null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('code'),
                ImageChooserPanel("image", classname="col6"),
                ImageChooserPanel("image_mobile", classname="col6"),
                FieldPanel('url'),

            ],
            heading=_("Base Info"),
            classname="collapsible"
        ),
        StreamFieldPanel('lives')
    ]
    search_fields = [
        index.SearchField("code", partial_match=True),
    ]

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Float Image")
        verbose_name_plural = _("Float Images")


@register_snippet
class MiniLiveChannel(models.Model):
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

    def __str__(self):
        return f'{self.cid}({self.get_vendor_display()}-{self.get_channel_type_display()})'

    @property
    def is_live(self):
        return self.channel_type == ChannelType.LIVE

    @property
    def channel_url(self):
        return get_channel_url(self)

    def user_channel_url(self, user):
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
        verbose_name = _("Mini Live Channel")
        verbose_name_plural = _("Mini Live Channels")
