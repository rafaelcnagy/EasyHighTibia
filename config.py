import configparser

config = configparser.ConfigParser()
config.read('config.ini')

STEAM_ACCOUNT = config['steam']['account_name']
STEAM_PASSWORD = config['steam']['password']
