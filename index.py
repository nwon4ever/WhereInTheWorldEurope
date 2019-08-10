# Handler for launch, intent, and session ended Requests. 
# This function routes the incoming request based on type (LaunchRequest,
# IntentRequest, etc.) The JSON body of the request is provided in the event parameter.
def handler(event, context):
    if event['session']['new']:
        on_session_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return on_intent_request(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_end()

# Called when the session starts.
def on_session_start():
    print("Session Started.")

# Called when the user invokes the skill.
def on_launch(event):
    welcome_message = "Welcome to Where In The World Europe edition! I will ask you " + NUM_GAME_QUESTIONS \
            + " questions, try to get as many right as you can. Just say your best guess. Let's start. "
    reprompt_message = "Try to get as many questions right as you can."
    card_text = "Respond with your best guess for each question."
    card_title = "Welcome to WhereInTheWorld!"
    return build_json_response(welcome_message, card_text, card_title, reprompt_message, False)

def on_session_end():
    print("Session Ended.")

# Called when a user input is mapped by Alexa to an intent
def on_intent_request(event):
    intent_name = event['request']['intent']['name']

# SKILL SPECIFIC LOGIC

NUM_GAME_QUESTIONS = '5';

# JSON RESPONSE HELPER FUNCTIONS

# The response of our Lambda function should be in JSON format. These functions
# are used by both the intent handlers and the request handlers to build the output.
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict

def response_field_builder_with_reprompt_and_card(output_speech_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(output_speech_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def build_json_response(output_speech_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(output_speech_text, card_text, card_title, reprompt_text, value)
    return response_dict