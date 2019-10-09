# Sunsetter (with [*Wolfram|Alpha*][WA])

## Overview

This project aims to automate sunset checking; scripts are intended to be used in conjunction with the check. In particular, you can add scripts to fire around sunset and a fixed point after. For example, you could create external scripts that control an IOT device (smart plug, lightbulb): turn on near sunset and turn off after.

## Usage

After installing [dependencies](#requirements) and [configuring](#setup) [*Wolfram|Alpha Developers*][WADev] and [`config.yaml`](config.yaml.example), run [`process.py`](process.py).

## Requirements

This code is designed around the following:

- Python 3
    - `requests`
        - `GET` with [*Wolfram|Alpha*][WA]
    - `bs4` to parse the result from `requests`
    - `lxml` for `bs4` to parse
    - `pyyaml` for managing configuration
    - `pendulum` for time calculations
    - `python-crontab` for hooking into `crontab`
    - other [requirements](requirements.txt) 

## Setup

1. Setup with [*Wolfram|Alpha Developers*][WADev].
2. Request an **AppID**.
    - Store this into [`config.yaml`](config.yaml.example) in `appid`.
3. [Fill](#configuration) in the other fields in the configuration file as desired.
4. *(Optional)* Run [`crontabber.py`](crontabber.py) to register cron jobs with both the [`process.py`](process.py) and the [`remove.py`](remove.py) scripts. Requires all fields to be filled out.

## [Configuration](config.yaml.example)

- `scripts`
    - `root`: where your scripts live
    - `switch_on`: called around sunset, with your `offset`s considered
    - `switch_off`: called at `shutdown` time
- `failsafe`: failsafe in case the [*Wolfram|Alpha*][WA] APIs can't be reached; treated as sunset
    - `hour`
    - `minute`
- `sunset`
    - `remove`: *(default: `true`)* whether auto-remove should remove `switch_on` jobs
    - `offset`: how far away in time relative to sunset; can be negative or positive
        - `hours`
        - `minutes`
- `run`: *(required for `run`)*
    - `hour`
    - `minute`
- `remove`: *(required for `remove`)*
    - `hour`
    - `minute`
- `shutdown`: *(optional but recommended)* when to call `switch_off`
    - `enabled`: *(default: `false`)* whether to use `switch_off`
    - `remove`: *(default: `false`)* whether auto-remove should remove `switch_off` jobs
    - `hour`
    - `minute`
- `env`: *(required for `run` and `remove`)* where the environment is for the project
- `root`: *(required for `run` and `remove`)* where the project root is

⚠️ Each section's `hour` and `minute`, if present, represent when that section will run, at `hour:minute` local time. Compare that with `hours` and `minutes` in section `sunset[offset]`; these values instead are relative values from sunset.

⚠️ If `shutdown`, `shutdown[hour]`, `shutdown[minute]`, or `scripts[switch_off]` are missing, the program will warn you but still run everything except call the shutdown (`switch_off`) scripts.

⚠️ If `env` and `root` are missing, both the optional `run` and `remove` scripts cannot be registered as cron jobs.

⚠️ If `run`, `run[hour]`, or `run[minute]` are missing, the optional `run` script cannot be registered as a cron job.

⚠️ If `remove`, `remove[hour]`, or `remove[minute]` are missing, the optional `remove` script cannot be registered as a cron job.

⚠️ Any other missing parameters will cause the program to fail.

## Project Files

- [`config.yaml.example`](config.yaml.example)
    - template configuration; copy to `config.yaml` and follow [setup](#setup)
- [`config.py`](config.py)
    - manages the configuration for other scripts
- [`process.py`](process.py)
    - manages the [*Wolfram|Alpha*][WA] API; can be auto-run
- [`remove.py`](remove.py)
    - removes `switch_on` and/or `switch_off` cron jobs; can be auto-run 
- [`crontabber.py`](crontabber.py)
    - manages `python-crontab` for other scripts

## Disclaimer

This project is not affiliated with or endorsed by [*Wolfram|Alpha*][WA]. See [`LICENSE`](LICENSE) for more detail.

[WA]: https://www.wolframalpha.com/
[WADev]: https://developer.wolframalpha.com/portal/myapps/
