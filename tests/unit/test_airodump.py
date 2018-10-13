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
            runmock.assert_called_with(
                'airodump-ng',
                '--write',
                airodump.tempdir.name + "/" + airodump.uuid,
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
            runmock.assert_called_with(
                'airodump-ng',
                '--write',
                'foo',
                stderr=-1,
                stdout=-1,
                stdin=-1)

    async with AirodumpNg() as airodump:
        with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
            await airodump.run(w='foo')
            runmock.assert_called_with(
                'airodump-ng', '-w', 'foo', stderr=-1, stdout=-1, stdin=-1)


@pytest.mark.asyncio
async def test_csv():
    """Test main run method."""
    from pyrcrack import AirodumpNg
    import tempfile

    async with AirodumpNg() as airodump:
        assert not airodump.csv_file
        dir_ = airodump.tempdir.name + "/"
        with tempfile.NamedTemporaryFile(
                dir=dir_, prefix=airodump.uuid + "-", suffix='.csv') as named:
            named.write(b'')
            print(named.name)
            assert airodump.csv_file


@pytest.mark.asyncio
async def test_sorted_aps():
    """Test sorted aps property."""
    from pyrcrack import AirodumpNg

    class FakeAp:
        """Fake ap."""

        def __init__(self, score):
            self.score = score

    fakeaps = [FakeAp(0), FakeAp(1)]
    sortedaps = [fakeaps[1], fakeaps[0]]

    async with AirodumpNg() as airodump:
        airodump.meta = {'result': {'aps': fakeaps}}
        assert airodump.sorted_aps() == sortedaps


@pytest.mark.asyncio
async def test_results():
    """Test results."""
    import tempfile
    from pyrcrack import AirodumpNg

    async with AirodumpNg() as airodump:
        assert airodump.get_results() == {"aps": [], "clients": []}
        dir_ = airodump.tempdir.name + "/"
        with tempfile.NamedTemporaryFile(
                dir=dir_, prefix=airodump.uuid + "-", suffix=".csv") as named:
            data = (
                ('speed', 'A'),
                ('channel', '2'),
                ('first_time_seen', 'None'),
                ('beacons', '10'),
                ('lan_ip', '0.0.0.0'),
                ('essid', 'FOO'),
                ('last_time_seen', 'None'),
                ('privacy', 'None'),
                ('key', 'None'),
                ('iv', '10'),
                ('cipher', 'WPA'),
                ('authentication', 'PSK'),
                ('power', '10'),
                ('bssid', '00:0a:0b:0c:0d'),
                ('id_length', '1'),
            )
            app = b','.join([a[1].encode() for a in data]) + b'\n'
            sep = (b'Station MAC, First time seen, Last time seen,'
                   b' Power, # packets, BSSID, Probed ESSIDs\n')
            cli = (b'00:0a:0b:0c:0d, None, None, '
                   b'-80, 10, 00:0a:0b:0c:0d, asdf\n')
            named.write(b','.join([a[0].encode() for a in data]) + b'\n')
            named.write(app)
            named.write(sep)
            named.write(cli)
            named.seek(0)

            res = airodump.get_results()
            app = res['aps'][0].__dict__
            clients = app.pop('clients')
            assert clients[0].__dict__ == {
                "first_time_seen": "None",
                "power": "-80",
                "bssid": "00:0a:0b:0c:0d",
                "station_mac": "00:0a:0b:0c:0d",
                "last_time_seen": "None",
                "packets": "10",
                "probed_essids": "asdf"
            }
            assert res['clients'][0].__dict__ == {
                "first_time_seen": "None",
                "power": "-80",
                "bssid": "00:0a:0b:0c:0d",
                "station_mac": "00:0a:0b:0c:0d",
                "last_time_seen": "None",
                "packets": "10",
                "probed_essids": "asdf"
            }
