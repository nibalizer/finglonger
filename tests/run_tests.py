#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import subprocess
import tempfile
import sys

import git
import yaml


def create_temp_git_repo():
    temp_git_dir = tempfile.mkdtemp()
    repo = git.Repo.init(temp_git_dir)
    os.makedirs(os.path.join(temp_git_dir, 'envs', 'test'))
    return repo

def get_test_config():
    config = tempfile.NamedTemporaryFile()
    test_config = {
        'environment': 'test'
    }
    config.write(yaml.safe_dump(test_config))
    config.flush()
    return config

def run_finglonger(git_dir, home_dir, config_path):
    try:
        save_cwd = os.getcwd()
        finglonger_path = os.path.abspath(os.path.join(home_dir, '..',
                                                       'finglonger.py'))
        os.chdir(git_dir)
        return subprocess.check_output(['python', finglonger_path, '--config',
                                        config_path])
    finally:
        os.chdir(save_cwd)

home = os.path.dirname(__file__) or '.'
tests_dir = os.path.join(home, 't')
results_dir = os.path.join(home, 'r')
fails = []
for suite in os.listdir(tests_dir):
    print('Found suite: {}'.format(suite))
    suite_path = os.path.join(tests_dir, suite)
    if not os.path.isdir(suite_path):
        continue
    if not os.path.isdir(os.path.join(results_dir, suite)):
        continue

    try:
        repo = create_temp_git_repo()
        config = get_test_config()
        for test in sorted(os.listdir(suite_path)):
            print('  Found test: {}'.format(test), end="")
            test_path = os.path.join(suite_path, test)
            tasks_path = os.path.join(repo.working_tree_dir, 'envs', 'test',
                                      'tasks.yaml')
            shutil.copy(test_path, tasks_path)
            repo.index.add(['envs/test/tasks.yaml'])
            repo.index.commit('Test commit')
            output = run_finglonger(repo.working_tree_dir, home, config.name)
            result_path = os.path.join(
                results_dir, suite, test.rsplit('.yaml', 1)[0])
            with open(result_path) as result_file:
                if output != result_file.read():
                    with tempfile.NamedTemporaryFile() as actual_results:
                        actual_results.write(output)
                        actual_results.flush()
                        subprocess.call(['diff', '-u', result_path,
                                         actual_results.name])
                        fails.append((suite, test))
                        print("  FAIL")
            print("  PASS")
    finally:
        shutil.rmtree(repo.working_tree_dir)

if fails:
    print("Some tests failed! {}".format(fails))
    sys.exit(1)
