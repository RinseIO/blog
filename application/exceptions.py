from django import http
from django.template import loader, RequestContext, Context
from application.models import ErrorViewModel


class ApplicationException(Exception):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = server_error

class Http400(ApplicationException):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = bad_request

class Http403(ApplicationException):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = permission_denied

class Http404(ApplicationException):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = page_not_found

class Http405(ApplicationException):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = method_not_allowed

class Http500(ApplicationException):
    def __init__(self, *args, **kwargs):
        super(ApplicationException, self).__init__(*args, **kwargs)
        self.view = server_error


# -----------------------------------------------
# error views
# -----------------------------------------------
def bad_request(request):
    template = loader.get_template('error/default.html')
    model = ErrorViewModel(
        status=400,
        exception='Bad Request'
    )
    return http.HttpResponseBadRequest(template.render(RequestContext(request, model)))

def permission_denied(request):
    template = loader.get_template('error/default.html')
    model = ErrorViewModel(
        status=403,
        exception='Permission Denied'
    )
    return http.HttpResponseForbidden(template.render(RequestContext(request, model)))

def page_not_found(request):
    template = loader.get_template('error/default.html')
    model = ErrorViewModel(
        status=404,
        exception='%s Not Found' % request.path
    )
    return http.HttpResponseNotFound(template.render(RequestContext(request, model)))

def method_not_allowed(request):
    template = loader.get_template('error/default.html')
    model = ErrorViewModel(
        status=405,
        exception='%s Not Allowed' % request.method
    )
    return http.HttpResponse(status=405, content=template.render(RequestContext(request, model)))

def server_error(request):
    template = loader.get_template('error/default.html')
    model = ErrorViewModel(
        status=500,
        exception='Server Error'
    )
    return http.HttpResponseServerError(template.render(Context(model)))
