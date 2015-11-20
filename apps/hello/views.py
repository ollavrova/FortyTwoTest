import datetime
import json
import logging
from apps.hello.forms import PersonEditForm
from apps.hello.models import Person, Requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.dateformat import DateFormat
from django_remote_forms.forms import RemoteForm
from signals import *  # noqa


logger = logging.getLogger(__name__)


def home(request):
    person = Person.objects.first()
    return render_to_response('hello/index.html',
                              {'person': person},
                              RequestContext(request))


def req(request):
    if request.method == 'POST' and request.is_ajax():
        get_time = json.loads(request.body)['old_time']
        start = datetime.datetime.strptime(get_time,
                                           '%Y-%m-%d %H:%M:%S.%f')
        delta = Requests.objects.filter(
            timestamp__gt=start,
            timestamp__lt=datetime.datetime.now()).exclude(
            request_method='POST',
            request_path='/requests/').count()
        if delta:
            logger.info('check requests:' + str({'new': delta}))
        timedata = DateFormat(datetime.datetime.now()).format('Y-m-d H:i:s.u')
        return HttpResponse(json.dumps({'result': delta,
                                        'old_time': timedata}),
                            content_type="application/json")
    else:
        query = Requests.objects.order_by('-priority', 'timestamp')[:10]
        timedata = DateFormat(Requests.objects.latest('timestamp').
                              timestamp).format('Y-m-d H:i:s.u')
        response = TemplateResponse(request, 'hello/requests.html',
                                    {'object_list': query,
                                     'old_time': timedata,
                                     'result': 0})
    return response


@login_required
def edit(request, pk):
    person = Person.objects.get(id=pk)
    form = PersonEditForm(instance=person)
    photo = person.photo.url if person.photo else None
    if request.method == 'POST' and request.is_ajax():
        form = PersonEditForm(request.POST, request.FILES, instance=person)
        response_data = dict()
        if form.is_valid():
            form.save()
        else:
            response_data['errs'] = process_form_err(form)
            logger.info('Errors of form saving!' + str(response_data['errs']))
        form.photo = person.photo.url if person.photo else None
        response_data['form'] = (RemoteForm(form)).as_dict()
        response_data['form']['fields']['photo']['initial'] = None
        response_data['photo'] = photo
        return HttpResponse(json.dumps(response_data),
                            content_type='application/javascript')
    return render(request, 'hello/edit.html',
                           {'form': form, 'person': person,
                            'photo': photo})


def process_form_err(form):
    errors = dict()
    for e in form.errors.iteritems():
        errors.update({e[0]: unicode(e[1])})
    return errors
