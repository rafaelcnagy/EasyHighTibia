import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))

STEAM_ACCOUNT = config['steam']['account_name']
STEAM_PASSWORD = config['steam']['password']

driver_path = config['selenium']['driver_path'] if config['selenium']['driver_path'].strip() else '../chromedriver'
SELENIUM_PATH = os.path.join(os.path.dirname(__file__), driver_path)
