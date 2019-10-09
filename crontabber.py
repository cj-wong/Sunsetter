from pathlib import Path
from typing import Dict

import yaml
from crontab import CronTab

from config import CONF, LOGGER


PROJECT = 'Sunsetter'


class CronTabber:
    """Handles crontab and job management for Sunsetter."""

    def __init__(self):
        """Initialize CronTabber."""
        self.crontab = CronTab(user=True)

    def new(self, script: str, hour: int, minute: int) -> None:
        """Registers a new job with the `script` to call
        at `hour` and `minute`.

        Args:
            script (str): the script to call in this job; the key of CONF['scripts']
            hour (int): the hour the job will start
            minute (int): the minute the job will start

        """
        job = self.crontab.new(
            command=f"{CONF['scripts']['root']}/{CONF['scripts'][script]}",
            comment=f"{PROJECT}-{script}",
            )
        job.hour.on(hour)
        job.minute.on(minute)
        self.crontab.write()

    def remove_script_jobs(self, script: str) -> int:
        """Removes all jobs that run `script` from cron.

        Args:
            script (str): the script to call in this job; the key of CONF['scripts']

        Returns:
            int: number of jobs removed

        """
        # Will intentionally cause KeyError, etc. if invalid
        CONF['scripts'][script]

        return self.crontab.remove_all(comment=f"{PROJECT}-{script}")

    def register_auto_remove(self) -> None:
        """Registers an auto-remove script. This should only be
        called once, unless the cron job was deleted.

        """
        try:
            assert (CONF['env'] and CONF['root']), 'Configuration not found'
            script = f"{CONF['root']/remove.py}"
            assert Path(script).exists(), 'Script not found'
            CONF['remove']['hour'] and CONF['remove']['minute']
        except (AssertionError, KeyError, TypeError, ValueError) as e:
            print('A fatal error has occurred. More info:')
            print(e)
            LOGGER.error(e)
            raise 

        job = self.crontab.new(
            command=f"{CONF['env']} {script}",
            comment=f"{PROJECT}-auto-remove"
            )
        job.hour.on(CONF['remove']['hour'])
        job.minute.on(CONF['remove']['minute'])
        self.crontab.write()
