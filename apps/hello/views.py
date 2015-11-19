import datetime
import json
import logging
from apps.hello.forms import PersonEditForm
from apps.hello.models import Person, Requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.dateformat import DateFormat
from django.views.generic import UpdateView
from django_remote_forms.forms import RemoteForm
from signals import *


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
    if request.method == 'POST' and request.is_ajax():
        logger.info('User %s tried to edit data.' % request.user)
        form = PersonEditForm(request.POST, request.FILES, instance=person)
        response_data = dict()
        response_data['data'] = form.data
        if form.is_valid():
            form.save()
            response_data['err'] = 'false'
            logger.info('The form is saved. No errors.')
        else:
            response_data['err'] = 'true'
            errors = {}
            for e in form.errors.iteritems():
                errors.update({e[0]: unicode(e[1])})
            response_data['errs'] = errors
            messages.add_message(request, messages.ERROR, form.errors)
            logger.info('Errors of form saving!' + str(errors))
        form.photo = None
        response_data['form'] = (RemoteForm(form)).as_dict()
        response_data['form']['fields']['photo']['initial'] = None
        response_data['photo'] = person.photo.url if person.photo \
            else None
        # logger.info('response_data =' + json.dumps(response_data['form'],
        #                                            indent=4))
        return HttpResponse(json.dumps(response_data),
                            content_type='application/javascript')
    else:
        form = PersonEditForm(instance=person)
        photo = person.photo.url if person.photo else None
    return render(request, 'hello/edit.html',
                           {'form': form, 'person': person,
                            'photo': photo})
