import logging

import yaml


MAX_H = 24
MAX_M = 60

LOGGER = logging.getLogger('sunset_log')
LOGGER.setLevel(logging.DEBUG)

FH = logging.FileHandler('sunset.log')
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.WARNING)

FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)

try:
    with open('config.yaml', 'r') as f:
        CONF = yaml.safe_load(f)
        APPID = CONF['appid']
        OFFSET = CONF['sunset']['offset']
        OFFSET_H = OFFSET['hours']
        OFFSET_M = OFFSET['minutes']
        SHUTDOWN = CONF['shutdown']
        SCRIPTS = CONF['scripts']
        assert OFFSET_H in range(-MAX_H + 1, MAX_H), (
            'not within 24 hours'
            )
        assert OFFSET_M in range(-MAX_M + 1, MAX_M), (
            'exceeded 60 minutes (use hours)'
            )
except FileNotFoundError:
    ERR = 'config.yaml was not found. Create it from config.yaml.example.'
    print(ERR)
    LOGGER.error(ERR)
    print('Exiting...')
    raise InvalidConfigError
except (KeyError, TypeError, ValueError) as e:
    print('config.yaml is malformed. More information:')
    print(e)
    LOGGER.error(e)
    print('Exiting...')
    raise InvalidConfigError
except AssertionError as e:
    print('Offset values are invalid. More information:')
    print(e)
    LOGGER.error(e)
    print('Exiting...')
    raise InvalidConfigError


class Error(Exception):
    """Base exception for Sunsetter"""
    pass


class InvalidConfigError(Error):
    """An invalid configuration was detected."""
    def __init__(self):
        super().__init__('An invalid configuration was detected.')
