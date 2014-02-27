from django.conf.urls import patterns, include, url
from application.views import *
from application.exceptions import *


# methods
def dispatch(**dispatches):
    def wraps(request, *args, **kwargs):
        handler = dispatches.get(request.method, method_not_allowed)
        try:
            return handler(request, *args, **kwargs)
        except ApplicationException as e:
            return e.view(request, *args, **kwargs)
    return wraps
def api_dispatch(**dispatches):
    def wraps(request, *args, **kwargs):
        if 'application/json' not in request.META['HTTP_ACCEPT'].split(','):
            # return base view for first loading
            return base_view(request)
        handler = dispatches.get(request.method, method_not_allowed)
        try:
            return handler(request, *args, **kwargs)
        except ApplicationException as e:
            return e.view(request, *args, **kwargs)
    return wraps

urlpatterns = patterns('',
    url(r'^$', dispatch(GET=base_view)),
    # url(r'^posts$', api_dispatch(GET=get_posts, POST=add_post)),
    # url(r'^posts/(?P<post_id>\d+)$', api_dispatch(DELETE=delete_post)),
)
