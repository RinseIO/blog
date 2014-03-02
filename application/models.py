import json, os
from datetime import datetime
from django.http import HttpResponse
from couchdbkit import *
from couchdbkit.designer import push
from application.utils import get_db_url


class UserPermission(object):
    anonymous = 0
    root = 1
    normal = 2

class UserModel(object):
    def __init__(self):
        self.is_login = True
        self.id = 100
        self.permission = UserPermission.root
        self.name = 'Kelp'
        self.email = 'kelp@rinse.io'


# -----------------------------------------------
# couch db documents
# -----------------------------------------------
server = Server(uri=get_db_url())
db = server.get_or_create_db('blog')
# push views of posts to database.
push(os.path.join(os.path.dirname(__file__), '_design', 'posts'), db)
class PostModel(Document):
    """
    The post data model.
    """
    title = StringProperty()
    content = StringProperty()
    create_time = DateTimeProperty(default=datetime.utcnow)

    def dict(self):
        return {
            'id': self._id,
            'title': self.title,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
PostModel.set_db(db)


# -----------------------------------------------
# response
# -----------------------------------------------
class JsonResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        if 'dict' in dir(content) and callable(content.dict):
            dict_content = content.dict()
        else:
            dict_content = content
        super(JsonResponse, self).__init__(json.dumps(dict_content), content_type='application/json', *args, **kwargs)


# -----------------------------------------------
# pager
# -----------------------------------------------
class PageList(list):
    def __init__(self, index=0, size=20, total=0, *args, **kwargs):
        self.__index = index
        self.__size = size
        self.__total = total
        super(PageList, self).__init__(*args, **kwargs)

    @property
    def index(self):
        return self.__index

    @property
    def size(self):
        return self.__size

    @property
    def total(self):
        return self.__total

    @property
    def has_next_page(self):
        return self.__total > (self.__index + 1) * self.__size

    @property
    def has_previous_page(self):
        return self.__index > 0

    @property
    def max_index(self):
        max = self.__total / float(self.__size)
        return int(max) if max > int(max) else int(max) - 1

    def dict(self):
        return {
            'index': self.__index,
            'size': self.__size,
            'total': self.__total,
            'has_next_page': self.has_next_page,
            'has_previous_page': self.has_previous_page,
            'max_index': self.max_index,
            'items': [x.dict() for x in self]
        }


# -----------------------------------------------
# error
# -----------------------------------------------
class ErrorViewModel(dict):
    def __init__(self, *args, **kw):
        super(ErrorViewModel, self).__init__(*args, **kw)
        if 'status' not in self:
            self['status'] = 0
        if 'exception' not in self:
            self['exception'] = ''

    @property
    def exception(self):
        return self['exception']
    @exception.setter
    def exception(self, value):
        self['exception'] = value

    @property
    def status(self):
        return self['status']
    @status.setter
    def status(self, value):
        self['status'] = value
