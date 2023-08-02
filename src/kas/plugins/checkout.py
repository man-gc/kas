# kas - setup tool for bitbake based projects
#
# Copyright (c) Konsulko Group, 2020
#
# SPDX-License-Identifier: MIT
"""
    This plugin implements the ``kas checkout`` command.

    When this command is executed, kas will checkout repositories and set up
    the build directory as specified in the chosen config file. This command
    is useful if you need to inspect the configuration or modify any of the
    checked out layers before starting a build.

    For example, to setup the configuration described in the file
    ``kas-project.yml`` you could run::

        kas checkout kas-project.yml
"""

from kas.config import Config
from kas.context import create_global_context
from kas.libcmds import Macro
from kas.libkas import setup_parser_common_args

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2018'


class Checkout:
    name = 'checkout'
    helpmsg = (
        'Checks out all necessary repositories and sets up the build '
        'directory as specified in the configuration file.'
    )

    @classmethod
    def setup_parser(cls, parser):
        setup_parser_common_args(parser)

    def run(self, args):
        ctx = create_global_context(args)
        ctx.config = Config(ctx, args.config)

        macro = Macro()
        macro.run(ctx, args.skip)


__KAS_PLUGINS__ = [Checkout]
