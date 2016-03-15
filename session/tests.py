from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from Recipes.models import Recipe, GeneralAction, BasicReturnText
from accounts.models import User, LinkAccountToEcho
from .models import AppSession

import json


class CreateAlexaRequest():

    def __init__(self, **kwargs):
        self._response = {}
        self._response['version'] = kwargs.get('version', '1.0')
        self._response['session'] = {
            'new': False,
            'sessionId': 'amzn1.echo-api.session.000000-0000-0000-0000000000',
            'application': {
                'applicationId': 'amzn1.echo-sdk-ams.app.0000-000-000',
                },
            'attributes': {},
            'user': {
                'userId': 'amzn1.account.AM3B000000000000000000000000000'
                },
            }

        self._response['request'] = {
            'type': kwargs.get('type', 'IntentRequest'),
            'requestId': 'amzn1.echo-api.request.0000-00000-000-00000-00000',
            'timestamp': '2015-05-13T12:34:56Z',
            'intent': {
                'name': kwargs.get('intent_name', 'passcode'),
                'slots': []
                }
            }

    def create_param(self, **kwargs):
        param = {
            kwargs.get('type', 'AMAZON.STRING'): {
                'name': kwargs['name'],
                'value': kwargs['value']
                }
            }
        self._response['request']['intent']['slots'].append(param)

    def get_params(self):
        return self._response


class ResponseTestCases(TestCase):

    def setUp(self):
        self.password = '$tr0ngPa$$w0rd'
        self.user = User.objects.create_user(
            first_name='Adam',
            last_name='Collins',
            email='adc82@case.edu',
            password=self.password
            )

        self.recipe = Recipe.objects.create(
            creator=self.user,
            name='First App',
            description='First Description'
            )

        self.basic_return_text = BasicReturnText.objects.create(
            return_statement='Hello World!'
            )
        self.general_action = GeneralAction.objects.create(
            type='RT',
            basic_return_text=self.basic_return_text
            )

        basic_return_text2 = BasicReturnText.objects.create(
            return_statement='Hello World!2'
            )
        general_action2 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text2
            )

        basic_return_text3 = BasicReturnText.objects.create(
            return_statement='Hello World!3'
            )
        general_action3 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text3
            )

        basic_return_text4 = BasicReturnText.objects.create(
            return_statement='Hello World!4'
            )
        general_action4 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text4
            )

        basic_return_text5 = BasicReturnText.objects.create(
            return_statement='Hello World!5'
            )
        general_action5 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text5
            )
        self.recipe.insert_action(self.general_action, 0)
        self.recipe.insert_action(general_action2, 0)
        self.recipe.insert_action(general_action3, 0)
        self.recipe.insert_action(general_action4, 0)
        self.recipe.insert_action(general_action5, 0)

        self.actions = [self.general_action, general_action2, general_action3,
                        general_action4, general_action5]

    def test_app_session_model_next_action(self):
        session = AppSession.objects.create(
            user=self.user,
            amazon_echo='1lkjh342k41j4kl1j34',
            current_app=self.recipe
            )

        for action in self.actions:
            return_statement = session.next_action()
            self.assertEqual(return_statement, action.get_action()[1])

    def test_registering_echo(self):
        link = LinkAccountToEcho.objects.create(user=self.user)
        request = CreateAlexaRequest(type='IntentRequest',
                                     intent_name='register')
        request.create_param(type='AMAZON.FOUR_DIGIT_NUMBER',
                             name='passcode',
                             value=link.passcode)
        c = Client()
        resp = c.post(reverse('session:echo_request'),
                      data=json.dumps(request.get_params()),
                      content_type='application/json',
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                      )
        self.assertEqual(resp.status_code, 200)

    def test_session_has_not_started(self):
        pass

    def test_echo_is_in_session(self):
        pass

    def test_echo_sessions_has_ended(self):
        pass
