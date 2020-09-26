from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import pandas as pd
import locale

class IntroPage(Page):
    pass

class TradingPage(Page):
    live_method = 'live_trading_report'

    def js_vars(self):
        """
        Pass data for trading controller to javascript front-end
        """
        timeseries_df = pd.read_csv('_static/ZTS/timeseries_files/timeseries_{}.csv'.format(self.round_number))
        timeseries_points = timeseries_df['AdjustedClose'].to_list()
        timeseries_length = len(timeseries_points)
        timeseries_news = timeseries_df['News'].fillna("").to_list()
        return dict(
            refresh_rate=self.session.config['refresh_rate'],
            data=timeseries_df['AdjustedClose'].to_list(),
            length=timeseries_length,
            news=timeseries_news,
            cash=self.session.config['initial_cash'],
        )

class ResultsPage(Page):
    pass

page_sequence = [IntroPage, TradingPage, ResultsPage]
