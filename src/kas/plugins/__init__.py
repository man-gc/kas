# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2017-2018
#
# SPDX-License-Identifier: MIT
"""
    This module contains and manages kas plugins
"""

PLUGINS = {}


def register_plugins(mod):
    """
    Register all kas plugins found in a module
    """
    for plugin in getattr(mod, '__KAS_PLUGINS__', []):
        PLUGINS[plugin.name] = plugin


def load():
    """
    Import all kas plugins
    """
    from . import build, checkout, dump, for_all_repos, menu, shell

    register_plugins(build)
    register_plugins(checkout)
    register_plugins(dump)
    register_plugins(for_all_repos)
    register_plugins(shell)
    register_plugins(menu)


def get(name):
    """
    Lookup a kas plugin class by name
    """
    return PLUGINS.get(name, None)


def all():
    """
    Get a list of all loaded kas plugin classes
    """
    return PLUGINS.values()
