#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import subprocess
from contextlib import suppress
from . import Air, PATH


class Airmon(Air):
    """
        Airmon-ng object.

        It doubles as a context manager.
        So you can call it as

        ::

            wifi = Airmon().start('wlan0')
            Airmon('smoothie0').stop()
            Airmon('wlan0').check()

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
        self.interface = interface  #: Wireless interface
        super(self.__class__, self).__init__()

    def _do_action(self, what):
        """
            Execute airmon-ng with MON_PREFIX and PATH set.
        """
        env = {'PATH': PATH, 'MON_PREFIX': 'smoothie'}
        return subprocess.check_output(["airmon-ng", what,
                                        self.interface], env=env)

    def start(self):
        """
            Executes

            ::

                airmon-ng  start <WIFI>

            and replaces self.interface with the monitor interface.
        """
        ret = self._do_action('start')

        for asg in re.finditer(r'(.*) on (.*)\)', ret.decode()):
            self.interface = asg.group(2)
            return self.interface

    def stop(self):
        """
            Stops monitor mode on current interface
        """
        with suppress(subprocess.CalledProcessError):
            self._do_action('stop')
