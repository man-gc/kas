# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2019
#
# SPDX-License-Identifier: MIT

import os
import stat
import shutil
import pytest
from kas import kas
from kas.repos import PatchApplyError, PatchFileNotFound, PatchMappingError


def test_patch(changedir, tmpdir):
    tdir = str(tmpdir / 'test_patch')
    shutil.copytree('tests/test_patch', tdir)
    cwd = os.getcwd()
    os.chdir(tdir)
    kas.kas(['shell', 'test.yml', '-c', 'true'])
    for f in ['kas/tests/test_patch/hello.sh', 'hello/hello.sh']:
        assert os.stat(f)[stat.ST_MODE] & stat.S_IXUSR
    kas.kas(['shell', 'test.yml', '-c', 'true'])
    os.chdir(cwd)


def test_patch_update(changedir, tmpdir):
    """
        Test that patches are applied correctly after switching a repo from
        a branch to a commit hash and vice-versa with both git and mercurial
        repositories.
    """
    tdir = str(tmpdir / 'test_patch_update')
    shutil.copytree('tests/test_patch', tdir)
    cwd = os.getcwd()
    os.chdir(tdir)
    kas.kas(['shell', 'test.yml', '-c', 'true'])
    kas.kas(['shell', 'test2.yml', '-c', 'true'])
    for f in ['kas/tests/test_patch/hello.sh', 'hello/hello.sh']:
        assert os.stat(f)[stat.ST_MODE] & stat.S_IXUSR
    os.chdir(cwd)


def test_invalid_patch(changedir, tmpdir):
    """
        Test on common errors when applying patches
    """
    tdir = str(tmpdir / 'test_patch_invalid')
    shutil.copytree('tests/test_patch', tdir)
    cwd = os.getcwd()
    os.chdir(tdir)

    with pytest.raises(PatchFileNotFound):
        kas.kas(['shell', 'test-invalid.yml', '-c', 'true'])

    with pytest.raises(PatchMappingError):
        kas.kas(['shell', 'test-invalid2.yml', '-c', 'true'])

    with pytest.raises(PatchApplyError):
        kas.kas(['shell', 'test-invalid3.yml', '-c', 'true'])
    os.chdir(cwd)
