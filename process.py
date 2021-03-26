from typing import Tuple

import pendulum
import requests
from bs4 import BeautifulSoup

import config
from crontabber import CronTabber


URL = 'https://api.wolframalpha.com/v2/query'


def check_sunset() -> Tuple[int, int]:
    """Checks sunset time using the Wolfram|Alpha API.

    Returns:
        tuple(int, int): (hour, minute) of the sunset

    """
    try:
        page = requests.get(
            f'{URL}?input=sunset&appid={config.APPID}'
            '&assumption=CalendarEventName'
            )
        soup = BeautifulSoup(page.text, 'lxml')
        for pod in soup.find_all('pod'):
            if pod['id'] == 'Result':
                text = pod.plaintext.text
                time = text.split('\n')[0]
                h_m, period = time.split()[:2]
                hour, minute = [int(d) for d in h_m.split(':')]
                if period.startswith('p'):
                    hour += 12
                message = f'Sunset will be at {hour:02}:{minute:02}'
                config.LOGGER.info(message)
                return (hour, minute)
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        config.LOGGER.warn('Encountered an error. Using failsafe...')
        config.LOGGER.warn(e)
        failsafe = config.CONF['failsafe']
        config.LOGGER.info(
            f"Sunset emulated at {failsafe['hour']:02}:{failsafe['minute']:02}"
            )
        return (failsafe['hour'], failsafe['minute'])


def adjust_time(hour: int, minute: int) -> Tuple[int, int]:
    """Adjusts time from sunset using offset in config.

    Returns:
        tuple(int, int): (hour, minute) of the adjusted time

    """
    today = pendulum.today()
    today = today.add(hours=hour, minutes=minute)
    today = today.add(hours=config.OFFSET_H, minutes=config.OFFSET_M)
    hour = today.hour
    minute = today.minute
    message = f'Scripts will fire at around {hour:02}:{minute:02}'
    config.LOGGER.info(message)
    return (today.hour, today.minute)


if __name__ == '__main__':
    hour, minute = check_sunset()

    try:
        # Implicit check for KeyError, etc.
        config.SCRIPTS['root']
        config.SCRIPTS['switch_on']
    except (KeyError, TypeError, ValueError) as e:
        config.LOGGER.error(e)
        config.LOGGER.error('Scripts will not run. Exiting...')
        raise config.InvalidConfigError

    hour, minute = adjust_time(hour, minute)
    crontab = CronTabber()

    crontab.new(
        'switch_on',
        hour,
        minute
        )

    shutdown = config.CONF['shutdown']
    try:
        # Implicit check for KeyError, etc.
        shutdown['enabled']
        shutdown['remove']
        config.SCRIPTS['switch_off']
        crontab.new(
            'switch_off',
            shutdown['hour'],
            shutdown['minute']
            )
    except (KeyError, TypeError, ValueError) as e:
        config.LOGGER.info('Shutdown is disabled. More info:')
        config.LOGGER.info(e)

    config.LOGGER.info('Completed Sunsetter.')
