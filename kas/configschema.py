# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2020
#
# SPDX-License-Identifier: MIT

'''
    This module contains the schema of the configuration file.
'''
__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2018'

import json
import os

cwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(cwd, 'schema-kas.json'), 'r') as f:
    CONFIGSCHEMA = json.load(f)
