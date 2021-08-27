from ._builtin import Page, WaitPage
from .exitcodes import sha_hash

class Checkout(Page):
    def vars_for_template(self):
        return {'exitcode' : sha_hash(self.participant.code)[0:8]}

page_sequence = [
    Checkout
]
