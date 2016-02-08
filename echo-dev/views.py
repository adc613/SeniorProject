from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

import datetime
import json
import shelve


class DevPageView(View):
    template_name = 'index.html'

    def serialize(self, dict):
        length = len(dict) / 2
        keys = [0 for x in range(0, length)]
        values = [0 for x in range(0, length)]

        for key, value in dict.iteritems():
            item = key.split('-')
            print(value)
            if item[0] == 'key':
                keys[int(item[1])] = value
            else:
                values[int(item[1])] = value

        list = zip(keys, values)

        returned_dict = {}
        for key, value in list:
            returned_dict[key] = value

        return returned_dict

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DevPageView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        db = shelve.open('dev.db')
        context = db
        print(request)
        return render(request, self.template_name, context)

    def post(self, request):
        db = shelve.open('dev.db')
        print(request)
        db['response'] = self.serialize(request.POST)
        context = db
        return render(request, self.template_name, context)


class ResponseView(View):
    template_name = 'response.html'

    def get(self, request):
        now = datetime.datetime.now()
        with open('log', 'ab') as file:
            file.write('---' + str(now) + '----\n')
            file.write(str(request))
            file.write('\n')
        db = shelve.open('dev.db')
        response = db['response']
        response = json.dumps(response)
        context = {}
        context['response'] = response

        return render(request, self.template_name, context)
