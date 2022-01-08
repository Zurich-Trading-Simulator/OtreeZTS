from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd
import locale

class InstructionPage(Page):
    def is_displayed(self):
        return self.round_number == 1

class StartPage(Page):
    def is_displayed(self):
        return self.round_number <= self.session.config['num_rounds']
    
    def vars_for_template(self):
        is_training_round = self.session.config['training_round'] and self.round_number == 1
        return dict(
            is_training_round=is_training_round,
        )

class TradingPage(Page):
    live_method = 'live_trading_report'

    def is_displayed(self):
        return self.round_number <= self.session.config['num_rounds']

    def js_vars(self):
        """
        Pass data for trading controller to javascript front-end
        """
        timeseries_df = pd.read_csv('_static/ZTS/timeseries_files/{}_{}.csv'.format(
            self.session.config['timeseries_file'], self.round_number))
        timeseries_points = timeseries_df['AdjustedClose'].to_list()
        timeseries_length = len(timeseries_points)

        timeseries_news = [""] * timeseries_length
        if 'News' in timeseries_df:
            timeseries_news = timeseries_df['News'].fillna("").to_list()
        return dict(
            refresh_rate=self.session.config['refresh_rate'],
            graph_buffer=self.session.config['graph_buffer'],
            data=timeseries_df['AdjustedClose'].to_list(),
            share1=timeseries_df['Share1'].to_list(),
            share2=timeseries_df['Share2'].to_list(),
            share3=timeseries_df['Share3'].to_list(),
            share4=timeseries_df['Share4'].to_list(),
            share5=timeseries_df['Share5'].to_list(),
            share6=timeseries_df['Share6'].to_list(),
            length=timeseries_length,
            news=timeseries_news,
            cash=self.session.config['initial_cash'],
        )

class ResultsPage(Page):
    def is_displayed(self):
        return self.round_number <= self.session.config['num_rounds']

page_sequence = [InstructionPage, StartPage, TradingPage, ResultsPage]
