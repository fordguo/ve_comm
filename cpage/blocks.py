from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from . import thumbnail_url, video_url


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
    description = blocks.RichTextBlock(required=False)

    class Meta:
        icon = 'folder'
        value_class = OssStructValue


class AgendaItem(blocks.StructBlock):
    title = blocks.CharBlock(max_length=512)
    description = blocks.RichTextBlock(required=False)
    start = blocks.DateTimeBlock()
    end = blocks.DateTimeBlock()
    speakers = blocks.StreamBlock(
        [("speaker", SpeakerBlock())], required=False)

    class Meta:
        icon = 'list-ol'
        form_template = 'block_forms/agenda_item.html'


class AgendaBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=64)
    sub_name = blocks.CharBlock(max_length=128, required=False)
    items = blocks.ListBlock(AgendaItem())

    class Meta:
        icon = 'date'
