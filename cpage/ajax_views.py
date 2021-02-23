

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from webinar import get_channel_url, get_user_channel_url
from webinar.ajax_views import ajax_required
from .snippet import FloatImage


@ajax_required(auth=False)
def get_float_image(request, code):
    img = get_object_or_404(FloatImage, code=code)
    lives = []
    for i in img.lives:
        ninfo = {"name": i.value["name"]}
        stage, label, message, channel = i.value["lives"].live_info()
        live_info = dict(stage=stage, label=label, status="invalid",
                         message=message)
        if label:
            live_info["status"] = "valid"
        if channel:
            if request.user.is_authenticated:
                live_info["channel_url"] = get_user_channel_url(
                    channel.channel, request.user)
            else:
                live_info["channel_url"] = get_channel_url(channel.channel)

        ninfo["live"] = live_info
        lives.append(ninfo)
    return JsonResponse({
        'image': img.image.file.url, 'image_mobile': img.image_mobile.file.url,
        "id": img.id, "lives": lives, "url": img.url, 'time_status': img.time_status,
        'start_delta': img.start_delta
    })
