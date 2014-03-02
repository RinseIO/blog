from django.template.response import TemplateResponse
from application.models import *
from application.exceptions import Http404


# -----------------------------------------------
# base view
# -----------------------------------------------
def base_view(request):
    return TemplateResponse(request, 'base.html')


# -----------------------------------------------
# post views
# -----------------------------------------------
def get_posts(request):
    """
    Get posts.
    :param request.GET:
        index: The page index.
    """
    model = request.GET.dict()
    try:
        index = int(model.get('index', '0'))
    except:
        raise Http400
    size = 10

    total = PostModel.view('posts/all').count()
    posts = PostModel.view(
        'posts/all_sorted_create_time',
        descending=True,
        limit=size,
        skip=index * size
    ).all()
    return JsonResponse(PageList(index, size, total, posts))

def add_post(request):
    """
    Add a post.
    :param request.body:
        It should be json.
        title: The post title.
        content The post content.
    :return: JsonResponse(PostModel)
    """
    model = json.loads(request.body)
    post = PostModel()
    post.title = model.get('title')
    post.content = model.get('content')
    post.save()
    return JsonResponse(post.dict())

def delete_post(request, post_id):
    """
    Delete the post.
    :param post_id: The post id.
    """
    view = PostModel.view(
        'posts/all',
        key=post_id
    )
    post = view.first()
    if post is None:
        raise Http404
    post.delete()

    return HttpResponse(status=200)

def update_post(request, post_id):
    """
    Update the post.
    :param post_id: The post id.
    :param request.body:
        It should be json.
        title: The post title.
        content The post content.
    :return: JsonResponse(PostModel)
    """
    model = json.loads(request.body)
    view = PostModel.view(
        'posts/all',
        key=post_id
    )
    post = view.first()
    if post is None:
        raise Http404
    post.title = model.get('title')
    post.content = model.get('content')
    post.save()
    return JsonResponse(post.dict())
