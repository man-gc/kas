# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2021
#
# SPDX-License-Identifier: MIT

import os
import shutil
import pytest

if os.getenv('FORCE_ALL_TESTS'):
    import snack
else:
    snack = pytest.importorskip(
                'snack',
                reason='\'python3-newt\' distribution package not installed'
    )

from kas import kas

@pytest.fixture(autouse=True)
def patch_kas(monkeypatch):
    INPUTS = iter([' ', None, ' ', None])
    ACTIONS = iter([None, 'build', None, 'build'])
    SELECTIONS = iter([0, 3])

    def mock_runOnce(unused1):
        return next(INPUTS)

    def mock_buttonPressed(unused1, unused2):
        return next(ACTIONS)

    def mock_current(unused1):
        return next(SELECTIONS)

    monkeypatch.setattr(snack.GridFormHelp, 'runOnce', mock_runOnce)
    monkeypatch.setattr(snack.ButtonBar, 'buttonPressed', mock_buttonPressed)
    monkeypatch.setattr(snack.Listbox, 'current', mock_current)


def file_contains(filename, expected):
    with open(filename) as file:
        for line in file.readlines():
            if line == expected:
                return True
    return False


def check_bitbake_options(expected):
    with open('build/bitbake.options') as file:
        return file.readline() == expected


def test_menu(monkeypatch, tmpdir):
    tdir = str(tmpdir / 'test_menu')
    shutil.copytree('tests/test_menu', tdir)
    monkeypatch.chdir(tdir)

    # select opt1 & build
    kas.kas(['menu'])
    assert file_contains('build/conf/local.conf', 'OPT1 = "1"\n')
    assert file_contains('.config.yaml', 'build_system: openembedded\n')
    assert check_bitbake_options('-c build target1\n')

    # rebuild test
    kas.kas(['build'])
    assert file_contains('build/conf/local.conf', 'OPT1 = "1"\n')
    assert check_bitbake_options('-c build target1\n')

    # select alternative target & build
    kas.kas(['menu'])
    assert file_contains('build/conf/local.conf', 'OPT1 = "1"\n')
    assert check_bitbake_options('-c build target2\n')


def test_menu_inc_workdir(monkeypatch, tmpdir):
    tdir = str(tmpdir / 'test_menu_inc')
    kas_workdir = str(tmpdir / 'test_menu_inc' / 'out')
    shutil.copytree('tests/test_menu', tdir)
    monkeypatch.chdir(tdir)
    os.mkdir(kas_workdir)
    os.environ['KAS_WORK_DIR'] = kas_workdir
    kas.kas(['menu'])
    del os.environ['KAS_WORK_DIR']


def test_menu_implicit_workdir(monkeypatch, tmpdir):
    tdir = str(tmpdir / 'test_menu_iwd')
    kas_workdir = str(tmpdir / 'test_menu_iwd_out')
    shutil.copytree('tests/test_menu', tdir)
    os.mkdir(kas_workdir)
    monkeypatch.chdir(kas_workdir)
    kas.kas(['menu', tdir + '/Kconfig'])
