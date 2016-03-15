from .models import AppSession
from accounts.models import User

import datetime
import dateutil


class AlexaResponse():

    output_speech_types = ['PlainText', 'SSML']
    card_typs = ['Simple', 'LinkAccount']

    def __init__(self, **kwargs):
        self._response = {}

        self._response['version'] = kwargs.get('version', '0.1')
        self._response['shouldEndSession'] = kwargs.get(
            'should_end_session', False)
        self._response['sessionAttributes'] = kwargs.get(
            'sessionAttributes', None)

        self.init_outputSpeech(kwargs)

    def outputSpeech_dict(self, **kwargs):
        try:
            return_statement = kwargs['return_statement']
        except KeyError:
            raise ValueError('return_statement value is absent')
        return_statement_type = kwargs.get('return_statement_type',
                                           'PlaintText')

        output = {}

        if return_statement_type in self.output_speech_types:
            output['type'] = type
        else:
            raise ValueError('Return type {} is not valid'.format(type))

        if output['type'] == 'PlainText':
            output['text'] = return_statement
        elif output['type'] == 'SSML':
            output['ssml'] = return_statement

        return output

    def init_outputSpeech(self, **kwargs):
        self._response['outputSpeech'] = self.outputSpeech_dict(kwargs)

    def init_reprompt(self, **kwargs):
        self._response['reprompt'] = self.outputSpeech_dict(kwargs)

    def init_card(self, **kwargs):
        type = kwargs.get('type', 'simple')
        content = kwargs.get('content', None)
        title = kwargs.get('title', None)

        if type == 'Simple':
            if content is None and title is None:
                return None
            elif content is None:
                raise ValueError('A card_content value is requied')
            elif title is None:
                raise ValueError('a card_title value is required')
        elif type == 'LinkAccount':
            if content is not None or title is not None:
                raise ValueError('Content and title are not applicable')

        card = {'type': type, 'content': content, 'title': title}
        self._response['card'] = card

    def get_response(self):
        return self._response


class AlexaRequest():

    replay_buffer = datetime.timedelta(minutes=5)
    amazon_item_types = [
        'AMAZON.DATE',
        'AMAZON.DURATION',
        'AMAZON.FOUR_DIGIT_NUMBER',
        'AMAZON.NUMBER',
        'AMAZON.TIME',
        'AMAZON.US_CITY',
        'AMAZON.US_FIRST_NAME',
        'AMAZON.US_STATE',
        ]
    custom_item_types = []

    item_types = amazon_item_types + custom_item_types

    def __init__(self, request):
        self._request = request
        if not self.verify_application():
            raise ValueError('Invalid application ID')

    def get_version(self):
        return self._request['version']

    def is_new(self):
        return self._request['session']['new']

    def get_session_id(self):
        return self._request['session']['sessionId']

    def verify_application(self):
        # fix this later
        return True

    def does_user_exists(self):
        # Change everyting to accessToken. Right now we use userId which can
        # change in unique circumstances. accessToken is the proper way to link
        # an account
        user = User.objects.get(echo=self._request['user']['userId'])
        return user is not None

    def get_user(self):
        print('-----hey-----')
        print(self._request)
        print(self._request['session'])
        print(self._request['session']['user'])
        print(self._request['session']['user']['userId'])
        print('-----hey-----')
        return User.objects.get(echo=self._request['session']['user']['userId'])

    def get_user_id(self):
        return self._request['session']['user']['userId']

    def get_session(self):
        return AppSession.objects.get(user=self.get_user(), end=False)

    def is_launch_request(self):
        return self._request['request']['type'] == 'LaunchRequest'

    def get_timestamp(self):
        return dateutil.parser.parse(self._request['request']['timestamp'])

    def check_replay_attack(self):
        time = self.get_timestamp()
        now = datetime.datetime.now()

        return time < now - self.replay_buffer

    def is_intent_request(self):
        return self._request['request']['type'] == 'IntentRequest'

    def is_session_ended_request(self):
        return self._request['request']['type'] == 'SessionEndedRequest'

    def get_request_id(self):
        return self._request['request']['requestId']

    def get_intent_type(self):
        if not self.is_intent_request():
            return None
        return self._request['request']['intent']['name']

    def get_intent_params(self):
        if not self.is_intent_request():
            return None
        params = {}
        for item in self._request['request']['intent']['slots']:
            dummy_type = object()
            for type in self.item_types:
                param = item.get(type, dummy_type)
                if param is dummy_type:
                    params[param['name']] = param['value']
                    break

    def get_session_ended_reason(self):
        if self.is_session_ended_request():
            return self._request['request']['reason']
        return None
