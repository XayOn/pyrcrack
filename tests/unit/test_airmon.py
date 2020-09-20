import pytest


@pytest.mark.asyncio
async def test_run_airmon():
    """Test main run method."""
    import asynctest
    from pyrcrack import AirmonNg

    async with AirmonNg() as airmong:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            with pytest.raises(AssertionError):
                await airmong.run('foo')
            await airmong.run('start')

            runmock.assert_called_with('airmon-ng',
                                       'start',
                                       stderr=-1,
                                       stdout=-1,
                                       stdin=-1)

    async with AirmonNg() as airmong:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            await airmong.run()
            runmock.assert_called_with('airmon-ng',
                                       stderr=-1,
                                       stdout=-1,
                                       stdin=-1)
