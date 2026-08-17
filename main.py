#!/usr/bin/env python3
"""Thin convenience wrapper so `python main.py` keeps working.

Equivalent to `python -m meteo.cli` / the installed `meteo` console script.
"""

import sys

from meteo.cli import main

if __name__ == "__main__":
    sys.exit(main())
