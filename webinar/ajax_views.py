import functools

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from . import get_user_channel_url
from .snippet import FloatImage


def ajax_required(original_function=None, *, method='GET', auth=True):
    def _wrap(function):
        @functools.wraps(function)
        def _wrapped_f(request, *args, **kwargs):
            if not request.is_ajax() or request.method != method:
                return HttpResponseBadRequest()
            if auth and not request.user.is_authenticated:
                return HttpResponseForbidden()
            return function(request, *args, **kwargs)
        return _wrapped_f
    if original_function:
        return _wrap(original_function)
    return _wrap


def _check_live_block(stream_value, parent_block_type, parent_id):
    q = []
    flag = True
    for s in stream_value:
        if s.block_type == parent_block_type and s.id == parent_id:
            flag = False
            return s
        else:
            q.append(s)
    if flag and q:
        for s in q:
            return _check_live_block(s, parent_block_type, parent_id)


@ajax_required(auth=False)
def get_live_info(request, content_type, pk, stream_attr, parent_block_type, parent_id):
    st = content_type.split(".")
    model_type = None
    if len(st) > 1:
        model_type = ContentType.objects.get(app_label=st[0],
                                             model=st[1]).model_class()
    else:
        model_type = ContentType.objects.get(model=content_type).model_class()

    result = {"status": "invalid"}
    obj = get_object_or_404(model_type, pk=pk)
    info = _check_live_block(getattr(obj, stream_attr),
                             parent_block_type, parent_id)
    if info:
        stage, label, message, channel = info.value["lives"].live_info()
        result.update(stage=stage, label=label,
                      message=message, channel=channel)
        if label:
            result["status"] = "valid"
        if channel:
            result["channel_url"] = get_user_channel_url(
                channel.channel, request.user)
    return JsonResponse(result)


@ajax_required(auth=False)
def get_float_image(request, code):
    img = get_object_or_404(FloatImage, code=code)
    lives = []
    for i in img.lives:
        ninfo = {"name": i.value["name"]}
        stage, label, message, channel = i.value["lives"].live_info()
        live_info = dict(stage=stage, label=label, status="invalid",
                         message=message, channel=channel)
        if label:
            live_info["status"] = "valid"
        if channel:
            live_info["channel_url"] = get_user_channel_url(
                channel.channel, request.user)

        ninfo["live"] = live_info
        lives.append(ninfo)
    return JsonResponse({
        'image': img.image.file.url, 'image_mobile': img.image_mobile.file.url,
        "id": img.id, "lives": lives, "url": img.url
    })
