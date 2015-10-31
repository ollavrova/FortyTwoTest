import json
import logging
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.dateformat import DateFormat
from apps.hello.forms import PersonEditForm
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
            if delta:
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


@login_required
def edit(request):
    person = Person.objects.first()
    if request.method == 'POST' and request.is_ajax():
        logger.info('User %s tried to edit data.' % request.user)
        form = PersonEditForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            try:
                form.save()
                logger.info('The form is saved.')
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                logger.exception(e)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        return render_to_response('hello/reload.html',
                                  {'form': form, 'person': person},
                                  RequestContext(request))
    else:
        form = PersonEditForm(instance=person)
    return render_to_response('hello/edit.html',
                              {'form': form, 'person': person},
                              RequestContext(request))
