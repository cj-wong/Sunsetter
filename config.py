import logging
import logging.handlers

import yaml


class InvalidConfigError(ValueError):
    """An invalid configuration was detected."""

    def __init__(self) -> None:
        """Initialize the error message for invalid configuration."""
        super().__init__('An invalid configuration was detected.')


class TimeError(ValueError):
    """Offsets are not valid times."""

    def __init__(self, message: str) -> None:
        """Initialize the time error with a message."""
        super().__init__(message)


_LOGGER_NAME = 'Sunsetter'

LOGGER = logging.getLogger(_LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)

_FH = logging.handlers.RotatingFileHandler(
    f'{_LOGGER_NAME}.log',
    maxBytes=40960,
    backupCount=5,
    )
_FH.setLevel(logging.DEBUG)

_CH = logging.StreamHandler()
_CH.setLevel(logging.WARNING)

_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
_FH.setFormatter(_FORMATTER)
_CH.setFormatter(_FORMATTER)

LOGGER.addHandler(_FH)
LOGGER.addHandler(_CH)

_MAX_H = 24
_MAX_M = 60

try:
    with open('config.yaml', 'r') as f:
        CONF = yaml.safe_load(f)
        APPID = CONF['appid']
        OFFSET = CONF['sunset']['offset']
        OFFSET_H = OFFSET['hours']
        OFFSET_M = OFFSET['minutes']
        SHUTDOWN = CONF['shutdown']
        SCRIPTS = CONF['scripts']
        if OFFSET_H not in range(-_MAX_H + 1, _MAX_H):
            raise TimeError('OFFSET_H is not within 24 hours')
        if OFFSET_M not in range(-_MAX_M + 1, _MAX_M):
            raise TimeError('OFFSET_M exceeds 60 minutes (use hours)')
except FileNotFoundError:
    LOGGER.error(
        'config.yaml was not found. Create it from config.yaml.example.')
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
