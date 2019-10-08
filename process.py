import logging
import sys
from typing import Tuple

import pendulum
import requests
import yaml
from bs4 import BeautifulSoup
from crontab import CronTab


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


MAX_H = 24
MAX_M = 60

PROJECT = 'Sunsetter'


URL = 'https://api.wolframalpha.com/v2/query'

try:
    with open('config.yaml', 'r') as f:
        CONF = yaml.safe_load(f)
        APPID = CONF['appid']
        OFFSET = CONF['sunset']['offset']
        OFFSET_H = OFFSET['hours']
        OFFSET_M = OFFSET['minutes']
        SHUTDOWN = CONF['shutdown']
        SCRIPTS = SCRIPTS
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
    sys.exit(1)
except (KeyError, TypeError, ValueError) as e:
    print('config.yaml is malformed. More information:')
    print(e)
    LOGGER.error(e)
    print('Exiting...')
    sys.exit(1)
except AssertionError as e:
    print('Offset values are invalid. More information:')
    print(e)
    LOGGER.error(e)
    print('Exiting...')
    sys.exit(1)


def check_sunset() -> Tuple[int, int]:
    """Checks sunset time using the Wolfram|Alpha API.

    Returns:
        tuple(int, int): (hour, minute) of the sunset

    """
    page = requests.get(
        f'{URL}?input=sunset&appid={APPID}&assumption=CalendarEventName'
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
            LOGGER.info(message)
            print(message)
            return (hour, minute)


def adjust_time(hour: int, minute: int) -> Tuple[int, int]:
    """Adjusts time from sunset using offset in config.

    Returns:
        tuple(int, int): (hour, minute) of the adjusted time

    """
    today = pendulum.today()
    today = today.add(hours=hour, minutes=minute)
    today = today.add(hours=OFFSET_H, minutes=OFFSET_M)
    hour = today.hour
    minute = today.minute
    message = f'Scripts will fire at around {hour:02}:{minute:02}'
    LOGGER.info(message)
    print(message)
    return (today.hour, today.minute)


def cron_it(crontab: CronTab, script: str, hour: int, minute: int) -> None:
    """Puts the `script` to call at `hour` and `minute` into cron.

    Args:
        crontab (CronTab): the crontab itself
        script (str): the script to call in this job
        hour (int): the hour the job will start
        minute (int): the minute the job will start

    """
    job = crontab.new(
        command=f"{SCRIPTS['root']}/{script}",
        comment=PROJECT,
        )
    if script == SCRIPTS['switch_off']:
        job.comment = 'Sunsetter OFF'
    job.hour.on(hour)
    job.minute.on(minute)
    crontab.write()


if __name__ == '__main__':
    hour, minute = check_sunset()
    SHUTDOWN = CONF['shutdown']
    try:
        assert (
            SHUTDOWN['enabled']
            and SHUTDOWN['hour']
            and SHUTDOWN['minute']
            ), (
            'Shutdown is disabled.'
            )
        assert (
            SCRIPTS['root']
            and SCRIPTS['switch_on']
            and SCRIPTS['switch_off']
            ), (
            'Scripts are not configured.'
            )
    except (AssertionError, KeyError, TypeError, ValueError) as e:
        print('A fatal error has occurred. More info:')
        print(e)
        logger.ERROR(e)
        print('Scripts will not run. Exiting...')
        sys.exit(2)

    hour, minute = adjust_time(hour, minute)
    crontab = CronTab(user=True)

    cron_it(
        crontab,
        SCRIPTS['switch_on'],
        hour,
        minute
        )

    # If you do not plan on ever changing shutdown time, you can
    # comment out this block after having run at least once.
    cron_it(
        crontab,
        SCRIPTS['switch_off'],
        SHUTDOWN['hour'],
        SHUTDOWN['minute']
        )
    ###

    print('Completed Sunsetter.')
