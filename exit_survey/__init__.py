from otree.api import *

doc = """

The Exit Survey

After players finish The Mini Ultimatum Game, this app is meant to gather more data and feedback from them.
The survey asks about Kenya's population, a math problem, and the country's capital city.

Thank you for partcipating in this survey.

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
    kenyan_capital = models.IntegerField(
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

    kenyan_population = models.IntegerField(
        label="What is the population of Kenya?",
    )
        #method to check that the answer to the math question has to be 29(hardcoded)
    def correct_math_question_answer(self):
    	return self.math_question == 29


# Different Pwithin the App
class KenyanCapital(Page):
    form_model = 'player'
    form_fields = ['kenyan_capital']


class MathQuestion(Page):
    form_model = 'player'
    form_fields = ['math_question']
#validation of the answer to the math question ,added error handling for incorrect answer
    def error_message(self, values):
        if values['math_question'] != 29:
            return 'Your answer to the math question is incorrect. Please try again.'


class KenyanPopulation(Page):
    form_model = 'player'
    form_fields = ['kenyan_population']


class ThankYou(Page):
    pass

page_sequence = [KenyanCapital, MathQuestion, KenyanPopulation, ThankYou]
