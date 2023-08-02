# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2018
#
# SPDX-License-Identifier: MIT
"""
    This plugin implements the ``kas build`` command.

    When this command is executed, kas will checkout repositories, setup the
    build environment and then invoke bitbake to build the targets selected
    in the chosen config file.

    For example, to build the configuration described in the file
    ``kas-project.yml`` you could run::

        kas build kas-project.yml
"""

import logging
import subprocess
import sys

from kas.config import Config
from kas.context import create_global_context
from kas.kasusererror import CommandExecError
from kas.libcmds import Command, Macro
from kas.libkas import find_program, run_cmd, setup_parser_common_args

__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2017-2018'


class Build:
    """
    This class implements the build plugin for kas.
    """

    name = 'build'
    helpmsg = (
        'Checks out all necessary repositories and builds using bitbake as ' 'specified in the configuration file.'
    )

    @classmethod
    def setup_parser(cls, parser):
        """
        Setup the argument parser for the build plugin
        """

        setup_parser_common_args(parser)
        parser.add_argument(
            'extra_bitbake_args',
            nargs='*',
            help='Extra arguments to pass to bitbake ' '(typically requires separation via \'--\')',
        )
        parser.add_argument('--target', action='append', help='Select target to build')
        parser.add_argument('-c', '--cmd', '--task', dest='task', help='Select which task should be executed')

    def run(self, args):
        """
        Executes the build command of the kas plugin.
        """

        if args.config and args.config.startswith('-'):
            args.extra_bitbake_args.insert(0, args.config)
            args.config = None

        ctx = create_global_context(args)
        ctx.config = Config(ctx, args.config, args.target, args.task)

        macro = Macro()
        macro.add(BuildCommand(args.extra_bitbake_args))
        macro.run(ctx, args.skip)


class BuildCommand(Command):
    """
    Implements the bitbake build step.
    """

    def __init__(self, extra_bitbake_args):
        super().__init__()
        self.extra_bitbake_args = extra_bitbake_args

    def __str__(self):
        return 'build'

    def execute(self, ctx):
        """
        Executes the bitbake build command.
        """
        # Start bitbake build of image
        bitbake = find_program(ctx.environ['PATH'], 'bitbake')
        cmd = [
            bitbake,
            '-c',
            ctx.config.get_bitbake_task(),
            *self.extra_bitbake_args,
            *ctx.config.get_bitbake_targets(),
        ]
        if sys.stdout.isatty():
            logging.info('%s$ %s', ctx.build_dir, ' '.join(cmd))
            ret = subprocess.call(cmd, env=ctx.environ, cwd=ctx.build_dir)
            if ret != 0:
                raise CommandExecError(cmd, ret)
        else:
            run_cmd(cmd, cwd=ctx.build_dir)


__KAS_PLUGINS__ = [Build]
