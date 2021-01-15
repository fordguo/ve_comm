from collections import namedtuple

from django.utils import timezone
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from . import ChannelType, LiveVendor, get_channel_url, thumbnail_url, video_url


class BannerImage(blocks.StructBlock):
    image = ImageChooserBlock(label="Image")
    mobile_image = ImageChooserBlock(label="Mobile Image")
    name = blocks.CharBlock(label="Name",
                            max_length=64, required=False)
    url = blocks.URLBlock(label="URL", required=False)

    class Meta:
        icon = "image"
        form_template = 'block_forms/banner.html'


class SpeakerInfoStream(blocks.StreamBlock):
    title = blocks.CharBlock(label="Job Title",
                             max_length=128, required=False, icon="title")
    intro = blocks.RichTextBlock(label="Introduction", required=False)

    class Meta:
        icon = 'pilcrow'


class SpeakerBlock(blocks.StructBlock):
    name = blocks.CharBlock(label="Name", max_length=128)
    info = SpeakerInfoStream(
        label="Base Info", block_counts={'title': {'min_num': 0}}, required=False
    )
    image = ImageChooserBlock(label="Photo", required=False)
    mobile_image = ImageChooserBlock(label="Mobile Photo", required=False)

    class Meta:
        icon = 'user'
        label = "Speaker"
        form_template = 'block_forms/speaker.html'


LC = namedtuple("NamedLiveChannel", [
                "cid", "wid", "vendor", "channel_type", "token"])


class LiveInfoStructValue(blocks.StructValue):
    def is_validate(self):
        now = timezone.now()
        end = self.get("end")
        if end:
            return now >= self.get("start") and now <= end
        else:
            return True


class LiveChannelStructValue(LiveInfoStructValue):
    def __init__(self, block, *args):
        super().__init__(block, *args)
        self.channel = LC(self.get("cid"), self.get("wid"),
                          self.get("vendor"), self.get("channel_type"), self.get("token"))

    def channel_url(self):
        return get_channel_url(self.channel)


class LiveBreakBlock(blocks.StructBlock):
    start = blocks.DateTimeBlock()
    end = blocks.DateTimeBlock()
    label = blocks.CharBlock(reqired=False)
    message = blocks.CharBlock(reqired=False)

    class Meta:
        icon = 'horizontalrule'
        value_class = LiveInfoStructValue
        form_template = 'block_forms/live_break.html'


class LiveChannelBlock(blocks.StructBlock):
    start = blocks.DateTimeBlock()
    end = blocks.DateTimeBlock(reqired=False)
    cid = blocks.CharBlock("Channel ID", max_length=255)
    wid = blocks.CharBlock("Watch ID", max_length=255, reqired=False)
    vendor = blocks.ChoiceBlock(choices=LiveVendor.choices)
    channel_type = blocks.ChoiceBlock(choices=ChannelType.choices)
    token = blocks.CharBlock(max_length=255, reqired=False)

    class Meta:
        icon = 'view'
        value_class = LiveChannelStructValue
        form_template = 'block_forms/live_channel.html'


class LiveInfoStream(blocks.StreamBlock):
    channel = LiveChannelBlock()
    lbreak = LiveBreakBlock(label="Live Break")

    class Meta:
        icon = 'wagtail'


def _live_info(ls, stage):
    """
        return tuple(stage,label,message,channelvalue)
    """
    label, message = None, ""
    # ls is StreamValue（没有value属性）是一个Sequence，StreamChild才有value属性，而且value是一个Dict
    if ls:
        channel, lbreak = None, None
        for s in ls:
            if s.block_type == "channel":
                channel = s
            elif s.block_type == "lbreak":
                lbreak = s
        if channel and channel.value.is_validate():
            if stage == "pre":
                label = "精彩抢先看"
            elif stage == "live":
                label = "进入直播"
            elif stage == "post":
                label = "直播回放"
            return (stage, label, message, channel.value)
        elif lbreak and lbreak.value.is_validate():
            message = lbreak.value.get("message")
            label = lbreak.value.get("label")
            if stage == "pre":
                if not label:
                    label = "精彩抢先看"
                if not message:
                    message = "抢先看准备中"
            elif stage == "live":
                if not label:
                    label = "进入直播"
                if not message:
                    message = "直播准备中"
            elif stage == "post":
                if not label:
                    label = "直播回放"
                if not message:
                    message = "回放准备中"
            return (stage, label, message, None)

    return (None, label, message, None)


class LiveStructValue(blocks.StructValue):
    def live_info(self):
        info = _live_info(self.get("pre"), "pre")
        if info[1]:
            return info
        info = _live_info(self.get("live"), "live")
        if info[1]:
            return info
        info = _live_info(self.get("post"), "post")
        if info[1]:
            return info
        return ("no_live", "", "直播间无效", None)


class LiveBlock(blocks.StructBlock):
    pre = LiveInfoStream(label="Pre Live", required=False,
                         max_num=2, block_counts={"lbreak": {"max_num": 1}, "channel": {"max_num": 1}})
    live = LiveInfoStream(label="Live", required=False,
                          max_num=2, block_counts={"lbreak": {"max_num": 1}, "channel": {"max_num": 1}})
    post = LiveInfoStream(label="Post Live", required=False,
                          max_num=2, block_counts={"lbreak": {"max_num": 1}, "channel": {"max_num": 1}})

    class Meta:
        icon = 'tick'
        value_class = LiveStructValue


class NameLiveBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=128, required=False)
    lives = LiveBlock(required=False)

    class Meta:
        icon = 'title'


class OssStructValue(blocks.StructValue):
    def pc_thumbnail(self):
        return thumbnail_url(self.get('category'), self.get('name'), 'pc')

    def mobile_thumbnail(self):
        return thumbnail_url(self.get('category'), self.get('name'), 'mobile')

    def pc_video(self):
        return video_url(self.get('category'), self.get('name'), '1080p')

    def mobile_video(self):
        return video_url(self.get('category'), self.get('name'), '480p')


class OssVideoBlock(blocks.StructBlock):
    category = blocks.CharBlock(max_length=128)
    name = blocks.CharBlock(max_length=128)
    title = blocks.CharBlock(max_length=255, reqired=False)

    class Meta:
        icon = 'folder'
        value_class = OssStructValue
