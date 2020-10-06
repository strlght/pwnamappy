# pwnamappy
[![license badge](https://img.shields.io/github/license/strlght/pwnamappy)](https://github.com/strlght/pwnamappy/blob/main/LICENSE) [![static analysis badge](https://github.com/strlght/pwnamappy/workflows/Static%20analysis/badge.svg)](https://github.com/strlght/pwnamappy/actions?query=workflow%3A%22Static+analysis%22)

pwnamppy is a CLI tool for turning pwns from [wpa-sec](https://wpa-sec.stanev.org) into pins on the map.

## Instalation
Python 3.6 or later is required.

    python setup.py install

## Usage
    pwnamappy [-h] (-ws WPA_SEC_KEY | -wsf in-file) -wg WIGLE_KEY [-f FILE]