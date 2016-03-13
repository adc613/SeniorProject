def generic_response(return_text, should_session_end):
    response = {
        "version": "0.1",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "Hello Friend it's Alexa"
            },
            "card": {
                "type": "Simple",
                "content": "You're so Cool Adam thanks",
                "title": "Hello World!"
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": return_text
                }
            },
            "shouldEndSession": should_session_end,
            },
        "sessionAttributes": None
    }

    return response


class AlexaResponse():

    output_speech_types = ['PlainText', 'SSML']
    card_typs = ['Simple', 'LinkAccount']

    def __init__(self, **kwargs):
        self._response = {}

        self._response['version'] = kwargs.get('version', '0.1')
        self._response['shouldEndSession'] = kwargs.get(
            'should_end_session': False)
        self._response['sessionAttributes'] = kwargs.get(
            'sessionAttributes': None)


        init_outputSpeech(kwargs)

    def outputSpeech_dict(self, **kwargs):
        try:
            return_statement = kwargs['return_statement']
        except KeyError:
            raise ValueError('return_statement value is absent')
        return_statement_type = kwargs.get('return_statement_type',
                                           'PlaintText')

        output = {}

        if return_statement_type in output_speech_types:
            output['type'] = type
        else:
            raise ValueError('Return type {} is not valid'.format(type))

        if output['type'] == 'PlainText':
            output['text'] = return_statement
        elif output['type'] == 'SSML':
            output['ssml'] = return_statement

        return output

    def init_outputSpeech(self, **kwargs):
        self._response['outputSpeech'] = outputSpeech_dict(kwargs)

    def init_reprompt(self, **kwargs):
        self._response['reprompt'] = outputSpeech_dict(kwargs)

    def init_card(self, **kwargs):
        type = kwargs.get('type', 'simple')
        content = kwargs.get('content', None)
        title = kwargs.get('title', None)

        if type == 'Simple':
            if content == None and title == None:
                return None
            elif content == None:
                raise ValueError('A card_content value is requied')
            elif title == None:
                raise ValueError('a card_title value is required')
        elif type == 'LinkAccount':
            if content != None or title != None:
                raise ValueError('Content and title are not applicable')

        card = {'type': type, 'content': content, 'title': title}
        self._response['card'] = card

    def get_response(self):
        return self._response


class AlexaRequest():
    pass
