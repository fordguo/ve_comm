

import json
from webinar.snippet import MiniLiveChannel
from webinar.ajax_views import get_live_info
from cpage.ajax_views import get_float_image


FLOAT_PREFIX = "float::"
LIVE_PREFIX = "live::"
MUDU_PREFIX = "mudu::"


def parse_quick_params(params):
    if params.startswith(FLOAT_PREFIX):
        return 'float', params[len(FLOAT_PREFIX):].split(':')
    elif params.startswith(LIVE_PREFIX):
        return 'live', params[len(LIVE_PREFIX):].split(':')
    elif params.startswith(MUDU_PREFIX):
        return 'mudu', params[len(MUDU_PREFIX):].split(':')
    return None, None


def quick_float(code):
    return f"{FLOAT_PREFIX}{code}"


def quick_live(content_type, pk, stream_attr, parent_block_type, parent_id):
    return f"{LIVE_PREFIX}{content_type}:{pk}:{stream_attr}:{parent_block_type}:{parent_id}"


def quick_mudu(cid, wid):
    return f"{MUDU_PREFIX}{cid}:{wid}"


def get_quick_url(request, params):
    qtype, qparams = parse_quick_params(params)
    assert qtype
    if qtype == 'float':
        res = get_float_image(request, qparams[0])
        lives = json.loads(res.content)['lives']
        assert lives
        return lives[0]['channel_url']
    elif qtype == 'live':
        res = get_live_info(request, *qparams)
        lives = json.loads(res.content)['lives']
        assert lives
        return lives[0]['channel_url']
    elif qtype == 'mudu':
        live = MiniLiveChannel.get_by_cid_or_wid(qparams[0], qparams[1])
        assert live
        return live.get_user_channel_url(request.user)
