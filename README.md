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
3. Fill in the other fields in the configuration file as desired.
    - `scripts`
        - `root`: where your scripts live
        - `switch_on`: called around sunset, with your `offset`s considered
        - `switch_off`: called at `shutdown` time
    - `sunset`
        - `offset`: how far away in time relative to sunset; can be negative or positive
            - `hours`
            - `minutes`
    - `clean`: currently unused
        - `hour`
        - `minute`
    - `shutdown`: when to call `switch_off`
        - `hour`
        - `minute`

## Project Files

- [`config.yaml.example`](config.yaml.example)
    - template configuration; copy to `config.yaml` and follow [setup](#setup)
- [`process.py`](process.py)
    - the script for this project

## Disclaimer

This project is not affiliated with or endorsed by [*Wolfram|Alpha*][WA]. See [`LICENSE`](LICENSE) for more detail.

[WA]: https://www.wolframalpha.com/
[WADev]: https://developer.wolframalpha.com/portal/myapps/
