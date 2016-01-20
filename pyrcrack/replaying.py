#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Replaying options
"""
import os
import time
import psutil
import threading
from . import Air, WrongArgument
from subprocess import Popen, DEVNULL
from contextlib import suppress


class Aireplay(Air):
    """
    TODO
    """

    _stop = False
    _allowed_arguments = (
        ('b', False),
        ('d', False),
        ('s', False),
        ('m', False),
        ('n', False),
        ('u', False),
        ('v', False),
        ('t', False),
        ('f', False),
        ('w', False),
        ('D', False),
        ('x', False),
        ('p', False),
        ('a', False),
        ('c', False),
        ('h', False),
        ('g', False),
        ('F', False),
        ('ignore_negative_one', True),
        ('R', False)
    )

    _allowed_arguments_fakeauth = (
        ('e', False),
        ('o', False),
        ('q', False),
        ('Q', False),
        ('y', False),
        ('T', False)
    )
    _allowed_arguments_arpreplay = (
        ('j', False),
    )
    _allowed_arguments_fragment = (
        ('k', False),
        ('l', False)
    )

    _allowed_attacks = (
        'deauth', 'fakeauth', 'interactive', 'arpreplay',
        'chopchop', 'fragment', 'caffe_latte', 'cfrag', 'migmode')

    def __init__(self, attack=False, interface=False, **kwargs):
        self.interface = interface

        if attack not in self._allowed_attacks:
            raise WrongArgument

        self.attack = attack
        extra = tuple()
        with suppress(AttributeError):
            extra = getattr(self, "_allowed_arguments_{}".format(attack))
        self._allowed_arguments = self._allowed_arguments + \
            extra + (attack, False),
        kwargs[attack] = True
        super(self.__class__, self).__init__(**kwargs)

    def scan(self):
        """
            Get next result: implement in childrens
            Both this and previous one must be
            responsible for duplicates
        """
        self.start()
        while not os.path.exists(self.curr_csv):
            time.sleep(5)

    def watch_process(self):
        """
            Watcher thread.
            This one relaunches airodump eatch time it dies until
            we call stop()
        """
        psutil.wait_procs([psutil.Process(self._proc.pid)],
                          callback=self.start)

    def start(self, _=False):
        """
            Start process.
            psutil sends an argument (that we don't actually need...)
            interface defaults to monitor interface 0 as started by Airmon
        """
        if not self._stop:
            self._current_execution += 1
            params = self.flags + self.arguments
            line = ["aireplay-ng"] + params + [self.interface]
            self._proc = Popen(line, bufsize=0,
                               env={'PATH': os.environ['PATH']},
                               stderr=DEVNULL, stdin=DEVNULL, stdout=DEVNULL)
            os.system('stty sane')

        time.sleep(5)
        watcher = threading.Thread(target=self.watch_process)
        watcher.start()
