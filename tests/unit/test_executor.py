"""Test executor class."""

import pytest


def test_helpstr_extraction():
    """Test helpstr extraction.

    This tests helpstr(), wich should try to execute a command,
    and echo to ensure output 0.
    """
    from unittest.mock import patch
    with patch("subprocess.check_output", side_effect=(b'test',)) as mock:
        from pyrcrack import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake executor class."""
            command = "foobar"
            is_async = False

        assert FakeExecutor().helpstr == 'test'
        mock.assert_called_with("foobar 2>&1; echo", shell=True)


def test_usage():
    """Test extract usage from a specified command."""
    # opt = docopt.parse_defaults(self.helpstr)
    # return dict({a.short or a.long: bool(a.argcount) for a in opt})
    from unittest.mock import patch
    with patch("subprocess.check_output", side_effect=(b'test',)):
        from pyrcrack import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake executor class."""
            command = "foobar"
            is_async = False
            helpstr = """fake
            Usage: fake [options]

            Options:
                -f
                -y=<foo>
            """

        assert FakeExecutor().usage == {'-f': False, '-y': True}


def test_run():
    """Check command usage."""
    from unittest.mock import patch
    # opts = docopt.docopt(
    #     self.helpstr, args + list(itertools.chain(*kwargs.items())))

    # if not self.is_async:
    #     return subprocess.check_call(opts)
    # return asyncio.create_subprocess_exec(opts)
    with patch("subprocess.check_call", side_effect=(b'test',)) as mock:
        from pyrcrack import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake executor class."""
            command = "foobar"
            is_async = False
            helpstr = """fake
            Usage: fake [options]

            Options:
                -f=<bar>
                -y=<foo>
            """

        assert FakeExecutor().run(f=True, y="foo") == b'test'
        try:
            mock.assert_called_with('foobar', '-f', True, '-y', 'foo')
        except AssertionError:
            mock.assert_called_with('foobar', '-y', 'foo', '-f', True)


def test_run_async():
    """Check command usage."""
    from unittest.mock import patch
    with patch("asyncio.create_subprocess_exec",
               side_effect=(b'test',)) as mock:
        from pyrcrack import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            """Fake executor class."""
            command = "foobar"
            is_async = True
            helpstr = """fake
            Usage: fake [options]

            Options:
                -f=<bar>
                -y=<foo>
            """

        assert FakeExecutor().run(f=True, y="foo") == b'test'
        try:
            mock.assert_called_with('foobar', '-f', True, '-y', 'foo')
        except AssertionError:
            mock.assert_called_with('foobar', '-y', 'foo', '-f', True)


@pytest.mark.parametrize('in_,out', (('aircrack-ng', 'AircrackNg'),
                                     ('airodump-ng', 'AirodumpNg')))
def test_stc(in_, out):
    """Convert snake case to camelcase in class format."""
    from pyrcrack import stc
    assert stc(in_) == out
