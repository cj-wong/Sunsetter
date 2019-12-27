# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.4] - 2019-12-26
### Fixed
- Issue with [`remove.py`](remove.py) treating `switch_on` jobs as `switch_off` to remove

### Changed
- Minor code changes: relative paths are accepted for `env` in [`config.yaml`](config.yaml.example) provided that `env` is within `root`

## [1.1.3] - 2019-12-25
### Changed
- Use `RotatingFileHandler` for logs
- Minor code polish
- On/off scripts are now called by `cd`ing into the scripts' root and executing from there
- Replaced all `assert`s and `AssertionError`s with more Pythonic checks
- `StreamLogger` set to `INFO`
- Removed and/or replaced duplicating `print`s with logging

## [1.1.2] - 2019-10-12
### Added
- `crontabber.AutoConfigError` - error when registering auto-scripts

### Fixed
- Configuration missing errors on auto-scripts

## [1.1.1] - 2019-10-09
### Changed
- `conf[shutdown][remove]` now dictates whether shutdown/`switch_off` scripts should be added
- logger level for whether to add shutdown scripts is now `info` rather than `warning`

### Fixed
- `env` issue on auto-scripts
- Exceptions not grouped

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
