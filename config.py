import logging

import yaml


MAX_H = 24
MAX_M = 60

LOGGER = logging.getLogger('sunset')
LOGGER.setLevel(logging.DEBUG)

FH = logging.handlers.RotatingFileHandler(
    'sunset.log',
    maxBytes=4096,
    backupCount=5,
    )
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.INFO)

FH.setFormatter(
    logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
CH.setFormatter(
    logging.Formatter(
        '%(levelname)s - %(message)s'
        )
    )

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
        if OFFSET_H not in range(-MAX_H + 1, MAX_H):
            raise TimeError('OFFSET_H is not within 24 hours')
        if OFFSET_M not in range(-MAX_M + 1, MAX_M):
            raise TimeError('OFFSET_M exceeds 60 minutes (use hours)')
except FileNotFoundError:
    LOGGER.error(
        'config.yaml was not found. Create it from config.yaml.example.'
        )
    LOGGER.warn('Exiting...')
    raise InvalidConfigError
except (KeyError, TypeError, ValueError) as e:
    LOGGER.error('config.yaml is malformed. More information:')
    LOGGER.error(e)
    LOGGER.warn('Exiting...')
    raise InvalidConfigError
except TimeError as e:
    LOGGER.error('Offset values are invalid. More information:')
    LOGGER.error(e)
    LOGGER.warn('Exiting...')
    raise InvalidConfigError


class Error(Exception):
    """Base exception for Sunsetter"""
    pass


class InvalidConfigError(Error):
    """An invalid configuration was detected."""
    def __init__(self) -> None:
        super().__init__('An invalid configuration was detected.')


class TimeError(Error):
    """Offsets are not valid times."""
    def __init__(self, message: str) -> None:
        """Initialize the time error with a message."""
        super().__init__(message)
