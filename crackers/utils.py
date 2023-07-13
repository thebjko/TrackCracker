import json

from django.http import HttpResponse as HttpResponseBase
from django.http import HttpResponseRedirect

from django.template import loader
from typing import Any

    
class HTTPResponseHXRedirect(HttpResponseRedirect):
    '''
    HTMX 요청시 페이지를 전환하기 위한 클래스
    https://stackoverflow.com/questions/65569673/htmx-hx-target-swap-html-vs-full-page-reload
    '''
    def __init__(self, *args, **kwargs):
        trigger = kwargs.pop('trigger', None)
        super().__init__(*args, **kwargs)
        self['HX-Redirect'] = self['Location']
        # self.headers['HX-Trigger-After-Settle'] = json.dumps(trigger)

    status_code = 200


class HttpResponse(HttpResponseBase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        trigger = kwargs.pop('trigger', None)
        super().__init__(*args, **kwargs)
        self.headers["HX-Trigger"] = json.dumps(trigger)


def render(request, template_name, context=None, content_type=None, status=None, using=None, **kwargs: Any):
    content = loader.render_to_string(template_name, context, request, using=using)
    trigger = kwargs.pop('trigger', None)
    response = HttpResponse(content, content_type, status, trigger=trigger)
    return response