import response_builder
import quizquestion
import random

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
    return on_intent_request(event)

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

    game_info = {"questions" : populate_game_questions(), "current_q_index" : 0, "score" : 0}
    welcome_message += game_info["questions"][0][0]
    return response_builder.build_json_response(welcome_message, card_text, card_title, reprompt_message, game_info, False)

def on_session_end():
    print("Session Ended.")

# Called when a user input is mapped by Alexa to an intent
def on_intent_request(event):
    intent_name = event['request']['intent']['name']
    if intent_name == "AnswerIntent":
    	return handleAnswerRequest(event)
    # elif intentName == "DontKnowIntent":
    #     handleDontKnowRequest(event)

def handleAnswerRequest(event):
	user_answer = event['request']['intent']['slots']['Capital']['value']
	all_game_questions = event['session']['attributes']['questions']
	
	question_number = event['session']['attributes']["current_q_index"]
	if user_answer == all_game_questions[question_number][1]:
		event['session']['attributes']["score"] += 1
		return response_builder.build_json_response(user_answer + " is correct!", "","","", "", False)
	else:
		return response_builder.build_json_response(user_answer + " is incorrect! You suck.", "","","", "", False)
	#next_question = all_game_questions[question_number + 1]
	
	
	#if user_answer == all_game_questions[question_number][1]:
		#event['sessionAttributes']["score"] += 1
		#return response_builder.build_json_response(user_answer + " is correct!" + next_question, "","","", event['session']['attributes'], False)
	#eturn response_builder.build_json_response(user_answer + " is incorrect!" + next_question, "","","", event['session']['attributes'], False)

def handleDontKnowRequest(event):
	pass

# SKILL SPECIFIC LOGIC


NUM_GAME_QUESTIONS = '5';

def populate_game_questions():
  """Build and return the list of questions for this game, no duplicates."""
  indices = random.sample(range(0, len(quizquestion.questions_all)), 5) # If user doesn't specify, choose 5 random questions
  return quizquestion.QuizQuestion.get_game_questions(indices)   

print(populate_game_questions()) 
