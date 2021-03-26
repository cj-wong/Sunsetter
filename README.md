# Sunsetter

*Automated scripts at local sunset*

## Overview

This project checks local sunset time using [Wolfram|Alpha] and runs scripts of your choice
This project aims to automate sunset checking; scripts are intended to be used in conjunction with the check. In particular, you can add scripts to fire around sunset and a fixed point after. For example, you could create external scripts that control an IOT device (smart plug, lightbulb): turn on near sunset and turn off after.

## Usage

After installing [dependencies](#requirements) and following [setup](#setup), run [process.py](process.py).

## Requirements

This code is designed around the following:

- Python 3.7+
    - `requests`
        - `GET` with *[Wolfram|Alpha]*
    - `bs4` to parse the result from `requests`
    - `lxml` for `bs4` to parse
    - `pyyaml` for managing configuration
    - `pendulum` for time calculations
    - `python-crontab` for hooking into `crontab`
    - other [requirements](requirements.txt) 

## Setup

1. Create an account with *[Wolfram|Alpha Developers][WADEV]*.
2. Request an **AppID**. Store this value into `appid` in the configuration file.
3. [Configure](#configuration) the other fields in the configuration file as desired.
4. *(Optional)* Run [crontabber.py] to register cron jobs with both the [process.py](process.py) and the [remove.py](remove.py) scripts. Requires all fields to be filled out.

## [Configuration](config.yaml.example)

- `scripts`: *(required)*
    - `root`: where your scripts live
    - `switch_on`: script called around sunset relative to your `offset`s
    - `switch_off`: script called at `shutdown` time
- `failsafe`: *(optional, but strongly recommended)* failsafe in case the *[Wolfram|Alpha]* APIs can't be reached; treated like sunset time
    - `hour`
    - `minute`
- `sunset`
    - `remove`: *(default: `true`)* whether auto-remove should remove `switch_on` jobs
    - `offset`: offset in time relative to sunset; can be negative (before sunset) or positive (after sunset)
        - `hours`
        - `minutes`
- `run`: *(required for running this project automatically)*
    - `hour`
    - `minute`
- `remove`: *(required for `remove` scripts)*
    - `hour`
    - `minute`
- `shutdown`: *(optional, but recommended)* when to call `switch_off` script
    - `enabled`: *(default: `false`)* whether to use `switch_off`
    - `remove`: *(default: `false`)* whether auto-remove should remove `switch_off` jobs
    - `hour`
    - `minute`
- `env`: *(required for `run` and `remove`)* where the environment is for the project
- `root`: *(required)* where the project root is

⚠️ `scripts` (and `scripts["root"]` and `scripts["switch_on"]`) and `root` are **required**. This project will not function properly without them. (`scripts["switch_off"]` is optional.)

⚠️ For `run`, `remove`, and `shutdown`,  `hour` and `minute` represent when that section will run, at `hour:minute` local time. Compare this with `hours` and `minutes` in section `sunset["offset"]`; **these values instead are relative values from sunset**.

⚠️ If `env` is missing, both the optional `run` and `remove` cron jobs cannot be registered.

⚠️ For `run`, `remove`, and `shutdown`, their child values must also be defined or their respective scripts won't run at all. For `shutdown`, `scripts["switch_off"]` must also be defined.

## Disclaimer

This project is not affiliated with or endorsed by *[Wolfram|Alpha]*. See [LICENSE](LICENSE) for more detail.

[Wolfram|Alpha]: https://www.wolframalpha.com/
[WADEV]: https://developer.wolframalpha.com/portal/myapps/
[crontabber.py]: crontabber.py
[process.py]: process.py
