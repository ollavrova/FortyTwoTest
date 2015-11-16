import datetime
import json
import logging
from apps.hello.forms import PersonEditForm
from apps.hello.models import Person, Requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response
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


# @login_required
# def edit(request):
#     person = Person.objects.get(pk=1)
#     if request.method == 'POST' and request.is_ajax():
#         logger.info('User %s tried to edit data.' % request.user)
#         form = PersonEditForm(request.POST, request.FILES, instance=person)
#         if form.is_valid():
#             form.save()
#             logger.info('The form is saved.')
#         else:
#             messages.add_message(request, messages.ERROR, form.errors)
#         return render_to_response('hello/reload.html',
#                                   {'form': form, 'person': person},
#                                   RequestContext(request))
#     else:
#         form = PersonEditForm(instance=person)
#     return render_to_response('hello/edit.html',
#                               {'form': form, 'person': person},
#                               RequestContext(request))


class AjaxableResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            context = self.ajax_invalid_context_data(**form.errors)
            return self.render_to_json_response(context, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            context = self.ajax_valid_context_data(pk=self.object.pk)
            return self.render_to_json_response(context)
        else:
            return response

    def ajax_valid_context_data(self, **kwargs):
        return kwargs

    def ajax_invalid_context_data(self, **kwargs):
        return kwargs


class Edit(AjaxableResponseMixin, UpdateView):
    template_name = "hello/edit.html"
    model = Person
    form_class = PersonEditForm
    success_url = reverse_lazy('edit')
    thumbnail_options = dict(size=(300, 400), crop=True)

    def get_object(self, queryset=None):
        return Person.objects.get(pk=1)

    def ajax_valid_context_data(self, **kwargs):
        context = super(Edit, self).ajax_valid_context_data(**kwargs)
        thumbnail = self.object.photo.get_thumbnail(self.thumbnail_options)
        context['photo'] = thumbnail.url if thumbnail else None
        form = PersonEditForm(self.request.POST, self.request.FILES)
        context['form'] = RemoteForm(form).as_dict()
        return context

edit = login_required(Edit.as_view())
