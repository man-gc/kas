# kas - setup tool for bitbake based projects
#
# Copyright (c) Peter Hatina, 2021
# Copyright (c) Siemens AG, 2021-2022
#
# SPDX-License-Identifier: MIT

import os
import pathlib
import re
import shutil

import pytest
from kas import kas


def test_build_dir_is_placed_inside_work_dir_by_default(changedir, tmpdir):
    conf_dir = str(tmpdir / 'test_env_variables')
    shutil.copytree('tests/test_environment_variables', conf_dir)

    os.chdir(conf_dir)

    kas.kas(['checkout', 'test.yml'])

    assert os.path.exists(os.path.join(os.getcwd(), 'build', 'conf'))


def test_build_dir_can_be_specified_by_environment_variable(changedir, tmpdir):
    conf_dir = str(tmpdir / 'test_env_variables')
    build_dir = str(tmpdir / 'test_build_dir')
    shutil.copytree('tests/test_environment_variables', conf_dir)
    os.chdir(conf_dir)

    os.environ['KAS_BUILD_DIR'] = build_dir
    kas.kas(['checkout', 'test.yml'])
    del os.environ['KAS_BUILD_DIR']

    assert os.path.exists(os.path.join(build_dir, 'conf'))


def _test_env_section_export(changedir, tmpdir, bb_env_var, bb_repo):
    conf_dir = pathlib.Path(str(tmpdir / 'test_env_variables'))
    env_out = conf_dir / 'env_out'
    bb_env_out = conf_dir / 'bb_env_out'
    init_build_env = conf_dir / 'oe-init-build-env'

    shutil.copytree('tests/test_environment_variables', str(conf_dir))
    os.chdir(str(conf_dir))

    # Overwrite oe-init-build-env script
    # BB_ENV_* filter variables are only exported by
    # kas when they are already exported in the setup environment script
    script = """#!/bin/sh
    export %s="FOO"
    export PATH="%s/%s/bin:${PATH}"
    """ % (
        bb_env_var,
        str(conf_dir),
        bb_repo,
    )
    init_build_env.write_text(script)
    init_build_env.chmod(0o775)

    # Before executing bitbake, first get the bitbake.conf
    kas.kas(['checkout', 'test_env.yml'])
    shutil.copy(str(conf_dir / bb_repo / 'conf' / 'bitbake.conf'), str(pathlib.Path('build') / 'conf' / 'bitbake.conf'))

    kas.kas(['shell', '-c', 'env > %s' % env_out, 'test_env.yml'])
    kas.kas(['shell', '-c', 'bitbake -e > %s' % bb_env_out, 'test_env.yml'])

    # Check kas environment
    test_env = {}
    with env_out.open() as f:
        for line in f.readlines():
            key, val = line.split("=", 1)
            test_env[key] = val.strip()

    # Variables with 'None' assigned should not be added to environment
    with pytest.raises(KeyError):
        _ = test_env['TESTVAR_WHITELIST']

    assert test_env['TESTVAR_DEFAULT_VAL'] == 'BAR'
    assert 'TESTVAR_WHITELIST' in test_env[bb_env_var]

    # Check bitbake's environment
    test_bb_env = {}
    with bb_env_out.open() as f:
        for line in f.readlines():
            if re.match(r'^#', line):
                continue
            match = re.match(r'(^[a-zA-Z0-9_]+)=\"([a-zA-Z0-9_ ]+)\"', line)
            if match:
                key, val = match.group(1), match.group(2)
                test_bb_env[key] = val.strip()

    assert 'TESTVAR_WHITELIST' in test_bb_env[bb_env_var]
    assert test_bb_env["TESTVAR_DEFAULT_VAL"] == "BAR"


# BB_ENV_EXTRAWHITE is deprecated but may still be used
def test_env_section_export_bb_extra_white(changedir, tmpdir):
    _test_env_section_export(changedir, tmpdir, 'BB_ENV_EXTRAWHITE', 'bitbake_old')


def test_env_section_export_bb_env_passthrough_additions(changedir, tmpdir):
    _test_env_section_export(changedir, tmpdir, 'BB_ENV_PASSTHROUGH_ADDITIONS', 'bitbake_new')
