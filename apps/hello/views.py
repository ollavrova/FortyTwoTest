import json
import logging
from django.http import HttpResponse
from django.template.response import TemplateResponse
from apps.hello.models import Person, Requests
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'hello/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['person'] = Person.objects.first()
        context['user'] = self.request.user
        return context


home = HomeView.as_view()


def req(request):
    logger.info(request.GET)
    if request.is_ajax():
        try:
            start = int(request.GET.get('request_old_count'))
            end = int(request.new_count)
            delta = end - start
            delta_list = range(start, end)
        except Exception as e:
            delta = e.message
            logger.error(e.message)
        logger.info('check requests:'+str({'result': delta}))
        return HttpResponse(json.dumps({'result': delta,
                                        'delta_list': delta_list,
                                        'result_upload': delta_list}),
                            content_type="application/json")
    else:
        count = Requests.objects.all().count()
        query = Requests.objects.order_by('timestamp')[:10]
        response = TemplateResponse(request, 'hello/requests.html',
                                    {'object_list': query,
                                     'old_count': count})
    return response
