"""Test specific airodump functions."""
import pytest


def test_props():
    """Props."""
    from pyrcrack import AirodumpNg
    assert AirodumpNg.requires_tempdir
    assert not AirodumpNg.requires_tempfile
    assert AirodumpNg.command == "airodump-ng"


@pytest.mark.asyncio
async def test_run_airodump():
    """Test main run method."""
    import asynctest
    from pyrcrack import AirodumpNg

    async with AirodumpNg() as airodump:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            airodump.result_updater = asynctest.mock.CoroutineMock()
            await airodump.run()
            assert runmock.called
            runmock.assert_called_with('airodump-ng',
                                       '--background',
                                       '1',
                                       '--write',
                                       airodump.tempdir.name + "/" +
                                       airodump.uuid,
                                       '--write-interval',
                                       '1',
                                       stderr=-1,
                                       stdout=-1,
                                       stdin=-1)


@pytest.mark.asyncio
async def test_run_airodump_with_write():
    """Test main run method."""
    import asynctest
    from pyrcrack import AirodumpNg

    async with AirodumpNg() as airodump:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            await airodump.run(write='foo')
            runmock.assert_called_with('airodump-ng',
                                       '--write',
                                       'foo',
                                       '--background',
                                       '1',
                                       '--write-interval',
                                       '1',
                                       stderr=-1,
                                       stdout=-1,
                                       stdin=-1)

    async with AirodumpNg() as airodump:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            await airodump.run(w='foo')
            runmock.assert_called_with('airodump-ng',
                                       '-w',
                                       'foo',
                                       '--background',
                                       '1',
                                       '--write-interval',
                                       '1',
                                       stderr=-1,
                                       stdout=-1,
                                       stdin=-1)


@pytest.mark.asyncio
async def test_csv():
    """Test main run method."""
    from pyrcrack import AirodumpNg

    async with AirodumpNg() as airodump:
        expected = (f"{airodump.tempdir.name}/{airodump.uuid}"
                    f"-{airodump.execn:02}.kismet.csv")
        assert airodump.get_file('kismet.csv') == expected
