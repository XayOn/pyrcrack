"""pyrcrack.

Aircrack-NG python bindings
"""
import asyncio
import subprocess

from .aircrack import AircrackNg  # noqa
from .airdecap import AirdecapNg  # noqa
from .aireplay import AireplayNg  # noqa
from .airmon import AirmonNg  # noqa
from .airbase import AirbaseNg  # noqa
from .airdecloack import AirdecloackNg  # noqa
from .airodump import AirodumpNg  # noqa


def check():
    """Check if aircrack-ng is compatible."""
    assert '1.6' in subprocess.check_output(['aircrack-ng', '-v'])


class Pyrcrack:
    """High level aircrack-ng interface.
    
    Arguments: 

        list_waiting_time: Time (in seconds) to wait for a network scan
    """
    def __init__(self, list_waiting_time):
        """Set up pyrcrack instance."""
        self.iface = None
        self.list_waiting_time = list_waiting_time

    @property
    async def interfaces(self):
        """List of currently available interfaces as reported by airmon-ng

        This is an awaitable property, use it as in::

            await Pyrcrack().interfaces

        Returns: None
        """
        return [a['interface'] for a in await airmon.list_wifis()]

    async def set_interface(self, interface):
        """Select an interface, set it on monitor mode

        Will set `iface` property.
        """
        assert interface in await self.interfaces
        async with AirmonNg() as airmon:
            interface = await airmon.set_monitor(interface)
            self.iface = interface[0]

    @property
    async def access_points(self) -> list:
        """Return a list of access points by scanning with airodump-ng

        This is a basic, hihg-level scan, on all channels without extra
        options, for more custom searches uses directly the AirodumpNg async
        context manager.

        Returns: List of `AccessPoint` instances
        """
        async with AirodumpNg() as pdump:
            await pdump.run(self.iface, write_interval=1)
            await asyncio.sleep(self.list_waiting_time)
            return pdump.sorted_aps()
