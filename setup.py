#!/usr/bin/env python
"""Postilion."""

import os
import sys
import subprocess
from setuptools import setup

action = sys.argv[1]


def update_reqs():
    """Updates requirements files."""
    if not os.path.exists('Pipfile'):
        return
    subprocess.check_call('pipenv lock', shell=True)
    subprocess.check_call(
        'pipenv lock -r | cut -d\- -f1 > tools/pip-requires',
        shell=True)
    subprocess.check_call(
        'pipenv lock --dev -r |cut -d\- -f1 > tools/test-requires',
        shell=True)


if action == "update_requirements":
    update_reqs()
    sys.exit(0)
elif action == "build_sphinx":
    subprocess.check_call('pip install -e ".[doc]"', shell=True)
elif 'dist' in action:
    update_reqs()

setup(setup_requires=['pbr>=1.9', 'setuptools>=17.1', 'pytest-runner'],
      pbr=True)
