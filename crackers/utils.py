from django.http import HttpResponseRedirect

    
class HTTPResponseHXRedirect(HttpResponseRedirect):
    '''
    HTMX 요청시 페이지를 전환하기 위한 클래스
    https://stackoverflow.com/questions/65569673/htmx-hx-target-swap-html-vs-full-page-reload
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['HX-Redirect'] = self['Location']
    status_code = 200