#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Aircrack-ng basic attacks
    This module handles as gracefully as it can be common
    aircrack-ng commands.
"""

import os
import tempfile
import logging

logging.basicConfig(level=logging.INFO)


class LaunchError(Exception):
    """
        Generic process launch error
    """
    pass


class WrongArgument(Exception):
    """
        Wrong argument has been passed to a call
    """
    pass


class Air:
    """
        Inherit this
    """
    _writepath = False
    _allowed_arguments = False
    _current_execution = 0
    _proc = False
    _exec_args = {}

    def __init__(self, **kwargs):
        """
            We actually allow only kwargs.
            The arguments must be implicit
            to the action...
        """
        for arg in kwargs:
            if arg not in self._allowed_arguments:
                raise WrongArgument()
        self._exec_args = kwargs

    @property
    def flags(self):
        """
            Returns flags
            yields a tuple
        """
        return ["--{}".format(arg) for arg, value in self._exec_args
                if isinstance(value, bool)]

    @property
    def arguments(self):
        """
            Return arguments
            yields a tuple
        """
        result = []
        for arg, value in self._exec_args:
            if not isinstance(value, bool):
                result.extend(["--{}".format(arg), value])
        return result

    @property
    def writepath(self):
        """
            Where to write things to.
        """
        if not self._writepath:
            tmpdir = tempfile.mkdtemp()
            pid = os.getpid()
            name = "{}_{}".format("airodump", pid)
            self._writepath = os.path.join(tmpdir, name)
        return self._writepath

    @property
    def current_execution(self):
        """
            Returns current execution number formatted for usual
            aircrack output
        """
        return str(self._current_execution).zfill(2)

    @property
    def curr_csv(self):
        """
            Return current execution's csv location
        """
        return "{}-{}.csv".format(self.writepath, self.current_execution)
