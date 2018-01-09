"""pyrcrack.

Aircrack-NG python bindings
"""

import abc
import asyncio
import functools
import itertools
import subprocess

import docopt
import stringcase


class ExecutorHelper:
    """Abstract class interface to a shell command."""

    def __init__(self):
        """Set docstring."""
        self.__doc__ = self.helpstr

    @abc.abstractproperty
    def is_async(self):
        """Async."""

    @abc.abstractproperty
    def command(self):
        """Specify command to execute."""

    @property
    @functools.lru_cache()
    def helpstr(self):
        """Extract help string for current command."""
        helpcmd = '{} 2>&1; echo'.format(self.command)
        return subprocess.check_output(helpcmd, shell=True).decode()

    @property
    @functools.lru_cache()
    def usage(self):
        """Extract usage from a specified command."""
        opt = docopt.parse_defaults(self.helpstr)
        return dict({a.short or a.long: bool(a.argcount) for a in opt})

    def run(self, *args, **kwargs):
        """Check command usage.

        TODO: handle long options.
        TODO: Replace, in positional args, all spaces in <foo bar>
              (transform to <foobar>)
        TODO: Convert arguments after docopt parsing from dict to tuple
              (i.e "<foobar>": "foo", "<barbaz>": "bar" should be
              ("foo", "bar")
        """
        kwargs = dict({"-{}".format(a): b for a, b in kwargs.items()})
        opts = tuple(itertools.chain(*kwargs.items())) + args
        opts = docopt.docopt(self.helpstr, opts)
        opts = [self.command] + list(itertools.chain(*opts.items()))
        if not self.is_async:
            return subprocess.check_call(*opts)
        return asyncio.create_subprocess_exec(*opts)


def stc(command):
    """Convert snake case to camelcase in class format."""
    return stringcase.pascalcase(command.replace('-', '_'))


CMDS = ('aircrack-ng', 'airodump-ng', 'aireplay-ng', 'airmon-ng', 'wesside-ng',
        'airdecap-ng', 'airdecloack-ng', 'airtun-ng', 'airbase-ng',
        'airtun-ng')


COMMANDS = {c: type(m, (ExecutorHelper,), {'command': c})
            for c, m in {command: stc(command) for command in CMDS}.items()}
