# ZTS Trading Simulator
This is the repository for the Zurich Trading Simulator (ZTS) a web-based behaviour experiment 
in the form of a trading game, designed by the Chair of Cognitive Science - ETH Zurich. 
It is developed in oTree an open-source platform for behavioral research.

## Project Structure
- The entire Project is developed in Otree built upon Django. Any requirements that are not supported in Otree are built directly in Django.
- Javascript and CSS Files are stored in `_static/` as suggested by [Otree Documentation](https://otree.readthedocs.io/en/latest/).
- An Otree session (The entire ZTS experiment) contains several sub-sessions:
    - `/ZTS`: x rounds of the trading simulator, where the number of rounds x can be set in the `ZTS/models.py`.
    - `/Post_Survey`: A link to a post survey, specified through the session settings.  
- Timeseries Files used for the trading charts are stored in the following way: 
    `/_static/ZTS/timeseries_files/timeseries_[round-nr].csv` make sure that if replacing them, they are in the same format.
- Reports: Download the custom Report for a more detailed trading actions summary.

## TODO:
- [X] Create basic Front End structure
- [X] Store Javascripts seperately as static files
- [X] Take setup values from backend when starting trading
- [X] Set up Server communication during trading
- [X] Store all Trading Reports in DB
- [X] Create a downloadable Report 
- [X] Calculate ROI percent
- [X] Overview after each round
- [X] Process timeseries files and send data to client
- [X] Take in qualtrics links
- [X] Set Payoff after each round
- [X] When buying shares and not enough money buy as much as possible
- [X] Make sure all important values are on Trading Report
- [ ] Find better solution on timeseries file selection in each round
- [ ] If possible make a random_payoff from some random round
- [ ] Allow uploading of timeseries files
- [ ] Finer grained Settings menu

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
Make sure to use `python 3.6` if possible to avoid any problems with Otree.
See deployment for notes on how to deploy the project on a live system. 

1. clone the repository to your local machine
2. cd to the project directory
3. create a new python environment: `python3 -m venv env_name`
4. activate your virtualenv source: `bin/activate`
5. install dependencies: `pip install -r requirements_base.txt`
6. run the developement server: `otree devserver`

## Testing

TODO

## Deployment

TODO

## Built With

* [oTree](http://www.otree.org) - A web framework for behavioural multiplayer experiments.
* [Django](https://www.djangoproject.com/) - The Django webframework.



