# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.7] - 2021-05-01
### Added
- Added new logger message in [crontabber.py] when creating new cron jobs.
- Added new exception `config.ShutdownDisabled` for when shutdown scripts are disabled.
- Added new function `is_shutdown_time_int()` sure that shutdown time hour and minute are both `int`.

### Changed
- Moved main script contents of [process.py] into new function `main()`.

### Fixed
- #5 - Fixed duplicating shutdown cron jobs even when disabled in the configuration.

## [1.1.6] - 2021-04-30
### Security
- Updated `urllib3`.

## [1.1.5] - 2021-03-26
### Changed
- Rewrote parts of the readme to improve clarity.
- The code has been linted with `Flake8` and `mypy`.
- Any instance of `class Error(Exception)` was removed and replaced in favor of other exceptions. (e.g. `ValueError`) In other words, any subclassed `Error`s now subclass a different exception.
- In [config.py]:
    - Synced changes from my skeleton git repo.
    - Both custom errors `InvalidConfigError` and `TimeError` now subclass `ValueError` rather than `Error`, which was itself a subclass of `Exception`.
    - `MAX_H` and `MAX_M` were marked private, as `_MAX_H` and `_MAX_M` respectively.

### Fixed
- In [process.py]: Fixed `failsafe` being mis-assigned; it was incorrectly assigned `config['failsafe']` when it was meant to be `config.CONF['failsafe']`.
- In [remove.py]: Fixed invalid `mode` in 

### Security
- Updated `pyyaml` and `lxml` for dependabot alerts.

## [1.1.4] - 2019-12-26
### Fixed
- Fixed issue with [remove.py] treating `switch_on` jobs as `switch_off` to remove

### Changed
- Minor code changes: relative paths are accepted for `env` in [config.yaml](config.yaml.example) provided that `env` is within `root`

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
- New [crontabber.py] to manage the `crontab` library
- New [remove.py] to auto-remove cron jobs
- Can now register cron jobs programmatically; simply call `crontabber.py` as main
    - Will register both [process.py] and [remove.py]
- Failsafe implemented in config, if API cannot be reached

### Changed
- Configuration is now stored in [config.py] to be accessible by all new files

## [1.0] - 2019-10-08
### Added
- Initial version

[config.py]: config.py
[crontabber.py]: crontabber.py
[process.py]: process.py
[remove.py]: remove.py
