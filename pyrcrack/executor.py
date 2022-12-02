"""Pyrcrack-ng Executor helper."""
import asyncio
import functools
import itertools
import logging
import os
import subprocess
import tempfile
import uuid
import warnings
from contextlib import suppress
from contextvars import ContextVar

import docopt
import stringcase

logging.basicConfig(level=logging.INFO)


class Option:
    """Represents a single option (e.g, -e)."""

    def __init__(self, usage, word=None, value=None, logger=None):
        """Set option parameters."""
        self.usage = usage
        self.word = word
        self.logger = logger
        self.value = value
        keys = usage.keys()
        self.is_short = Option.short(word) in keys
        self.is_long = Option.long(word) in keys
        self.expects_args = bool(usage[self.formatted])
        self.logger.debug("Parsing option %s:%s", self.word, self.value)

    @property
    @functools.lru_cache  # noqa: B019
    def formatted(self):
        """Format given option acording to definition."""
        result = Option.short(self.word) if self.is_short else Option.long(
            self.word)

        if self.usage.get(result):
            return result

        sword = self.word.replace("_", "-")
        return Option.short(sword) if self.is_short else Option.long(sword)

    @staticmethod
    def long(word):
        """Extract long format option."""
        return "--{}".format(word)

    @staticmethod
    def short(word):
        """Extract short format option."""
        return "-{}".format(word)

    @property
    def parsed(self):
        """Returns key, value if value is required."""
        if self.expects_args:
            return (self.formatted, str(self.value))
        return (self.formatted, )

    def __repr__(self):
        return f"Option(<{self.parsed}>, {self.is_short}, {self.expects_args})"


def check():
    """Check if aircrack-ng is compatible."""
    ver_check = subprocess.check_output(["aircrack-ng", "--help"])
    if b"Aircrack-ng 1.6" not in ver_check:
        if b"Aircrack-ng 1.7" not in ver_check:
            raise Exception("Unsupported Aircrack-ng detected")
        else:
            warnings.warn(
                "Aircrack-ng 1.7 detected, some features may not work")


class ExecutorHelper:
    """Abstract class interface to a shell command."""

    requires_tempfile = False
    requires_tempdir = False
    requires_root = True
    command = ""

    def __init__(self):
        """Set docstring."""
        if not self.__doc__:
            self.__doc__ = self.helpstr
        self.uuid = uuid.uuid4().hex
        self.called = False
        self.execn = 0
        self.logger = logging.getLogger(self.__class__.__name__)
        self.proc = None
        self.meta = {}
        self.debug = os.getenv("PYRCRACK_DEBUG", "") == 1
        self.tempfile = None
        self.tempdir = None
        if self.requires_tempfile:
            self.tempfile = tempfile.NamedTemporaryFile()
        elif self.requires_tempdir:
            self.tempdir = tempfile.TemporaryDirectory()
        if self.requires_root and not os.getenv("SKIP_ROOT_CHECK"):
            if os.geteuid() != 0:
                raise Exception("Must be run as root")
        if not os.getenv("SKIP_VERSION_CHECK"):
            check()

    @property
    @functools.lru_cache  # noqa: B019
    def helpstr(self):
        """Extract help string for current command."""
        helpcmd = "{} 2>&1; echo".format(self.command)
        return subprocess.check_output(helpcmd, shell=True).decode()

    @property
    @functools.lru_cache  # noqa: B019
    def usage(self):
        """Extract usage from a specified command.

        This is useful if usage not defined in subclass, but it is
        recommended to define them there.
        """
        opt = docopt.parse_defaults(self.__doc__)
        return dict({a.short or a.long: bool(a.argcount) for a in opt})

    def _run(self, *args, **kwargs):
        """Check command usage and execute it.

        If self.sync is defined, it will return process call output,
        and launch it blockingly.

        Otherwise it will call asyncio.create_subprocess_exec()
        """
        if not self.command:
            raise Exception("Subclassing error, please specify a base cmd")

        self.logger.debug("Parsing options: %s", kwargs)
        options = [
            Option(self.usage, a, v, self.logger) for a, v in kwargs.items()
        ]
        self.logger.debug("Got options: %s", options)

        opts = ([self.command] + list(args) +
                list(itertools.chain(*(o.parsed for o in options))))

        self.logger.debug("Running command: %s", opts)
        return opts

    @staticmethod
    def resolve(val):
        """Force string conversion.

        - In case an Interface object comes on args
        - In case a contextvar comes, retrieve its value
        """
        # I'm a little conflicted on this one, as it seems dirty to cast
        # everything to string
        # Yet, I'm letting it go like this because in the end, this is a
        # subprocess call that requires all args to be strings or bytes...
        # This will also allow us to use an AP object in a future.
        if isinstance(val, ContextVar):
            return str(val.get())
        return str(val)

    async def run(self, *args, **kwargs):
        """Run asynchronously."""
        opts = self._run(*args, **kwargs)
        self.proc = await asyncio.create_subprocess_exec(
            *[self.resolve(a) for a in opts],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return self.proc

    def __call__(self, *args, **kwargs):
        self.run_args = args, kwargs
        return self

    def __aiter__(self):
        """Defines us as an async iterator."""
        return self

    async def __anext__(self):
        """Get the next result batch."""
        if not self.called:
            self.called = True
            self.proc = await self.run(*self.run_args[0], **self.run_args[1])

        current_results = await self.results

        if not self.running:
            # If we haven't sent the latests results, send them now.
            if self.last_results != current_results:
                self.last_results = current_results
                return current_results
            raise StopAsyncIteration

        self.last_results = current_results
        return self.last_results

    @property
    def running(self):
        if not self.proc:
            return False
        return self.proc.returncode is None

    async def readlines(self):
        """Return lines as per proc.communicate, non-empty ones."""
        if not self.proc:
            return []
        com = await self.proc.communicate()
        return [a for a in com[0].split(b"\n") if a]

    @property
    async def results(self):
        return [self.proc]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up conext manager."""
        if self.debug and (self.requires_tempfile or self.requires_tempdir):
            self.logger.error(f"Not deleting {self.tempfile}, {self.tempdir}")

        if self.tempfile:
            self.tempfile.__exit__(exc_type, exc_val, exc_tb)

        if self.tempdir:
            self.tempdir.__exit__(exc_type, exc_val, exc_tb)

        if exc_type in (ProcessLookupError, subprocess.CalledProcessError):
            return True

        if self.proc:
            with suppress(Exception):
                self.proc.kill()

    async def __aenter__(self):
        """Create temporary directories and files if required."""
        if self.requires_tempfile and self.tempfile:
            self.tempfile.__enter__()
        elif self.requires_tempdir and self.tempdir:
            self.tempdir.__enter__()
        return self


def stc(command):
    """Convert snake case to camelcase in class format."""
    return stringcase.pascalcase(command.replace("-", "_"))
