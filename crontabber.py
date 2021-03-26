from pathlib import Path

from crontab import CronTab

from config import CONF, LOGGER


PROJECT = 'Sunsetter'


class AutoConfigError(RuntimeError):
    """Error on configuring/registering auto-run jobs."""

    def __init__(self):
        """Initialize the error with a message."""
        super().__init__('Could not register auto-run jobs')


class CronTabber:
    """Handles crontab and job management for Sunsetter."""

    def __init__(self):
        """Initialize CronTabber with current user's crontab."""
        self.crontab = CronTab(user=True)

    def new(self, script: str, hour: int, minute: int) -> None:
        """Register the script called at `hour:minute` as a new cron job.

        Args:
            script (str): the script to call in this job; must be a child key
                of CONF['scripts']
            hour (int): the hour the job will start
            minute (int): the minute the job will start

        """
        command = f"cd {CONF['scripts']['root']} && {CONF['scripts'][script]}"
        job = self.crontab.new(
            command=command,
            comment=f"{PROJECT}-{script}",
            )
        job.hour.on(hour)
        job.minute.on(minute)
        self.crontab.write()

    def remove_script_jobs(self, script: str) -> int:
        """Remove all jobs that run `script` from cron.

        Args:
            script (str): the script to call in this job; must be a child key
                of CONF['scripts']

        Returns:
            int: number of jobs removed

        """
        # Implicit check for KeyError, etc.
        CONF['scripts'][script]

        jobs = self.crontab.remove_all(comment=f"{PROJECT}-{script}")
        self.crontab.write()
        return jobs

    def register_auto(self, script: str, conf: str) -> None:
        """Register an auto-remove script.

        This should only be called once, unless the cron job was deleted.

        Args:
            script (str): the script to register for auto-runs
            conf (str): the configuration section to use;
                must have 'hour' and 'minute' keys

        """
        try:
            if not Path(f"{CONF['root']}/{script}").exists():
                raise FileNotFoundError
            command = f"cd {CONF['root']} && {CONF['env']}/bin/python {script}"
            job = self.crontab.new(
                command=command,
                comment=f"{PROJECT}-auto-{conf}"
                )
            job.hour.on(CONF[conf]['hour'])
            job.minute.on(CONF[conf]['minute'])
            self.crontab.write()
        except (FileNotFoundError, KeyError, TypeError, ValueError) as e:
            LOGGER.error(e)
            raise AutoConfigError


if __name__ == '__main__':
    print('Only run this once, or when/if these cron jobs are removed.')
    crontab = CronTabber()
    autos = [
        ('remove.py', 'remove'),
        ('process.py', 'run')
        ]
    for script, conf in autos:
        print('Registering', script)
        crontab.register_auto(script, conf)
