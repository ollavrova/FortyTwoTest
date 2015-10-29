import json
import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
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
