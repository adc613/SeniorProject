from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import HttpResponse

import datetime
import json
import shelve


class DevPageView(View):
    template_name = 'index.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DevPageView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        db = shelve.open('dev.db')
        context = {'oldResponse': db['response']}
        file = open('log', 'r')
        context['recent_request'] = file.read()
        return render(request, self.template_name, context)

    def post(self, request):
        db = shelve.open('dev.db')
        db['response'] = request.POST['newResponse']

        return HttpResponseRedirect(reverse('dev:home'))


class ResponseView(View):
    template_name = 'response.html'

    def get(self, request):
        now = datetime.datetime.now()
        with open('log', 'ab') as file:
            file.write('---' + str(now) + '----\n')
            file.write(str(request.POST))
            file.write('\n')
        db = shelve.open('dev.db')
        response = db['response']
        response = json.dumps(response)

        return HttpResponse(response, content_type="application/json")

    def post(self, request):
        now = datetime.datetime.now()
        with open('log', 'ab') as file:
            file.write('---' + str(now) + '----\n')
            file.write(str(request.POST))
            file.write('\n')
        db = shelve.open('dev.db')
        response = db['response']
        response = json.dumps(response)

        return HttpResponse(response, mimetype="application/json")
