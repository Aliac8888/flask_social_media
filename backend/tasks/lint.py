#!/usr/bin/env python
"""Run Ruff linter on the source code."""

from os import execv
from sys import argv

import __init__  # noqa: F401

execv(".venv/bin/ruff", ["ruff", "check", *argv[1:]])
