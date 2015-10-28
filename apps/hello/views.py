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
    logger.info(request.GET)
    if request.method == 'GET' and request.is_ajax():
        try:
            start = datetime.datetime.strptime(request.GET.get('old_time', ''),
                                               '%Y-%m-%d %H:%M:%S')
            delta = Requests.objects.filter(
                timestamp__range=[start,
                                  datetime.datetime.now()]).count()
        except Exception as e:
            delta = e.message
            logger.error(e.message)
        logger.info('check requests:'+str({'new': delta}))
        timedata = DateFormat(datetime.datetime.now()).format('Y-m-d H:i:s')
        return HttpResponse(json.dumps({'result': delta,
                                        'old_time': timedata}),
                            content_type="application/json")
    else:
        query = Requests.objects.order_by('timestamp')[:10]
        timedata = DateFormat(Requests.objects.latest('timestamp').
                              timestamp).format('Y-m-d H:i:s')
        response = TemplateResponse(request, 'hello/requests.html',
                                    {'object_list': query,
                                     'old_time': timedata})
    return response
