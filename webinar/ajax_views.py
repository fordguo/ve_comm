import functools

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .vendor import vhall
from . import get_channel_url, get_user_channel_url


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
        result.update(stage=stage, label=label, message=message)
        if label:
            result["status"] = "valid"
        if channel:
            if request.user.is_authenticated:
                result["channel_url"] = get_user_channel_url(
                    channel.channel, request.user)
            else:
                result["channel_url"] = get_channel_url(channel.channel)

    return result


@ajax_required(auth=False)
def ajax_get_live_info(request, content_type, pk, stream_attr, parent_block_type, parent_id):
    result = get_live_info(request, content_type, pk,
                           stream_attr, parent_block_type, parent_id)
    return JsonResponse(result)


@ajax_required(auth=False, method='POST')
def vhall_api_md5_sign(request):
    return JsonResponse(vhall.api_md5_sign(request.POST.copy()))


@ajax_required(auth=False, method='POST')
def vhall_js_md5_sign(request):
    # fs = ['roomid', 'account', 'username']
    # if k in fs
    params = {k: v for k, v in request.POST.items()}
    return JsonResponse(vhall.js_md5_sign(params))
