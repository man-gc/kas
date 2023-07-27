# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2020
#
# SPDX-License-Identifier: MIT

import os
import shutil
from kas import kas

import pytest

LAYERBASE = '${TOPDIR}/..'


@pytest.fixture
def dokas(tmpdir):
    tdir = str(tmpdir / 'test_layers')
    shutil.copytree('tests/test_layers', tdir)
    os.chdir(tdir)
    kas.kas(['shell', 'test.yml', '-c', 'true'])
    yield
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))


def test_layers_default(dokas):
    match = 0
    with open('build/conf/bblayers.conf', 'r') as f:
        for line in f:
            if '{}/kas '.format(LAYERBASE) in line:
                match += 1
    assert match == 1


def test_layers_include(dokas):
    match = 0
    with open('build/conf/bblayers.conf', 'r') as f:
        for line in f:
            if '{}/kas1/meta-'.format(LAYERBASE) in line:
                match += 1
    assert match == 2


def test_layers_exclude(dokas):
    with open('build/conf/bblayers.conf', 'r') as f:
        for line in f:
            assert '{}/kas2'.format(LAYERBASE) not in line


def test_layers_strip_dot(dokas):
    with open('build/conf/bblayers.conf', 'r') as f:
        lines = f.readlines()
        assert any('{}/kas3 '.format(LAYERBASE) in x for x in lines)
        assert any('{}/kas3/meta-bar'.format(LAYERBASE) in x for x in lines)
