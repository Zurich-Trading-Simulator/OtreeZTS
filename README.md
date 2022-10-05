# ZTS Trading Simulator
This is the repository for the Zurich Trading Simulator (ZTS) a web-based behavior experiment 
in the form of a trading game, designed by the Chair of Cognitive Science - ETH Zurich. 
It is developed using oTree an open-source platform for behavioral research.

For a more detailed documentation read [here](./documentation.pdf).

## Try it out!
This section shows how to quickly run a demo session of the oTree ZTS application, which is intended only for demonstration purposes.
To setup an own customizable experiment of the project please read deployment section [here](#deployment).

1. Open the following URL in a browser: [https://zts.otree.ethz.ch/](https://zts.otree.ethz.ch/)
2. Click on the “ZTS” button to open a demo session
3. Click on the provided link under Single-use links and the session should start in a separate tab.

## Project Structure
- The entire Project is developed in Otree.
- Javascript and CSS Files are stored in `_static/` as suggested by [Otree Documentation](https://otree.readthedocs.io/en/latest/).
- An Otree session (The entire ZTS experiment) contains several sub-sessions:
    - `/ZTS`: x rounds of the trading simulator, where the number of rounds x can be set  by the amount of timeseries files (data file containing the asset prices for each market day) provided to the session config.
    - `/Post_Survey`: A link to a post survey, specified through the session settings.  
- Timeseries Files used for the trading charts are stored in the following way: 
    `/_static/ZTS/timeseries_files/[filename].csv` make sure that you set the list of filenames and the filepath in the session config.
- Reports: In the Data tab download the custom Report for a more detailed summary on every trading action that took place.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
Make sure that python is installed on your machine (you can check this by running `python3 --version`).
Read the Deployment section [here](#deployment) for notes on how to setup an run your own project on a live system. 

1. clone the repository to your local machine
2. cd to the project directory
3. create a new python environment: `python3 -m venv env`
4. activate your virtualenv source: `source env/bin/activate`
5. install dependencies: `pip3 install -r requirements_base.txt`
6. run the developement server: `otree devserver`

**Troubleshooting:**
*Depending on your setup some errors might still arise there are some more details on the above steps [here](./documentation.pdf).*

## Deployment
Running the application locally, is enough for testing purposes, but please be aware that in order to perform any experiments the application needs to be run in a production environment, to guarantee safety and correctness. To deploy the oTreeZTS for production follow the oTree documentation steps [here](https://otree.readthedocs.io/ja/latest/server/intro.html).

## Built With

* [oTree](https://www.otree.org) - A web framework for behavioural multiplayer experiments.



