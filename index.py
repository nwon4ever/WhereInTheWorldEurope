import response_builder

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
    return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, False)

def on_session_end():
    print("Session Ended.")

# Called when a user input is mapped by Alexa to an intent
def on_intent_request(event):
    intent_name = event['request']['intent']['name']

# SKILL SPECIFIC LOGIC

NUM_GAME_QUESTIONS = '5';