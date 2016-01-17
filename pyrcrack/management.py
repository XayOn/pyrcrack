#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import subprocess
from contextlib import suppress
from . import Air


class Airmon(Air):
    """
        Airmon-ng object.

        It doubles as a context manager.
        So you can call it as

        ::

            wifi = Airmon().start('wlan0')
            Airmon().stop('wlan0')
            Airmon().check('wlan0')

        or as

        ::
            with Airmon('wlan0') as f:
                print(f.interface)

    """

    def __init__(self, interface):
        """
            We need this to use the context manager.
            So I decided to make interface mandatory
        """
        self.interface = interface
        super(self.__class__, self).__init__()

    def _do_action(self, what):
        """
            Generic do_action.
        """
        env = {'PATH': os.environ['PATH'], 'MON_PREFIX': 'smoothie'}
        return subprocess.check_output(["airmon-ng", what,
                                        self.interface], env=env)

    def start(self):
        """
            Start
        """
        ret = self._do_action('start')

        for asg in re.finditer(r'(.*) on (.*)\)', ret.decode()):
            self.interface = asg.group(2)
            return self.interface

    def stop(self):
        """
            Stop
        """
        with suppress(subprocess.CalledProcessError):
            self._do_action('stop')

    def __enter__(self, *args, **kwargs):
        self.start(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
        return self
