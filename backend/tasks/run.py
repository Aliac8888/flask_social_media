#!/usr/bin/env python
"""Run a flask development server."""

import __init__  # noqa: F401

from server.app import create_app
from server.config import be_host, be_port

create_app().run(be_host, be_port, debug=True)
