# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2019
#
# SPDX-License-Identifier: MIT

import os

import pytest


@pytest.fixture
def changedir():
    yield
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
