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
push(os.path.join(os.path.dirname(__file__), '_design', 'posts'), db)
class PostModel(Document):
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