"""Test specific aireplay functions."""
import pytest


def test_aireplay_props():
    """Props."""
    from pyrcrack import AireplayNg

    assert not AireplayNg.requires_tempdir
    assert not AireplayNg.requires_tempfile
    assert AireplayNg.command == "aireplay-ng"


@pytest.mark.asyncio
async def test_run_aireplay():
    """Test main run method."""
    import asynctest

    from pyrcrack import AireplayNg

    async with AireplayNg() as aireplay:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            aireplay.result_updater = asynctest.mock.CoroutineMock()
            await aireplay.run()
            assert runmock.called
            runmock.assert_called_with(
                "aireplay-ng", stderr=-1, stdout=-1, stdin=-1)
