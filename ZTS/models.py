from otree.db.models import Model, ForeignKey
from django.db import models as models_django
import datetime
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

author = ''

doc = """
Zurich Trading Simulation (ZTS)
A web-based behaviour experiment in the form of a trading game, 
designed by the Chair of Cognitive Science - ETH Zurich.
"""


class Constants(BaseConstants):
    name_in_url = 'ZTS'
    players_per_group = None
    num_rounds = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    def live_trading_report(self, id_in_group, payload):
        """
        Accepts the "daily" trading Reports from the front end and
        further processes them.
        :param id_in_group: id of player in group
        :param payload: trading report
        :return:
        """

        #print('received a report from', id_in_group, ':', payload)
        p = self.get_player_by_id(id_in_group)
        p.cash = payload['cash']
        p.shares = payload['owned_shares']
        p.share_value = payload['share_value']
        p.portfolio_value = payload['portfolio_value']
        p.pandl = payload['pandl']

        tradingaction = p.tradingaction_set.create()
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
            p.payoff = payload['pandl']

class Player(BasePlayer):
    cash = models.FloatField(initial=1000000)
    shares = models.FloatField(initial=0)
    share_value = models.FloatField(initial=0)
    portfolio_value = models.FloatField(initial=0)
    pandl = models.FloatField(initial=1000000)

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
    yield ['participant', 'action', 'quantity', 'price_per_share', 'cash', 'owned_shares', 'share_value', 'portfolio_value', 'cur_day',
           'asset', 'roi']
    for p in players:
        for ta in p.tradingaction_set.all():
            yield [p.participant.id_in_session, ta.action, ta.quantity, ta.price_per_share, ta.cash, ta.owned_shares, ta.share_value,
                   ta.portfolio_value, ta.cur_day, ta.asset, ta.roi]
