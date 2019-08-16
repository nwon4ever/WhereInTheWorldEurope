import response_builder
import quizquestion
import random

# Handler for launch, intent, and session ended Requests. 
# This function routes the incoming request based on type (LaunchRequest,
# IntentRequest, etc.) The JSON body of the request is provided in the event parameter.
def handler(event, context):
    request = event['request']['type']
    if request == "LaunchRequest":
        return on_launch()
    elif request == "IntentRequest":
        return on_intent_request(event)
    elif request == "SessionEndedRequest":
        return handle_on_session_end_request(event)
    
# Called when the user invokes the skill.
def on_launch():
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
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat(event)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help(event)
    elif intent_name == "AMAZON.StartOverIntent":
        return on_launch()
    elif intent_name == "AMAZON.CancelIntent":
        return
    elif intent_name == "AMAZON.StopIntent":
        return
    else:
        session_attributes = event['session']['attributes']
        if not event['request']['intent']['slots']:
            # unrecognized answer
            event['request']['intent']['slots'] = {"Answer" : ""}
            return handle_answer(event)
    #repeat

def handle_answer(event):
    is_game_in_progress = event['session']['attributes'] and event['session']['attributes']['questions']
    if not is_game_in_progress:
        # If the user responded with an answer but there is no game in progress, ask the user
        # if they want to start a new game. Set a flag to track that we've prompted the user.
        return ask_to_start_a_new_game()
    session_attributes = event['session']['attributes']
    user_answer = event['request']['intent']['slots']['Answer']['value']
    game_questions = session_attributes['questions']
    curr_q_ind = session_attributes["current_q_index"]

    if user_answer == game_questions[curr_q_ind][1]:
        session_attributes["score"] += 1
        result = "correct!"
    else:
        result = "incorrect."
    
    session_attributes["current_q_index"] += 1
    if session_attributes["current_q_index"] < int(NUM_GAME_QUESTIONS):
        next_q = game_questions[curr_q_ind + 1][0]
        return response_builder.build_json_response("{0} is {1} Next question. {2}".format(user_answer, result, next_q), "", "", "", session_attributes, False)
    else:
        score = session_attributes["score"]
        session_attributes = {"user_prompted_to_start" : True}
        return response_builder.build_json_response("Game over! You got {0} out of {1} questions correct. Want to play again?".format(score, NUM_GAME_QUESTIONS), "", "", "", session_attributes, False)
    

def handle_dont_know(event):
    session_attributes = event['session']['attributes']
    game_questions = session_attributes['questions']
    curr_q_ind = session_attributes["current_q_index"]

    answer_pass_response = "The answer is {0}.".format(game_questions[curr_q_ind][1])

    session_attributes["current_q_index"] += 1
    if session_attributes["current_q_index"] < int(NUM_GAME_QUESTIONS):
        next_q = game_questions[curr_q_ind + 1][0]
        return response_builder.build_json_response("{0}. Next question. {1}".format(answer_pass_response, next_q), "", "", "", session_attributes, False)
    else:
        score = session_attributes["score"]
        session_attributes = {"user_prompted_to_start" : True}
        return response_builder.build_json_response("{0} Game over! You got {1} out of {2} questions correct. Want to play again?".format(answer_pass_response,score, NUM_GAME_QUESTIONS), "", "", "", session_attributes, False)

def handle_repeat(event):
    session_attributes=event['session']['attributes']
    game_questions = session_attributes['questions']
    curr_q_ind = session_attributes["current_q_index"]
    return response_builder.build_json_response(game_questions[curr_q_ind][0], "", "", "", session_attributes, False)

def handle_stop(event):
    session_attributes = event['session']['attributes']
    core = session_attributes["score"]
    return response_builder.build_json_response("Game over! You got {0} out of {1} questions correct. Thanks for playing!".format(score, NUM_GAME_QUESTIONS), "", "", "", session_attributes, True)

def handle_no(event):
    session_attributes = event['session']['attributes']
    if session_attributes and session_attributes["user_prompted_to_start"]:
        # After being asked "Do you want to start a game?", user said no
        return handle_on_session_end_request(event)
    else:
        return ask_to_start_a_new_game()

def handle_yes(event):
    session_attributes = event['session']['attributes']
    if session_attributes and session_attributes["user_prompted_to_start"]:
        # After being asked "Do you want to start a game?", user said yes
        return on_launch()
    else:
        return ask_to_start_a_new_game()

def handle_help(event):
    helpOutput = "I will ask you " + NUM_GAME_QUESTIONS + " geography related questions. " \
        + "Respond with your best guess. " \
        + "To start a new game at any time, say, start game. " \
        + "To repeat the last question, say, repeat. " \
        + "Would you like to keep playing?"
    return response_builder.build_json_response(helpOutput, "","","", {}, False)

def handle_on_session_end_request(event):
    goodbye = "Goodbye for now!"
    return response_builder.build_json_response(goodbye, "Thanks for playing!","","", {}, True)

def ask_to_start_a_new_game():
    session_attributes = {"user_prompted_to_start" : True}
    speech_output = "There is no game in progress. Do you want to start a new game?"
    return response_builder.build_json_response(speech_output, "","","", session_attributes, False)

# SKILL SPECIFIC LOGIC

NUM_GAME_QUESTIONS = '5';

def populate_game_questions():
  """Build and return the JSON list of questions for this game, no duplicates."""
  indices = random.sample(range(0, len(quizquestion.questions_all)), 5) # If user doesn't specify, choose 5 random questions
  return quizquestion.QuizQuestion.get_game_questions(indices)   

print(populate_game_questions()) 






