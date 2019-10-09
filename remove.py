from config import CONF, LOGGER
from crontabber import CronTabber


CRONTAB = CronTabber()


def remove_switch_on() -> None:
    """Remove switch_on cron jobs."""
    if not CONF['sunset']['remove']:
        message = 'switch_on jobs will not be removed.'
        print(message)
        LOGGER.warn(message)
    else:
        jobs = CRONTAB.remove_script_jobs('switch_on')
        message = f"Jobs (switch_on) removed: {jobs}"
        print(message)
        LOGGER.info(message)


def remove_switch_off() -> None:
    """Remove switch_off cron jobs."""
    if not CONF['shutdown']['remove']:
        message = 'switch_off jobs will not be removed.'
        print(message)
        # By default in config.yaml.example, this is disabled.
        # Don't log it as a warning.
        LOGGER.info(message)
    else:
        jobs = CRONTAB.remove_script_jobs('switch_off')
        message = f"Jobs (switch_off) removed: {jobs}"
        print(message)
        LOGGER.info(message)


def main() -> None:
    """Main function for the remove module"""
    print('Beginning cron job removal...')
    remove_switch_on()
    remove_switch_off()
    print('Complete.')


if __name__ == '__main__':
    main()
