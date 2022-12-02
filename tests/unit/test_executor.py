"""Test executor class."""

import pytest


def test_helpstr_extraction():
    """Test helpstr extraction.

    This tests helpstr(), wich should try to execute a command, and echo
    to ensure output 0.
    """
    from unittest.mock import patch

    with patch("subprocess.check_output", side_effect=(b"test",)) as mock:
        from pyrcrack.executor import ExecutorHelper

        class FakeExecutor(ExecutorHelper):
            command = "foobar"
            requires_tempfile = False
            requires_tempdir = False
            requires_root = False

        assert FakeExecutor().helpstr == "test"
        mock.assert_called_with("foobar 2>&1; echo", shell=True)


def test_usage():
    """Test extract usage from a specified command."""
    # opt = docopt.parse_defaults(self.helpstr)
    # return dict({a.short or a.long: bool(a.argcount) for a in opt})
    from unittest.mock import patch

    with patch("subprocess.check_output", side_effect=(b"test",)):
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
            requires_root = False

        assert FakeExecutor().usage == {"-f": False, "-y": True}


@pytest.mark.asyncio
async def test_run_async():
    """Check command usage."""
    import asynctest

    with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
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
            requires_root = False

        await FakeExecutor().run(f="foo", y=True)

        try:
            runmock.assert_called_with(
                *["foobar", "-f", "foo", "-y"], stderr=-1, stdin=-1, stdout=-1
            )
        except AssertionError:
            runmock.assert_called_with(
                *["foobar", "-y", "-f", "foo"], stderr=-1, stdin=-1, stdout=-1
            )


@pytest.mark.parametrize(
    "in_,out", (("aircrack-ng", "AircrackNg"), ("airodump-ng", "AirodumpNg"))
)
def test_stc(in_, out):
    """Convert snake case to camelcase in class format."""
    from pyrcrack.executor import stc

    assert stc(in_) == out
