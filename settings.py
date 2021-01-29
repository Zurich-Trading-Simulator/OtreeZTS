from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    session_name="test_session",
    survey_link="https://www.qualtrics.com",
    refresh_rate=500,
    initial_cash=1000000,
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)


SESSION_CONFIGS = [
    dict(
        name='ZTS',
        num_demo_participants=1,
        app_sequence=['ZTS', 'Survey']
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='ZTS_test_room',
        display_name='ZTS Test Room',
        participant_label_file='_rooms/zts_test.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
<b>Zurich Trading Simulation (ZTS)</b>
<p>A web-based behaviour experiment 
in the form of a trading game, designed by the Chair of Cognitive Science - ETH Zurich.</p>
"""

# Change this default secret key to a fully random one after forking.
SECRET_KEY = '2sjpogef4a8#)%ca9_eu8%ba*l_d245lp&*hatrb6oy*u*dud^'

INSTALLED_APPS = ['otree']
