import json
from django.db import models
from django.http import HttpResponse


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