import json
import logging
import datetime
from django.http import HttpResponse
from django.template.response import TemplateResponse
from apps.hello.models import Person, Requests
from django.views.generic import TemplateView
from django.utils.dateformat import DateFormat


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['person'] = Person.objects.first()
        context['user'] = self.request.user
        return context


def req(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            get_time = json.loads(request.body)['old_time']
            start = datetime.datetime.strptime(get_time,
                                               '%Y-%m-%d %H:%M:%S.%f')
            delta = Requests.objects.filter(
                timestamp__gt=start,
                timestamp__lt=datetime.datetime.now()).exclude(
                request_method='POST',
                request_path='/requests/').count()
            logger.info('check requests:'+str({'new': delta}))
        except Exception as e:
            delta = e.message
            logger.error(delta)
        timedata = DateFormat(datetime.datetime.now()).format('Y-m-d H:i:s.u')
        return HttpResponse(json.dumps({'result': delta,
                                        'old_time': timedata}),
                            content_type="application/json")
    else:
        query = Requests.objects.order_by('timestamp')[:10]
        timedata = DateFormat(Requests.objects.latest('timestamp').
                              timestamp).format('Y-m-d H:i:s.u')
        response = TemplateResponse(request, 'hello/requests.html',
                                    {'object_list': query,
                                     'old_time': timedata,
                                     'result': 0})
    return response
