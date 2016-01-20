#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    Replay utilities
    ----------------

    This module contains everything related to cracking.
    Actually, this makes:

        - Aircrack
        - Wesside

    That's so because wesside has its own cracking option.

"""
import os
from . import Air, WrongArgument
from subprocess import Popen, DEVNULL
from contextlib import suppress


class Aircrack(Air):
    """
        Introduction
        ------------


        Aircrack-ng is a powerful wireless cracking tool.
        Supporting two main attack types (against wep or wpa) it accepts
        different options for each.

        That means you'll only be able to use specific options for specific
        attacks.

        .. param attack: Chosen attack (wep|wpa)
        .. param file_: CAP or IVS file to crack

        The rest of the params are gotten using *args, **kwargs magic,
        so you'll need to manually consult them here.

        General options (Note that you can combine these with wpa or wep)

        ::

            Aircrack('wep|wpa', a=false, essid=false, bssid=false,
                     p=false, E=false, q=false, combine=false, l=false,
                     w=false)

        WEP options:

        ::

            Aircrack('wep', c=False, t=False, h=False, debug=False, m=False,
                      n=False, i=False, f=False, k=False, x=False, x1=False,
                      x2=False, X=False, y=False, K=False, s=False, M=False,
                      wep_decloack=False, ptw_debug=False, oneshot=False)

        WPA options:

        ::

            Aircrack('wpa', S=False, r=False)

     """

    _stop = False
    _allowed_arguments = (
        ('a', False),
        ('essid', False),
        ('bssid', False),
        ('p', False),
        ('q', False),
        ('combine', False),
        ('E', False),
        ('l', False),
        ('w', False),
    )

    _allowed_arguments_wep = (
        ('c', False),
        ('t', False),
        ('h', False),
        ('debug', False),
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
        ('wep_decloack', False),
        ('ptw_debug', False),
        ('oneshot', False)
    )

    _allowed_arguments_wpa = (
        ('S', False),
        ('r', False),
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
        params = self.flags + self.arguments
        line = ["aircrack-ng"] + params + [self.file_]
        self._proc = Popen(line, bufsize=0,
                           env={'PATH': os.environ['PATH']},
                           stderr=DEVNULL, stdin=DEVNULL, stdout=DEVNULL)
        os.system('stty sane')


class Wesside(Air):
    """
        Please referr to wesside-ng's help
        for this.

        This accepts all parameters from wesside-ng's help.
     """

    _stop = False

    _allowed_arguments = (
        ('h', False),
        ('i', False),
        ('n', False),
        ('m', False),
        ('a', False),
        ('c', False),
        ('p', False),
        ('v', False),
        ('t', False),
        ('f', False),
    )

    def __init__(self, interface=False, **kwargs):
        self.interface = interface
        super(self.__class__, self).__init__(**kwargs)

    def start(self):
        """
            Start process.
        """
        params = self.flags + self.arguments
        line = ["wesside-ng"] + params + [self.interface]
        self._proc = Popen(line, bufsize=0,
                           env={'PATH': os.environ['PATH']},
                           stderr=DEVNULL, stdin=DEVNULL, stdout=DEVNULL)
        os.system('stty sane')
