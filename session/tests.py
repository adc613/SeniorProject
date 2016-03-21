from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from Recipes.models import Recipe, GeneralAction, BasicReturnText
from accounts.models import User, LinkAccountToEcho
from .models import AppSession

import json


USER_ID = 'amzn1.account.AM3B000000000000000000000000000'


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
                'userId': USER_ID
                },
            }

        self._response['request'] = {
            'type': kwargs.get('type', 'IntentRequest'),
            'requestId': 'amzn1.echo-api.request.0000-00000-000-00000-00000',
            'timestamp': '2015-05-13T12:34:56Z',
            'intent': {
                'name': kwargs.get('intent_name', 'passcode'),
                'slots': {}
                }
            }

    def create_param(self, **kwargs):
        name = kwargs.get('type', 'AMAZON.STRING')
        param = {
            'name': kwargs['name'],
            'value': kwargs['value']
            }
        self._response['request']['intent']['slots'][name] = param

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
            return_statement='Hello World!1'
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
            amazon_echo=USER_ID,
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
                             name='Number',
                             value=link.passcode)
        print('hello world')
        c = Client()
        resp = c.post(reverse('session:echo_request'),
                      data=json.dumps(request.get_params()),
                      content_type='application/json',
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                      )
        link = LinkAccountToEcho.objects.get(pk=link.pk)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(link.active)
        self.assertEqual(link.user.echo, USER_ID)

    def test_session_has_not_started(self):
        # link echo
        link = LinkAccountToEcho.objects.create(user=self.user)
        request = CreateAlexaRequest(type='IntentRequest',
                                     intent_name='register')
        request.create_param(type='AMAZON.FOUR_DIGIT_NUMBER',
                             name='Number',
                             value=link.passcode)
        c = Client()
        resp = c.post(reverse('session:echo_request'),
                      data=json.dumps(request.get_params()),
                      content_type='application/json',
                      HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                      )
        # create session
        AppSession.objects.create(
            user=self.user,
            amazon_echo=USER_ID,
            current_app=self.recipe
            )
        request = CreateAlexaRequest(type='IntentRequest',
                                     intent_name='not registering')
        for i in range(1, 6):
            resp = c.post(reverse('session:echo_request'),
                          data=json.dumps(request.get_params()),
                          content_type='application/json',
                          HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                          )
            return_text = resp.json()['response']['outputSpeech']['text']
            hacked_instruction_number = int(return_text[len(return_text) - 1])
            self.assertEqual(hacked_instruction_number, i)

    def test_load_application_view(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)
        resp = c.get(reverse('session:load_app'))
        self.assertEqual(resp.status_code, 200)

        resp = c.get(reverse('session:load_app', kwargs={'pk': 1}))
        session = AppSession.objects.get(user=self.user)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(session.current_app, self.recipe)
        print('hello world')
        print(resp.templates)
