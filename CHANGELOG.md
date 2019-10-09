# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1] - 2019-10-08
### Added
- New [`crontabber.py`](crontabber.py) to manage the `crontab` library
- New [`remove.py`](remove.py) to auto-remove cron jobs
- Can now register cron jobs programmatically; simply call `crontabber.py` as main
    - Will register both [`process.py`](process.py) and [`remove.py`](remove.py)
- Failsafe implemented in config, if API cannot be reached

### Changed
- Configuration is now stored in a separate [file](config.py) to be accessible by all new files

## [1.0] - 2019-10-08
### Added
- Initial version
