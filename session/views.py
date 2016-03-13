from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# import datetime
# import json

from .models import AppSession
from accounts.models import LinkAccountToEcho, User
from utils import AlexaResponse


class ResponseView(View):
    template_name = 'response.html'

    def does_echo_have_current_session(self, echo_id):
        return AppSession.objects.get(amazon_echo=echo_id)

    def has_echo_been_registered(self, echo_id):
        return User.objects.get(echo=echo_id)

    def register_echo(self, passcode, echo_id):
        link = LinkAccountToEcho.objects.get(passcode=passcode)
        if link and link.active:
            link.user.echo = echo_id
            link.user.save()
            link.active = False
            link.save()
            return 'You have successfully registered your echo'

        return 'There has been an error please retry'

    @method_decorator(csrf_exempt)
    def post(self, request):
        session = request.POST.get('session', None)
        if session is None:
            return HttpResponseRedirect(reverse('home'))

        echo_id = session['user']['userId']
        session = self.does_echo_have_current_session(echo_id)

        if session:
            # Echo is in a session
            return_text = session.get_next_action()
        else:
            user = self.has_echo_been_registered(echo_id)
            if user:
                # There not in an app, but echo has been registered
                return_text = 'Which application would you like?'
                return
            else:
                # Check registration process
                echo_request = request.POST.get('request', None)
                if not echo_request:
                    return_text = 'There seems to have been an error. ' +\
                        'Please try again'
                else:
                    intent = echo_request.get('intent', None)
                    if not intent:
                        return_text = 'There seems to have been an error. ' +\
                                      'Please try again'
                    elif intent['name'] == 'register':
                        passcode = intent['slots']['Number']['value']
                        return_text = self.register_echo(passcode, echo_id)
                    else:
                        # Echo has not been registered
                        return_text = "This echo has not been registered, " +\
                            "please login and begin registration process"

        response = AlexaResponse(return_statement=return_text).get_response()

        return HttpResponse(response, mimetype="application/json")
