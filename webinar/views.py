
from .vendor.mudu import parse_mudu_url
from .snippet import MiniLiveChannel

MUDU_PREFIX = "mudu"


class MuduMixin:

    def is_mudu_request(self, request):
        return 'visitorId' in request.GET

    def is_mudu(self, request):
        return self.is_mudu_request(request) or f"{MUDU_PREFIX}_vid" in request.session

    def get_mudu_url(self, request):
        live = MiniLiveChannel.get_by_cid_or_wid(
            request.session[f"{MUDU_PREFIX}_channel_id"], request.session[f"{MUDU_PREFIX}_watch_id"])
        return live.get_user_channel_url(request.user)

    def get_mudu_ids(self, request):
        return request.session[f"{MUDU_PREFIX}_channel_id"], request.session[f"{MUDU_PREFIX}_watch_id"]

    def checkin_mudu(self, request):
        url = self.request.GET.get('notify_url')
        vid = self.request.GET.get('visitorId')
        if not url and f"{MUDU_PREFIX}_vid" in request.session:
            url = request.session[f"{MUDU_PREFIX}_notify_url"]
            vid = request.session[f"{MUDU_PREFIX}_vid"]
        params = parse_mudu_url(url)
        watch_id = params.get('watch_id')
        channel_id = params.get('channel_id')
        assert watch_id or channel_id, 'channel id illegal'
        assert vid, 'visitorId is empty!!!'
        request.session[f"{MUDU_PREFIX}_watch_id"] = watch_id
        request.session[f"{MUDU_PREFIX}_channel_id"] = channel_id
        request.session[f"{MUDU_PREFIX}_vid"] = vid
        request.session[f"{MUDU_PREFIX}_notify_url"] = url

    def clear_mudu_session(self, request):
        # clean mudu session
        request.session.pop(f"{MUDU_PREFIX}_watch_id", None)
        request.session.pop(f"{MUDU_PREFIX}_channel_id", None)
        request.session.pop(f"{MUDU_PREFIX}_vid", None)
        request.session.pop(f"{MUDU_PREFIX}_notify_url", None)
