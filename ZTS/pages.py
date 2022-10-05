from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import locale

class InstructionPage(Page):
    def is_displayed(self):
        return self.round_number == 1

class StartPage(Page):
    def is_displayed(self):
        return self.round_number <= self.session.num_rounds
    
    def vars_for_template(self):
        is_training_round = self.session.config['training_round'] and self.round_number == 1
        return dict(
            is_training_round=is_training_round,
        )

class TradingPage(Page):
    live_method = 'live_trading_report'

    def is_displayed(self):
        return self.round_number <= self.session.num_rounds

    def js_vars(self):
        """
        Pass data for trading controller to javascript front-end
        """
        asset, prices, news = self.subsession.get_timeseries_values()
        return dict(
            refresh_rate=self.subsession.get_config_multivalue('refresh_rate_ms'),
            graph_buffer=self.session.config['graph_buffer'],
            prices=prices,
            news=news,
            asset=asset,
            cash=self.subsession.get_config_multivalue('initial_cash'),
            shares=self.subsession.get_config_multivalue('initial_shares'),
            trading_button_values=self.subsession.get_config_multivalue('trading_button_values')
        )

class ResultsPage(Page):
    def is_displayed(self):
        return self.round_number <= self.session.num_rounds

    def to_human_readable(self, x):
        return '{:,}'.format(int(x))

    def vars_for_template(self):
        return dict(
            cash = self.to_human_readable(self.player.cash),
            shares = self.to_human_readable(self.player.shares),
            share_value = self.to_human_readable(self.player.share_value),
            portfolio_value = self.to_human_readable(self.player.portfolio_value),
            pandl = self.to_human_readable(self.player.pandl)
        )

page_sequence = [InstructionPage, StartPage, TradingPage, ResultsPage]
