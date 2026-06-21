"""Pytest configuration.

Ensures the repository root is on ``sys.path`` so tests can import the app's
top-level modules (``shared``, ``digest``, ``views``). Only pytest loads this
file; the app itself never imports it.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
