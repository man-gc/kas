# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2018
#
# SPDX-License-Identifier: MIT
"""
    This module contains the implementation of the kas context.
"""

import logging
import os

try:
    import distro

    def get_distro_id_base():
        """
        Returns a compatible distro id.
        """
        return distro.like() or distro.id()

except ImportError:
    import platform

    def get_distro_id_base():
        """
        Wrapper around platform.dist to simulate distro.id
        platform.dist is deprecated and will be removed in python 3.7
        Use the 'distro' package instead.
        """
        return platform.dist()[0]


__context__ = None


def create_global_context(args):
    """
    Creates global context as singleton.
    """
    global __context__
    __context__ = Context(args)
    return __context__


def get_context():
    """
    Returns singleton global context.
    """
    return __context__


class Context:
    """
    Implements the kas build context.
    """

    def __init__(self, args):
        work_dir = os.environ.get('KAS_WORK_DIR', os.getcwd())
        self.__kas_work_dir = os.path.abspath(work_dir)
        build_dir = os.environ.get('KAS_BUILD_DIR', os.path.join(self.__kas_work_dir, 'build'))
        self.__kas_build_dir = os.path.abspath(build_dir)
        ref_dir = os.environ.get('KAS_REPO_REF_DIR', None)
        self.__kas_repo_ref_dir = os.path.abspath(ref_dir) if ref_dir else None
        self.setup_initial_environ()
        self.config = None
        self.args = args

    def setup_initial_environ(self):
        """
        Sets the environment variables for processes that are
        started by kas.
        """
        self.environ = {}
        distro_bases = get_distro_id_base().lower().split()
        for distro_base in distro_bases:
            if distro_base in ['fedora', 'suse', 'opensuse']:
                self.environ = {'LC_ALL': 'en_US.utf8', 'LANG': 'en_US.utf8', 'LANGUAGE': 'en_US'}
                break
            elif distro_base in ['debian', 'ubuntu', 'gentoo']:
                self.environ = {'LC_ALL': 'en_US.UTF-8', 'LANG': 'en_US.UTF-8', 'LANGUAGE': 'en_US:en'}
                break
        if self.environ == {}:
            logging.warning('kas: No supported distros found in %s. ' 'No default locales set.', distro_bases)

        for key in [
            'http_proxy',
            'https_proxy',
            'ftp_proxy',
            'no_proxy',
            'SSH_AUTH_SOCK',
            'BB_NUMBER_THREADS',
            'PARALLEL_MAKE',
        ]:
            val = os.environ.get(key, None)
            if val:
                self.environ[key] = val

    @property
    def build_dir(self):
        """
        The path to the build directory
        """
        return self.__kas_build_dir

    @property
    def kas_work_dir(self):
        """
        The path to the kas work directory
        """
        return self.__kas_work_dir

    @property
    def kas_repo_ref_dir(self):
        """
        The reference directory for the repo
        """
        return self.__kas_repo_ref_dir

    @property
    def force_checkout(self):
        return getattr(self.args, 'force_checkout', None)

    @property
    def update(self):
        return getattr(self.args, 'update', None)
