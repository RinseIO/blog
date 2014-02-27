import threading
from application.models import UserModel


g = threading.local()

class AuthenticationMiddleware(object):
    def process_request(self, request):
        request.user = UserModel()

class GlobalMiddleware(object):
    def process_request(self, request):
        g.request = request
