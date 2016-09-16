#!/usr/bin/python

import os
import sys
import subprocess
import tempfile

import yaml


def validate_config(config):
    max_tasks = config.get('max_tasks')
    if max_tasks is None:
        config['max_tasks'] = 5
    return config


def validate_environment(config):
    if os.path.isfile("tasks.yaml"):
        pass
    else:
        print "Tasks file not found, are you in the right directory?"
        sys.exit(1)


def git_cmd(command):
    p = subprocess.Popen(command.split(' '),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out, err


def process_task(task):
    print "Finglongering..."
    print task['name']
    temp, temp_name = tempfile.mkstemp()
    print temp_name
    f = os.fdopen(temp, 'w')
    f.write(task['shell'])
    f.close()
    os.chmod(temp_name, 0755)
    p = subprocess.Popen(["/bin/bash", temp_name],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    print err


if __name__ == "__main__":
    config_file = os.environ['HOME'] + "/.config/finglonger/config.yaml"
    if os.path.isfile(config_file):
        with open(config_file) as f:
            config = yaml.load(f.read())
    else:
        print "Config file not found: {0}".format(config_file)
        sys.exit(1)

    config = validate_config(config)
    validate_environment(config)

    git_cmd('git checkout master')
    with open("tasks.yaml") as f:
        master_tasks = yaml.load(f.read())

    git_cmd('git checkout done')
    with open("tasks.yaml") as f:
        done_tasks = yaml.load(f.read())

    git_cmd('git checkout master')

    print "Tasks on master", len(master_tasks)
    print "Tasks on done", len(done_tasks)
    num_tasks = len(master_tasks) - len(done_tasks)
    print "Tasks to do", num_tasks
    if num_tasks > config['max_tasks']:
        print "Error, too many tasks found ", num_tasks
        print "Cowardly refusing to do anything"
        print "If this is really what you want, modify max_tasks in config"
        sys.exit(1)

    for i in done_tasks:
        master_tasks.remove(i)
    for task in master_tasks:
        process_task(task['task'])

    git_cmd('git checkout done')
    git_cmd('git merge master')
    git_cmd('git push origin done')
    git_cmd('git checkout master')
