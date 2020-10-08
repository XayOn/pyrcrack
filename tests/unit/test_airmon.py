import pytest


@pytest.mark.asyncio
async def test_run_airmon():
    """Test main run method."""
    import asynctest
    from pyrcrack import AirmonNg

    with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
        with pytest.raises(AssertionError):
            await AirmonNg().run('foo')
        await AirmonNg().run('start')

        runmock.assert_called_with('airmon-ng',
                                   'start',
                                   stderr=-1,
                                   stdout=-1,
                                   stdin=-1)

    with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
        await AirmonNg().run()
        runmock.assert_called_with('airmon-ng',
                                   stderr=-1,
                                   stdout=-1,
                                   stdin=-1)
