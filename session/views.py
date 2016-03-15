from django.http import HttpResponse
# from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# import datetime
import json

from .models import AppSession
from accounts.models import LinkAccountToEcho, User
from utils import AlexaResponse, AlexaRequest


class ResponseView(View):
    template_name = 'response.html'

    def register_echo(self, request):
        passcode = request.get_intent_params()['passcode']
        link = LinkAccountToEcho.objects.get(passcode=passcode)
        if link and link.active:
            link.user.echo = request.get_user_id()
            link.user.save()
            link.active = False
            link.save()
            return 'You have successfully registered your echo'

        return 'There has been an error please retry'

    @method_decorator(csrf_exempt)
    def post(self, request):
        echo_request = AlexaRequest(json.loads(request.body))

        session = echo_request.get_session()

        if session is not None:
            # Echo is in a session
            return_text = session.next_action()
        elif echo_request.get_intent_type() == 'register':
            return_text = self.register_echo(echo_request)

        elif echo_request.get_user():
            # There not in an app, but echo has been registered
            return_text = 'Please go online and chose your application'

        else:
            # Echo has not been registered
            return_text = "This echo has not been registered, " +\
                "please login and begin registration process"

        response = AlexaResponse(return_statement=return_text).get_response()

        return HttpResponse(json.dumps(response),
                            content_type="application/json")
