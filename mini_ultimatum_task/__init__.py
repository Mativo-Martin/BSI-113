from otree.api import *
import random

doc = """
The Mini Ultimatum Game

Roles:
- Player 1: Select the amount you wish to give Player 2.
- Player 2: Accept proposals from the first player.
- Player 3: Assess the fairness of Player 1's offer decide whether on whether to punish or not 
Both players 1 and 2 lose all of their money if player 3 punishes player 1.
If player 3 does not penalize player 1, player 1 receives his amount, which is also transferred to player 2, and player 2 receives the amount that player 1 sent him.

"""


class C(BaseConstants):
    NAME_IN_URL = 'mini_ultimatum_task'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    ENDOWMENT = cu(200)


class Subsession(BaseSubsession):
    pass



class Group(BaseGroup):
    #defination of player roles and their specific actions

    offer = models.CurrencyField(
        min=0, max=C.ENDOWMENT,
        label="How much money do you wish to send Player 2?",
    )

    punish_decision = models.BooleanField(

        #player 3 decides on whether to punish or not, boolean choices are used
        
        label="Based on the amount player 1 has decided to send , do you choose:",
        choices=[
            [True, 'To Punish'],
            [False, 'Not to Punish']
        ],
        widget=widgets.RadioSelectHorizontal
    )

    def set_payoffs(self):

        #here we get the objects for the various players in the group
        player1 = self.get_player_by_id(1)
        player2 = self.get_player_by_id(2)
        player3 = self.get_player_by_id(3)

        # Check the decision made by Player 3 if is the punish is done the amount endowed is 0,
        #  else we calculate the amount to be deducted from the endowment
        if self.punish_decision:
            player1.payoff = 0
            player2.payoff = 0
        else:
            player1.payoff = 200 - self.offer
            player2.payoff = self.offer
            player3.payoff = 0


class Player(BasePlayer):
    #method to define the specific roles of players in the group and assign them the respective player ID
    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        elif self.id_in_group == 2:
            return 'Player 2'
        else:
            return 'Player 3 (Punisher)'


# Pages for the app
#here we ensure the prompt page is only displayed to the player with value of 1 only
class Offer(Page):
    form_model = 'group'
    form_fields = ['offer']

    def is_displayed(self):
        return self.id_in_group == 1
    
    #method that provided the amount variable which is the endowment
    def vars_for_template(self):
        return {
            'endowment': C.ENDOWMENT,
        }


class WaitForOffer(WaitPage):
    pass


class Decision(Page):
    form_model = 'group'
    form_fields = ['punish_decision']

    def is_displayed(self):
        return self.id_in_group == 3
    #method that provided the amount variable which was the endowment and the offer made by player 1
    def vars_for_template(self):
        return {
            'endowment': C.ENDOWMENT,
            'player1_offer': self.group.offer,
        }


class WaitForResults(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        player1 = self.group.get_player_by_id(1)
        player2 = self.group.get_player_by_id(2)
        player3 = self.group.get_player_by_id(3)

        return {
            'player1_offer': self.group.offer,
            'player3_decision': self.group.punish_decision,
            'player1_payout': player1.payoff,
            'player2_offer': player1.group.offer,
            'player2_payout': player2.payoff,
        }
    #method to move to 2nd app, the exit survey
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player:
            return "exit_survey"


page_sequence = [Offer, WaitForOffer, Decision, WaitForResults, Results]
