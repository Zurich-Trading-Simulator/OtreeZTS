from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    
    def vars_for_template(self):
        """
        Pass processed survey link to the survey page. Processing 
        consists of adding arguments important for the survey to the link.
        """
        l = self.session.config['survey_link']

        # Add some params to the link if desired (e.g. user id)
        #l = l + '?uid=' + str(self.participant.id_in_session)
        
        return dict(processed_survey_link=l,)

page_sequence = [Survey]
