#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Replaying options
"""
import os
from . import Air, WrongArgument
from subprocess import Popen, DEVNULL
from contextlib import suppress


class Aircrack(Air):
    """
        Please referr to aircrack-ng's help
        for this.

        This accepts the following parameters from aircrack-ng's help.


        .. TODO::

            Automagically extract this help from airodump-ng =)
     """

    _stop = False
    _allowed_arguments = (
        ('a', False),
        ('e', False),
        ('b', False),
        ('p', False),
        ('q', False),
        ('C', False),
        ('l', False),
        ('w', False),
    )

    _allowed_arguments_wep = (
        ('c', False),
        ('t', False),
        ('h', False),
        ('d', False),
        ('m', False),
        ('n', False),
        ('i', False),
        ('f', False),
        ('k', False),
        ('x', False),
        ('x1', False),
        ('x2', False),
        ('X', False),
        ('y', False),
        ('K', False),
        ('s', False),
        ('M', False),
        ('D', False),
        ('P', False),
        ('1', False),
    )

    _allowed_arguments_wpa = (
        ('E', False),
        ('J', False),
        ('S', False),
        ('r', False),
        (')', False),
    )

    _allowed_attacks = (
        'wpa', 'wep'
    )

    def __init__(self, attack=False, file_=False, **kwargs):
        self.file_ = file_

        if attack not in self._allowed_attacks:
            raise WrongArgument

        self.attack = attack
        extra = tuple()
        with suppress(AttributeError):
            extra = getattr(self, "_allowed_arguments_{}".format(attack))
        self._allowed_arguments = self._allowed_arguments + \
            extra
        super(self.__class__, self).__init__(**kwargs)

    def start(self):
        """
            Start process.
        """
        self._current_execution += 1
        params = self.flags + self.arguments
        line = ["aircrack-ng"] + params + [self.file_]
        self._proc = Popen(line, bufsize=0,
                           env={'PATH': os.environ['PATH']},
                           stderr=DEVNULL, stdin=DEVNULL, stdout=DEVNULL)
        os.system('stty sane')
