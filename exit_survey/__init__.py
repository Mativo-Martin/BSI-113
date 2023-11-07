from otree.api import *

doc = """

The Exit Survey

This app is designed to collect additional information and feedback from participants after completing the The Mini Ultimatum Game. 
	
The survey includes questions about the capital city of Kenya, a math problem, and the population of Kenya.

Thank you for your participation.

"""

class C(BaseConstants):
    NAME_IN_URL = 'ExitSurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    capital_city = models.IntegerField(
        label="What is the capital city of Kenya?",
        choices=[
            [1, 'Kisumu'],
            [2, 'Nairobi'],
            [3, 'Mombasa'],
        ],
        widget=widgets.RadioSelect,
    )

    math_question = models.IntegerField(
        label="What is 14 + 15?",
    )

    kenya_population = models.IntegerField(
        label="What is the population of Kenya?",
    )

    def correct_math_question_answer(self):
    	return self.math_question == 29


# PAGES
class KenyanCapital(Page):
    form_model = 'player'
    form_fields = ['capital_city']


class MathQuestion(Page):
    form_model = 'player'
    form_fields = ['math_question']

    def error_message(self, values):
        if values['math_question'] != 29:
            return 'Your answer to the math question is incorrect. Please try again.'


class KenyanPopulation(Page):
    form_model = 'player'
    form_fields = ['kenya_population']


class ThankYou(Page):
    pass

page_sequence = [KenyanCapital, MathQuestion, KenyanPopulation, ThankYou]
