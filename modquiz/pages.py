from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class BasePage(Page):

    def is_displayed(self):
        return self.round_number == 1

class Begin(BasePage):

    pass

class ConForm(BasePage):

    pass

class Confirmation(BasePage):

    pass

class Instructions(BasePage):

    pass

class Question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']

    def submitted_answer_choices(self):
        qd = self.player.current_question()
        return [
            qd['choice1'],
            qd['choice2'],
            qd['choice3'],
            qd['choice4']
        ]

    def before_next_page(self):
        self.player.check_correct()
        self.player.set_payoffs()

    timeout_seconds = 15

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct': sum([p.is_correct for p in player_in_all_rounds]),
        }

class Earnings(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

page_sequence = [
    Begin,
    ConForm,
    Confirmation,
    Instructions,
    Question,
    Results,
    Earnings,
]
