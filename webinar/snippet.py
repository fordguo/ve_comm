from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField

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
