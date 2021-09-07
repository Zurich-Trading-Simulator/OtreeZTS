import random
import datetime
from otree.db.models import Model, ForeignKey
from django.db import models as models_django
from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Jason Friedman, Student Helper COG, ETHZ'

doc = """
Trading App of the Zurich Trading Simulator (ZTS).
A web-based behaviour experiment in the form of a trading game, 
designed by the Chair of Cognitive Science - ETH Zurich.
"""


class Constants(BaseConstants):
    name_in_url = 'zts'
    players_per_group = None
    num_rounds = 99


class Subsession(BaseSubsession):

    def creating_session(self):
        """
        This function gets called before each creation of a ZTS 
        subsession. We use it to set a random payoff round for 
        each player.
        """
        if self.round_number == 1:
            for player in self.get_players():
                participant = player.participant
                first_round = 1
                if(self.session.config['training_round']):
                    first_round = 2

                # Make some checks if the session parameters are valid    
                if first_round > self.session.config['num_rounds']:
                    raise ValueError('Num rounds cannot be smaller than 1 (or 2 if there is a training session)!')

                participant.vars['round_to_pay'] = random.randint(first_round, self.session.config['num_rounds'])
                
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    cash = models.FloatField(initial=1000000)
    shares = models.FloatField(initial=0)
    share_value = models.FloatField(initial=0)
    portfolio_value = models.FloatField(initial=0)
    pandl = models.FloatField(initial=0)

    def role(self):
        return 'trader'
    def get_cash(self):
        return '{:,}'.format(int(self.cash))
    def get_shares(self):
        return '{:,}'.format(int(self.shares))
    def get_share_value(self):
        return '{:,}'.format(int(self.share_value))
    def get_portfolio_value(self):
        return '{:,}'.format(int(self.portfolio_value))
    def get_pandl(self):
        return '{:,}'.format(int(self.pandl))

    def live_trading_report(self, payload):
        """
        Accepts the "daily" trading Reports from the front end and
        further processes them.
        :param id_in_group: id of player in group
        :param payload: trading report
        """
        #print('received a report from', self.id_in_group, ':', payload)
        self.cash = payload['cash']
        self.shares = payload['owned_shares']
        self.share_value = payload['share_value']
        self.portfolio_value = payload['portfolio_value']
        self.pandl = payload['pandl']
        self.save()

        tradingaction = self.tradingaction_set.create()
        tradingaction.action = payload['action']
        tradingaction.quantity = payload['quantity']
        tradingaction.price_per_share = payload['price_per_share']
        tradingaction.cash = payload['cash']
        tradingaction.owned_shares = payload['owned_shares']
        tradingaction.share_value = payload['share_value']
        tradingaction.portfolio_value = payload['portfolio_value']
        tradingaction.cur_day = payload['cur_day']
        tradingaction.asset = payload['asset']
        tradingaction.roi = payload['roi_percent']
        tradingaction.save()

        # Set payoff if end of round
        if(payload['action'] == 'End'):
            self.set_payoff()

    def set_payoff(self):
        """
        Set the players payoff for the current round to the total portfolio value.
        If we want participants final payoff to be chosen randomly
        from all rounds instead of accumulated (oTree standard) subtract current payoff
        from participants.payoff if we are not in round_to_pay. Also payoff should not 
        count if we are in a training round.
        """
        self.payoff = 0
        '''self.payoff = self.portfolio_value
        random_payoff = self.session.config['random_round_payoff']
        training_round = self.session.config['training_round']
        if(random_payoff and self.round_number != self.participant.vars['round_to_pay']):
            self.participant.payoff -= self.payoff
        elif(training_round and self.round_number == 1):
            self.participant.payoff -= self.payoff'''

class TradingAction(Model):
    ACTIONS = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Start', 'Start'),
        ('End', 'End'),
        ('Hold', 'Hold'),
    ]

    # creates 1:m relation -> this action was made by a certain player
    player = ForeignKey(Player, on_delete=models.CASCADE)

    action = models.CharField(choices=ACTIONS, max_length=10)
    quantity = models.FloatField(initial=0.0)
    time = models_django.DateTimeField(auto_now_add=True)
    price_per_share = models.FloatField()
    cash = models.FloatField()
    owned_shares = models.FloatField()
    share_value = models.FloatField()
    portfolio_value = models.FloatField()
    cur_day = models.IntegerField()
    trade = models.CharField(blank=True, max_length=100)
    asset = models.CharField(blank=True, max_length=100)
    roi = models.FloatField()

def custom_export(players):
    """
    Create a custom export, that allows us to download more 
    detailed trading reports as csv or excel files
    :param players:
    :return:
    """
    # header row
    yield ['session', 'round_nr', 'participant', 'action', 'quantity', 'price_per_share', 'cash', 'owned_shares', 'share_value', 'portfolio_value', 'cur_day',
           'asset', 'roi']
    # data content
    for p in players:
        for ta in p.tradingaction_set.all():
            yield [p.session.code, p.subsession.round_number, p.participant.code, ta.action, ta.quantity, ta.price_per_share, ta.cash, ta.owned_shares, ta.share_value,
                   ta.portfolio_value, ta.cur_day, ta.asset, ta.roi]

