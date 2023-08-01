# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2019
#
# SPDX-License-Identifier: MIT
"""
    Installation using setup.py is no longer supported.
    Use `python -m pip install .` instead.
"""

import sys

from setuptools import setup

sys.exit(__doc__)

# Fake reference so GitHub considers it a real package
setup(name="kas")
