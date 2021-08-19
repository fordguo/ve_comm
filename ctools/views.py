from django.shortcuts import render

# Create your views here.


class MarketSessionMixin:
    def market_session(self, request):
        pks = {k: v for k, v in request.session.items() if k.startswith("pk_")}
        pks.update(self.extra_session(request))
        return pks

    def extra_session(self, request):
        return {}

    def reinit_market(self, request, infos):
        for k, v in infos.items():
            request.session[k] = v

    def clean_market(self, request):
        keys = [k for k in request.session.keys() if k.startswith("pk_")]
        keys += self.extra_session(request).keys()
        for k in keys:
            request.session.pop(k, None)
