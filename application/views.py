from django import http
from django.template import loader, RequestContext, Context
from django.template.response import TemplateResponse
from application.models import *


# -----------------------------------------------
# base view
# -----------------------------------------------
def base_view(request):
    return TemplateResponse(request, 'base.html')


# -----------------------------------------------
# post views
# -----------------------------------------------
def get_posts(request):
    import logging
    posts = PostModel.view('posts/all')
    logging.error(posts.__dict__)
    for post in posts.all():
        logging.error('title: %s' % post.title)
    return JsonResponse({})

def add_post(request):
    model = json.loads(request.body)
    post = PostModel()
    post.title = model.get('title')
    post.content = model.get('content')
    post.save()
    return JsonResponse(post.dict())


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