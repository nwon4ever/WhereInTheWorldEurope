class QuizQuestion:
	"""Represents a quiz question."""

	def __init__(self, question, answer):
		"""Create a new quiz question with its answer. """
		self.question = question
		self.answer = answer

	def question(self):
		"""Getter method for the question text."""
		return self.question

	def answer(self):
		"""Getter method for the answer text."""
		return self.answer

	def __repr__(self):
		return "Question: {0} Answer: {1}\n".format(self.question, self.answer)

	@staticmethod
	def get_game_questions(indices):
		"""Returns a list of QuizQuestions at the specified indices."""
		return [questions_all[ind] for ind in indices]


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