# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2020
#
# SPDX-License-Identifier: MIT
"""
    This module contains the version of kas.
"""
__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2020'

# Try to define version
try:
    from setuptools_scm import get_version

    __version__ = get_version(root="../..", relative_to=__file__)
except (ImportError, LookupError):
    try:
        from ._version import __version__  # noqa: F401
    except ModuleNotFoundError:
        raise RuntimeError(
            "kas is not correctly installed. "
            "Please install it with pip."
        )

# Please update docs/format-changelog.rst when changing the file version.
__file_version__ = 14
__compatible_file_version__ = 1
