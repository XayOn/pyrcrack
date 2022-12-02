import pytest


@pytest.mark.asyncio
async def test_run_airmon():
    """Test main run method."""
    import asynctest

    from pyrcrack import AirmonNg

    with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
        with pytest.raises(Exception):
            await AirmonNg().run("foo")
        await AirmonNg().run("start")

        runmock.assert_called_with(
            "airmon-ng", "start", stderr=-1, stdout=-1, stdin=-1)

    with asynctest.mock.patch("asyncio.create_subprocess_exec") as runmock:
        await AirmonNg().run()
        runmock.assert_called_with("airmon-ng", stderr=-1, stdout=-1, stdin=-1)


def test_run_model():
    from pyrcrack.models import Interfaces

    data = [
        b"Found 6 processes that could cause trouble.",
        b"Kill them using 'airmon-ng check kill' before putting",
        b"the card in monitor mode, they will interfere by changing channels",
        b"and sometimes putting the interface back in managed mode",
        b"  PID Name",
        b"  239 avahi-daemon",
        b"  241 wpa_supplicant",
        b"  243 avahi-daemon",
        b"  356 wpa_supplicant",
        b"  381 wpa_supplicant",
        b"  481 dhcpcd",
        b"PHY\tInterface\tDriver\t\tChipset",
        b"phy0\twlan0\t\tbrcmfmac\tBroadcom 43430",
        (
            b"\t\t(mac80211 monitor mode vif enabled for [phy0]wlan0"
            b" on [phy0]wlan0mon)"
        ),
        b"\t\t(mac80211 station mode vif disabled for [phy0]wlan0)",
        b"phy1\twlxe84e066b5386\tmt7601u\t\tRalink Technology, Corp. MT7601U",
    ]
    assert [a.__dict__ for a in Interfaces(data)] == [
        {
            "data": {
                "phy": "phy0",
                "interface": "wlan0",
                "driver": "brcmfmac",
                "chipset": "Broadcom 43430",
                "monitor": {
                    "driver": "mac80211",
                    "interface": "wlan0mon",
                    "mode": "monitor",
                    "original_interface": "wlan0",
                    "status": "enabled",
                },
            }
        },
        {
            "data": {
                "phy": "phy1",
                "interface": "wlxe84e066b5386",
                "driver": "mt7601u",
                "chipset": "Ralink Technology, Corp. MT7601U",
            }
        },
    ]

    data = b"""Found 7 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    677 wpa_supplicant
   2209 dhcpcd
   2210 dhcpcd
   2211 dhcpcd
 107797 dhcpcd
 107805 dhcpcd
 107853 dhcpcd

PHY	Interface	Driver		Chipset

phy0	wlp3s0		iwlwifi		Intel Corporation Wireless 7260 (rev 83)

\t\t(mac80211 monitor mode vif enabled for [phy0]wlp3s0 on [phy0]wlp3s0mon)
\t\t(mac80211 station mode vif disabled for [phy0]wlp3s0)
""".split(
        b"\n"
    )

    assert [a.__dict__ for a in Interfaces(data)] == [
        {
            "data": {
                "phy": "phy0",
                "interface": "wlp3s0",
                "driver": "iwlwifi",
                "chipset": "Intel Corporation Wireless 7260 (rev 83)",
                "monitor": {
                    "driver": "mac80211",
                    "interface": "wlp3s0mon",
                    "mode": "monitor",
                    "original_interface": "wlp3s0",
                    "status": "enabled",
                },
            }
        }
    ]
