from apps.hello.models import Requests
import datetime


class CustomMiddleware(object):
    def process_request(self, request):
        if request.method == 'GET':
            row = Requests(row=str(request), timestamp=datetime.datetime.now(),
                           request_path=request.path,
                           request_method=request.method)
            row.save()
        return
