#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stranger.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as `stranger` (if installed)
or ``python -m stranger`` (no install required).
"""
import sys

from stranger.cli import cli as base_command


if __name__ == '__main__':
    # exit using whatever exit code the CLI returned
    sys.exit(base_command())
