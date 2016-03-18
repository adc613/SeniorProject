from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from django.http import HttpResponse

# import datetime
import json

from .models import AppSession
from Recipes.models import Recipe
from accounts.models import LinkAccountToEcho
from utils import AlexaResponse, AlexaRequest


class ResponseView(View):
    template_name = 'load_app.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        print('hello')
        return super(ResponseView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {})

    def register_echo(self, request):
        passcode = request.get_intent_params()['Number']
        with open('log', 'ab') as file:
            file.write(str('found echo------'))
            file.write('\n')
        link = LinkAccountToEcho.objects.get(passcode=passcode)
        with open('log', 'ab') as file:
            file.write(str('got link------'))
            file.write('\n')
        if link and link.active:
            link.user.echo = request.get_user_id()
            link.user.save()
            link.active = False
            link.save()
            return 'You have successfully registered your echo'

        return 'There has been an error please retry'

    def post(self, request):
        with open('log', 'ab') as file:
            file.write(str(request.body))
            file.write('\n')

        echo_request = AlexaRequest(json.loads(request.body))

        with open('log', 'ab') as file:
            file.write(str('loaded------'))
            file.write('\n')

        session = echo_request.get_session()

        with open('log', 'ab') as file:
            file.write(str('found session------'))
            file.write('\n')

        if session is not None:
            # Echo is in a session
            return_text = session.next_action()
        elif echo_request.get_intent_type() == 'register':
            with open('log', 'ab') as file:
                file.write(str('register ing echo------'))
                file.write('\n')
            return_text = self.register_echo(echo_request)
            with open('log', 'ab') as file:
                file.write(str('registered echo echo------'))
                file.write('\n')

        elif echo_request.get_user():
            # There not in an app, but echo has been registered
            return_text = 'Please go online and chose your application'

        else:
            # Echo has not been registered
            return_text = "This echo has not been registered, " +\
                "please login and begin registration process"

        response = AlexaResponse(return_statement=return_text).get_response()
        with open('log', 'ab') as file:
            file.write(str('loaded------'))
            file.write('\n')

        return HttpResponse(json.dumps(response),
                            content_type="application/json")


class LoadApplicationView(View):
    template_name = 'load_app.html'
    post_template_name = 'app_is_loaded.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        context['apps'] = Recipe.objects.all()
        return render(request, self.template_name, context)

class ApplicationIsLoadedView(View):
    template_name = 'app_is_loaded.html'

    @method_decorator(login_required)
    def get(self, request, pk, **kwargs):
        print('hey')

        app = Recipe.objects.get(pk=pk)
        session = AppSession.objects.get_or_create(user=request.user,
                                                   current_app=app)[0]
        session.end = False
        session.save()

        return render(request, self.template_name, {})
