# kas - setup tool for bitbake based projects
#
# Copyright (c) Siemens AG, 2020
#
# SPDX-License-Identifier: MIT

import os
import shutil

from kas import kas


def test_build_system(changedir, tmpdir):
    tdir = str(tmpdir / 'test_build_system')
    shutil.copytree('tests/test_build_system', tdir)
    os.chdir(tdir)

    kas.kas(['shell', 'test-oe.yml', '-c', 'true'])
    with open('build-env', 'r') as f:
        assert f.readline().strip() == 'openembedded'

    kas.kas(['shell', 'test-isar.yml', '-c', 'true'])
    with open('build-env', 'r') as f:
        assert f.readline().strip() == 'isar'

    kas.kas(['shell', 'test-openembedded.yml', '-c', 'true'])
    with open('build-env', 'r') as f:
        assert f.readline().strip() == 'openembedded'
