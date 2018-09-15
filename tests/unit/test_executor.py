"""Test executor class."""

import pytest


def test_helpstr_extraction():
    """Test helpstr extraction.

    This tests helpstr(), wich should try to execute a command,
    and echo to ensure output 0.
    """
    from unittest.mock import patch
    with patch("subprocess.check_output", side_effect=(b'test', )) as mock:
        from pyrcrack.executor import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            command = "foobar"
            requires_tempfile = False
            requires_tempdir = False

        assert FakeExecutor().helpstr == 'test'
        mock.assert_called_with("foobar 2>&1; echo", shell=True)


def test_usage():
    """Test extract usage from a specified command."""
    # opt = docopt.parse_defaults(self.helpstr)
    # return dict({a.short or a.long: bool(a.argcount) for a in opt})
    from unittest.mock import patch
    with patch("subprocess.check_output", side_effect=(b'test', )):
        from pyrcrack.executor import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake command.
            Usage: fake [options]

            Options:
                -f
                -y=<foo>
            """

            command = "foobar"
            requires_tempfile = False
            requires_tempdir = False

        assert FakeExecutor().usage == {'-f': False, '-y': True}


def test_run():
    """Check command usage."""
    from unittest.mock import patch
    from pyrcrack.executor import ExecutorHelper

    class FakeExecutor(ExecutorHelper):
        """Fake command
        Usage: Fake [options]

        Options:
            -f
            -y=<foo>
        """

        command = "foobar"
        requires_tempfile = False
        requires_tempdir = False

    with patch("subprocess.check_output", side_effect=(b'test', )) as mock:
        assert FakeExecutor().run_sync(f=True, y="foo") == b'test'
        try:
            mock.assert_called_with(['foobar', '-f', '-y', 'foo'])
        except AssertionError:
            mock.assert_called_with(['foobar', '-y', 'foo', '-f'])

    import subprocess
    with patch(
            "subprocess.check_output",
            side_effect=(subprocess.CalledProcessError(1, "", b"error"), )):
        assert FakeExecutor().run_sync(f=True, y="foo") == b'error'


async def test_run_async():
    """Check command usage."""
    from unittest.mock import patch
    with patch(
            "asyncio.create_subprocess_exec", side_effect=(b'test', )) as mock:
        from pyrcrack.executor import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake command.
            Usage: fake [options]

            Options:
                -f=<bar>
                -y
            """

            command = "foobar"
            requires_tempfile = False
            requires_tempdir = False

        assert (await FakeExecutor().run_async(y=True, f="foo")) == b'test'
        try:
            mock.assert_called_with(['foobar', '-f', 'foo', '-y'])
        except AssertionError:
            mock.assert_called_with(['foobar', '-y', '-f', "foo"])


@pytest.mark.parametrize('in_,out', (('aircrack-ng', 'AircrackNg'),
                                     ('airodump-ng', 'AirodumpNg')))
def test_stc(in_, out):
    """Convert snake case to camelcase in class format."""
    from pyrcrack.executor import stc
    assert stc(in_) == out
