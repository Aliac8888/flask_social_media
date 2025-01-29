#!/usr/bin/env python
from os import execv
from sys import argv

import __init__  # noqa: F401

execv(".venv/bin/ruff", ["ruff", "check", *argv[1:]])
