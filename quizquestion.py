class QuizQuestion:
	"""Represents a quiz question."""

	def __init__(self, question, answer):
		"""Create a new quiz question with its answer. """
		self.question = question
		self.answer = answer

	def get_question(self):
		"""Getter method for the question text."""
		return self.question

	def get_answer(self):
		"""Getter method for the answer text."""
		return self.answer

	# def __repr__(self):
	# 	return "Question: {0} Answer: {1}\n".format(self.question, self.answer)

	@staticmethod
	def get_game_questions(indices):
		"""Returns a JSON compatible list of QuizQuestions at the specified indices."""
		game_questions = []
		for ind in indices:
			question_text = questions_all[ind].get_question()
			answer_text = questions_all[ind].get_answer()
			game_questions.append([question_text, answer_text])
		return game_questions


# Idea: At the beginning of the game, users can choose a country/region to focus questions on
questions_england = [
	("What is the capital of the UK?", "London"), 
	("In what country can you find a clock tower called the Big Ben?", "UK")
]
questions_france = [
	("What is the capital of France?", "Paris"), 
	("In which city is the Eiffel Tower located?", "Paris")
]
questions_germany = [
	("What is the capital of Germany", "Berlin"), 
	("Where in the world can you find the world's tallest gothic cathedral, the Cologne Cathedral?", "Germany")
]
questions_other = [
	("Which of the following countries has the highest population? France, Germany, Italy?", "Germany")
]

questions_all = questions_england + questions_france + questions_germany + questions_other
questions_all = [QuizQuestion(q, a) for q, a in questions_all]
print(QuizQuestion.get_game_questions([1]))