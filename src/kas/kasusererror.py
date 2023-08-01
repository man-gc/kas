# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2023
#
# SPDX-License-Identifier: MIT

"""
    This module provides a common base class for all exceptions
    which are related to user or configuration errors. These exceptions
    should be caught and reported to the user using a meaningful message
    instead of a stacktrace.

    When handling errors in KAS, never return directly using `sys.exit`,
    but instead throw an exception derived from :class:`KasUserError` (for user
    errors), or one derived from `Exception` for internal errors. These
    are then handled centrally, mapped to correct return codes and pretty
    printed.
"""


__license__ = 'MIT'
__copyright__ = 'Copyright (c) Siemens AG, 2023'


class KasUserError(Exception):
    """
    User or input error. Derive all user error exceptions from this class.
    """
    pass


class CommandExecError(KasUserError):
    """
    Failure in execution of a shell command. The `forward_error_code` parameter
    can be used to request the receiver of the exception to `sys.exit` with
    that code instead of a generic one. Only use this in special cases, where
    the return code can actually be related to a single shell command.
    """
    def __init__(self, command, ret_code,
                 forward_ret_code=False):
        self.ret_code = ret_code
        self.forward = forward_ret_code
        message = ["'{}'".format(c) if ' ' in c else c for c in command]
        super().__init__('Command "{}" failed with error {}'
                         .format(' '.join(message), ret_code))


class ArgsCombinationError(KasUserError):
    """
    Invalid combination of CLI arguments provided
    """
    def __init__(self, message):
        super().__init__('Invalid combination of arguments: {}'
                         .format(message))
