# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2019
#
# SPDX-License-Identifier: MIT

import os
import shutil

import pytest
from kas import kas
from kas.libkas import run_cmd
from kas.repos import Repo, RepoRefError


def test_refspec_switch(changedir, tmpdir):
    """
    Test that the local git clone is correctly updated when switching
    between a commit hash refspec and a branch refspec.
    """
    tdir = str(tmpdir / 'test_refspec_switch')
    shutil.copytree('tests/test_refspec', tdir)
    os.chdir(tdir)

    kas.kas(['shell', 'test.yml', '-c', 'true'])
    (rc, output) = run_cmd(['git', 'symbolic-ref', '-q', 'HEAD'], cwd='kas', fail=False, liveupdate=False)
    assert rc != 0
    assert output.strip() == ''
    (rc, output) = run_cmd(['git', 'rev-parse', 'HEAD'], cwd='kas', fail=False, liveupdate=False)
    assert rc == 0
    assert output.strip() == '907816a5c4094b59a36aec12226e71c461c05b77'
    (rc, output) = run_cmd(['git', 'symbolic-ref', '-q', 'HEAD'], cwd='kas2', fail=False, liveupdate=False)
    assert rc == 0
    assert output.strip() == 'refs/heads/master'

    kas.kas(['shell', 'test2.yml', '-c', 'true'])
    (rc, output) = run_cmd(['git', 'symbolic-ref', '-q', 'HEAD'], cwd='kas', fail=False, liveupdate=False)
    assert rc == 0
    assert output.strip() == 'refs/heads/master'
    (rc, output) = run_cmd(['git', 'symbolic-ref', '-q', 'HEAD'], cwd='kas2', fail=False, liveupdate=False)
    assert rc != 0
    assert output.strip() == ''
    (rc, output) = run_cmd(['git', 'rev-parse', 'HEAD'], cwd='kas2', fail=False, liveupdate=False)
    assert rc == 0
    assert output.strip() == '907816a5c4094b59a36aec12226e71c461c05b77'


def test_refspec_absolute(changedir, tmpdir):
    """
    Test that the local git clone works when a absolute refspec
    is given.
    """
    tdir = str(tmpdir / 'test_refspec_absolute')
    shutil.copytree('tests/test_refspec', tdir)
    os.chdir(tdir)

    kas.kas(['shell', 'test3.yml', '-c', 'true'])
    (rc, output) = run_cmd(['git', 'symbolic-ref', '-q', 'HEAD'], cwd='kas_abs', fail=False, liveupdate=False)
    assert rc == 0
    assert output.strip() == 'refs/heads/master'
    (rc, output_kas_abs) = run_cmd(['git', 'rev-parse', 'HEAD'], cwd='kas_abs', fail=False, liveupdate=False)
    assert rc == 0
    (rc, output_kas_rel) = run_cmd(['git', 'rev-parse', 'HEAD'], cwd='kas_rel', fail=False, liveupdate=False)
    assert rc == 0
    assert output_kas_abs.strip() == output_kas_rel.strip()


def test_url_no_refspec(changedir, tmpdir):
    """
    Test that a repository with url but no refspec raises an error.
    """
    tdir = str(tmpdir / 'test_url_no_refspec')
    shutil.copytree('tests/test_refspec', tdir)
    os.chdir(tdir)
    with pytest.raises(RepoRefError):
        kas.kas(['shell', 'test4.yml', '-c', 'true'])


def test_commit_refspec_mix(changedir, tmpdir):
    """
    Test that mixing legacy refspec with commit/branch raises errors.
    """
    tdir = str(tmpdir / 'test_commit_refspec_mix')
    shutil.copytree('tests/test_refspec', tdir)
    os.chdir(tdir)
    with pytest.raises(RepoRefError):
        kas.kas(['shell', 'test5.yml', '-c', 'true'])
    with pytest.raises(RepoRefError):
        kas.kas(['shell', 'test6.yml', '-c', 'true'])


def test_refspec_warning(capsys, changedir, tmpdir):
    """
    Test that using legacy refspec issues a warning, but only once.
    """
    tdir = str(tmpdir / 'test_refspec_warning')
    shutil.copytree('tests/test_refspec', tdir)
    os.chdir(tdir)
    # needs to be reset in case other tests ran before
    Repo.__legacy_refspec_warned__ = []
    kas.kas(['shell', 'test2.yml', '-c', 'true'])
    assert capsys.readouterr().err.count('Using deprecated refspec for repository "kas2".') == 1
