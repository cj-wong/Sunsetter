from typing import Any, Tuple

import pendulum
import requests
from bs4 import BeautifulSoup

import config
from crontabber import CronTabber


URL = 'https://api.wolframalpha.com/v2/query'


def check_sunset() -> Tuple[int, int]:
    """Check sunset time using the Wolfram|Alpha API.

    Returns:
        Tuple[int, int]: (hour, minute) of the sunset

    Raises:
        KeyError: if local sunset could not be determined from Wolfram|Alpha
            and failsafe was not configured

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
        else:
            raise ValueError(
                'Could not determine local sunset from Wolfram|Alpha.')
    except (AttributeError, KeyError, TypeError, ValueError) as e:
        config.LOGGER.warn('Encountered an error. Using failsafe...')
        config.LOGGER.warn(e)
        try:
            failsafe = config.CONF['failsafe']
            failsafe_time = f"{failsafe['hour']:02}:{failsafe['minute']:02}"
            config.LOGGER.info(
                f"Sunset emulated at {failsafe_time}."
                )
            return (failsafe['hour'], failsafe['minute'])
        except KeyError as e:
            config.LOGGER.error('Failsafe was not configured. Exiting...')
            raise e


def adjust_time(hour: int, minute: int) -> Tuple[int, int]:
    """Adjust time from sunset using offset in config.

    Returns:
        Tuple[int, int]: (hour, minute) of the adjusted time

    """
    today = pendulum.today().at(hour, minute)
    today = today.add(hours=config.OFFSET_H, minutes=config.OFFSET_M)
    hour = today.hour
    minute = today.minute
    message = f'Scripts will run at around {hour:02}:{minute:02}'
    config.LOGGER.info(message)
    return (today.hour, today.minute)


def is_shutdown_time_int(hour: Any, minute: Any) -> bool:
    """Check if shutdown time are numbers.

    Args:
        hour (Any): hour according to user config
        minute (Any): minute according to user config

    Returns:
        bool: True if both are numbers

    """
    return type(hour) is int and type(minute) is int


def main() -> None:
    """Run the main script."""
    hour, minute = check_sunset()

    try:
        if not (config.SCRIPTS['root'] and config.SCRIPTS['switch_on']):
            raise ValueError
    except (KeyError, ValueError) as e:
        config.LOGGER.error('Your configuration is malformed. More info:')
        config.LOGGER.error(e)
        config.LOGGER.info('Exiting...')
        raise config.InvalidConfigError from e

    hour, minute = adjust_time(hour, minute)
    crontab = CronTabber()

    crontab.new('switch_on', hour, minute)

    shutdown = config.CONF['shutdown']
    try:
        if not shutdown['enabled']:
            raise config.ShutdownDisabled
        if not (shutdown['remove'] and config.SCRIPTS['switch_off']):
            raise ValueError
        if not is_shutdown_time_int(shutdown['hour'], shutdown['minute']):
            raise ValueError
    except (ValueError, config.ShutdownDisabled) as e:
        config.LOGGER.info('Shutdown is disabled. More info:')
        config.LOGGER.info(e)
    else:
        crontab.new('switch_off', shutdown['hour'], shutdown['minute'])
    finally:
        config.LOGGER.info('Completed Sunsetter.')


if __name__ == '__main__':
    main()
