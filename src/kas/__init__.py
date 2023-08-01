# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2018
#
# SPDX-License-Identifier: MIT
"""
    kas - setup tool for bitbake based projects
"""

from .__version__ import __version__
from .__version__ import __file_version__, __compatible_file_version__
from .configschema import CONFIGSCHEMA

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2018'

__all__ = ['__version__', '__file_version__',
           '__compatible_file_version__', 'CONFIGSCHEMA']
