import json
import random
from otree.api import *
c = cu
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
    num_rounds = 20 # Actual num_rounds is specified in session config, by the length of the list 'timeseries_filename'!

class Subsession(BaseSubsession):

    def creating_session(self):
        """
        This function gets called before each creation of a ZTS subsession. We use it to set a random 
        payoff round for each player. If random_round_payoff is set the payoff is generate only by looking
        at one random round. If we have a training_round, then the random_payoff_round will not be the training
        round.
        """
        # The following initial session setup only needs to be called once and not for each subsession
        if self.round_number == 1:

            self.session.num_rounds = len(json.loads(self.session.config['timeseries_filename']))

            for player in self.get_players():
                first_round = 1
                if(self.session.config['training_round']):
                    first_round = 2

                # Make some checks if the session parameters are valid    
                if first_round > self.session.num_rounds:
                    raise ValueError('Num rounds cannot be smaller than 1 (or 2 if there is a training session)!')

                player.participant.vars['round_to_pay'] = random.randint(first_round, self.session.num_rounds)

    def get_config_multivalue(self, value_name):
        """
        Some config values can contain either a list of values (for each round) or a single value
        with this function we can provide a unified way of accessing it independently of what is 
        the actual value format.

        :param value_name: the name of the config variable
        :return: the parsed value for the current round
        """
        parsed_value = json.loads(self.session.config[value_name])
        if isinstance(parsed_value, list):
            assert(len(parsed_value) >= self.session.num_rounds), value_name + ' contains less entries than effective rounds!'
            return parsed_value[self.round_number - 1]
        else:
            return parsed_value

    def get_timeseries_values(self):
        """
        Read this rounds timeseries file and parse the lists of values

        :return : the list of prices and list of news
        """
        path = self.session.config['timeseries_filepath'] + self.get_config_multivalue('timeseries_filename')
        rows = read_csv(path, TimeSeriesFile)
        cols = {k: [dic[k] for dic in rows] for k in ['price', 'news']}
        if 'news' in cols.keys():
            news =  [x if x else '' for x in cols['news']]
        else:
            news = '' * len(cols['price'])
        return cols['price'], news
                
class Group(BaseGroup):
    pass

class Player(BasePlayer):
    cash = models.FloatField(initial=1000000)
    shares = models.FloatField(initial=0)
    share_value = models.FloatField(initial=0)
    portfolio_value = models.FloatField(initial=0)
    pandl = models.FloatField(initial=0)    

    def live_trading_report(self, payload):
        """
        Accepts the "daily" trading Reports from the front end and
        further processes them to store them in the database
        :param payload: trading report
        """
        #print('received a report from', self.id_in_group, ':', payload)
        self.cash = float(payload['cash'])
        self.shares = int(payload['owned_shares'])
        self.share_value = float(payload['share_value'])
        self.portfolio_value = float(payload['portfolio_value'])
        self.pandl = float(payload['pandl'])

        TradingAction.create(
            player=self,
            action=payload['action'],
            quantity = payload['quantity'],
            time = payload['time'],
            price_per_share = payload['price_per_share'],
            cash = payload['cash'],
            owned_shares = payload['owned_shares'],
            share_value = payload['share_value'],
            portfolio_value = payload['portfolio_value'],
            cur_day = payload['cur_day'],
            asset = payload['asset'],
            roi = payload['roi_percent']
        )

        # Set payoff if end of round
        if(payload['action'] == 'End'):
            self.set_payoff()

    def set_payoff(self):
        """
        Set the players payoff for the current round to the total portfolio value.
        If we want participants final payoff to be chosen randomly
        from all rounds instead of accumulatee standard) subtract current payoff
        from participants.payoff if we are not in round_to_pay. Also payoff should not 
        count if we are in a training round.
        """
        self.payoff = 0
        self.payoff = self.portfolio_value
        random_payoff = self.session.config['random_round_payoff']
        training_round = self.session.config['training_round']
        if(random_payoff and self.round_number != self.participant.vars['round_to_pay']):
            self.participant.payoff -= self.payoff
        elif(training_round and self.round_number == 1):
            self.participant.payoff -= self.payoff

class TradingAction(ExtraModel):
    """
    An extra database model that is used to store all the transactions. Each transaction is
    linked to the player that executed it. 
    """
    ACTIONS = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Start', 'Start'),
        ('End', 'End'),
        ('Hold', 'Hold'),
    ]

    player = models.Link(Player)
    action = models.CharField(choices=ACTIONS, max_length=10)
    quantity = models.FloatField(initial=0.0)
    time = models.StringField()
    price_per_share = models.FloatField()
    cash = models.FloatField()
    owned_shares = models.FloatField()
    share_value = models.FloatField()
    portfolio_value = models.FloatField()
    cur_day = models.IntegerField()
    asset = models.CharField(blank=True, max_length=100)
    roi = models.FloatField()

class TimeSeriesFile(ExtraModel):
    date = models.StringField()
    price = models.FloatField()
    news = models.StringField()

def custom_export(players):
    """
    Create a custom export, that allows us to download more 
    detailed trading reports as csv or excel files. 

    NOTE: the custom export will output all Trading actions that are found in the database,
    i.e. also of earlier sessions --> if you do not want this you migth need to implement a filter
    here.

    :param players: queryset of all players in the database
    :yield: a titel row and then the corresponding values one after the other
    """
    # header row
    yield ['session', 'round_nr', 'participant', 'action', 'quantity', 'price_per_share', 'cash', 'owned_shares', 'share_value', 'portfolio_value', 'cur_day',
           'asset', 'roi']
    # data content
    for p in players:
        for ta in TradingAction.filter(player=p):
            yield [p.session.code, p.subsession.round_number, p.participant.code, ta.action, ta.quantity, ta.price_per_share, ta.cash, ta.owned_shares, ta.share_value,
                   ta.portfolio_value, ta.cur_day, ta.asset, ta.roi]
    