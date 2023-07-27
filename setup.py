# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2019
#
# SPDX-License-Identifier: MIT
"""
    Setup script for kas, a setup tool for bitbake based projects
"""

from os import path
from setuptools import setup, find_packages

from kas import __version__

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2019'

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='kas',
    version=__version__,

    scripts=['kas-container'],

    description='Setup tool for bitbake based projects',
    long_description=LONG_DESCRIPTION,

    maintainer='Jan Kiszka',
    maintainer_email='jan.kiszka@siemens.com',

    url='https://github.com/siemens/kas',
    download_url=('https://github.com/siemens/'
                  'kas/archive/{version}.tar.gz'.format(version=__version__)),

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='OpenEmbedded bitbake development',

    packages=find_packages(),

    package_data={'kas': ['*.json']},

    entry_points={
        'console_scripts': [
            'kas=kas.kas:main',
        ],
    },

    install_requires=[
        'PyYAML>=3.0,<6',
        'distro>=1.0.0,<2',
        'jsonschema>=2.5.0,<4',
        'kconfiglib>=14.1.0,<15',
    ],

    # At least python 3.6 is needed by now:
    python_requires='>=3.6',
)
