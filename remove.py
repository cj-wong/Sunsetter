from config import CONF, LOGGER
from crontabber import CronTabber


CRONTAB = CronTabber()


def remove_switch(mode: str) -> None:
    """Remove switch_mode cron jobs.

    Args:
        mode (str): either 'on' or 'off'

    """
    if mode not in ['on', 'off']:
        LOGGER.error(f'Invalid mode: {mode}')

    trigger = 'sunset' if mode == 'on' else 'shutdown'

    mode = f'switch_{mode}'

    if not CONF[trigger]['remove']:
        message = f'{mode} jobs will not be removed.'
    else:
        jobs = CRONTAB.remove_script_jobs(f'{mode}')
        message = f"Jobs ({mode}) removed: {jobs}"
    LOGGER.info(message)


def main() -> None:
    """Main function for the remove module"""
    LOGGER.info('Beginning cron job removal...')
    for mode in ['on', 'off']:
        remove_switch(mode)
    LOGGER.info('Cron job removal complete.')


if __name__ == '__main__':
    main()
