import response_builder
import quizquestion
import random

# Handler for launch, intent, and session ended Requests. 
# This function routes the incoming request based on type (LaunchRequest,
# IntentRequest, etc.) The JSON body of the request is provided in the event parameter.
def handler(event, context):
    request = event['request']['type']
    if request == "LaunchRequest":
        return on_launch(event)
    elif request == "IntentRequest":
        return on_intent_request(event)
    elif request == "SessionEndedRequest":
        return handle_on_session_end_request(event)
    

# Called when the user invokes the skill.
def on_launch(event):
    welcome_message = "Welcome to Where In The World Europe edition! I will ask you " + NUM_GAME_QUESTIONS \
            + " questions, try to get as many right as you can. Just say your best guess. Let's start. "
    reprompt_message = "Try to get as many questions right as you can."
    card_text = "Respond with your best guess for each question."
    card_title = "Welcome to WhereInTheWorld!"

    session_attributes = {"questions" : populate_game_questions(), "current_q_index" : 0, "score" : 0}
    welcome_message += session_attributes["questions"][0][0]
    return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, session_attributes, False)

# Called when a user input is mapped by Alexa to an intent
def on_intent_request(event):
    intent_name = event['request']['intent']['name']
    if intent_name == "AnswerIntent":
        return handle_answer(event)
    elif intent_name == "DontKnowIntent":
        return handle_dont_know(event)
    elif intent_name == "AMAZON.NoIntent":
        return handle_no(event)
    elif intent_name == "AMAZON.YesIntent":
        return handle_yes(event)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help(event)
    elif intent_name == "AMAZON.StartOverIntent":
        return on_launch(event)
    elif intent_name == "AMAZON.CancelIntent":
        return

def handle_answer(event):
    is_game_in_progress = event['session']['attributes'] and event['session']['attributes']['questions']
    if not is_game_in_progress:
        # If the user responded with an answer but there is no game in progress, ask the user
        # if they want to start a new game. Set a flag to track that we've prompted the user.
        session_attributes = {"user_prompted_to_start" : True}
        speech_output = "There is no game in progress. Do you want to start a new game? ";
        return response_builder.build_json_response(speech_output, "","","", session_attributes, False)
    session_attributes = event['session']['attributes']
    user_answer = event['request']['intent']['slots']['Answer']['value']
    game_questions = session_attributes['questions']
    curr_q = session_attributes["current_q_index"]

    if user_answer == game_questions[curr_q][1]:
        session_attributes["score"] += 1
        return response_builder.build_json_response(user_answer + " is correct!", "","","", {}, False)
    else:
        return response_builder.build_json_response(user_answer + " is incorrect! You suck.", "","","", {}, False)

def handle_dont_know(event):
    pass

def handle_no(event):
    session_attributes = event['session']['attributes']
    if session_attributes and session_attributes["user_prompted_to_start"]:
        # After being asked "Do you want to start a game?", user said no
        handle_on_session_end_request(event)

def handle_yes(event):
    session_attributes = event['session']['attributes']
    if session_attributes and session_attributes["user_prompted_to_start"]:
        # After being asked "Do you want to start a game?", user said yes
        pass

def handle_help(event):
    helpOutput = "I will ask you " + NUM_GAME_QUESTIONS + " geography related questions. " \
        + "Respond with your best guess. " \
        + "To start a new game at any time, say, start game. " \
        + "To repeat the last question, say, repeat. " \
        + "Would you like to keep playing?"
    return response_builder.build_json_response(helpOutput, "","","", {}, False)

def handle_on_session_end_request(event):
    goodbye = "Goodbye for now!"
    return response_builder.build_json_response(goodbye, "","","", {}, True)

# SKILL SPECIFIC LOGIC

NUM_GAME_QUESTIONS = '5';

def populate_game_questions():
  """Build and return the JSON list of questions for this game, no duplicates."""
  indices = random.sample(range(0, len(quizquestion.questions_all)), 5) # If user doesn't specify, choose 5 random questions
  return quizquestion.QuizQuestion.get_game_questions(indices)   

print(populate_game_questions()) 
