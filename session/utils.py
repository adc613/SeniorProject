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
