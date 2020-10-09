"""Scan for targets and and pretty print some data."""
import asyncio
from asyncio import TimeoutError
from async_timeout import timeout

import pyrcrack

from rich.console import Console
from rich.prompt import Prompt

import logging
logging.basicConfig(level=logging.DEBUG)


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    airmon = pyrcrack.AirmonNg()
    interfaces = await airmon.interfaces
    console.print(interfaces.table)
    interface = Prompt.ask('Select an interface',
                           choices=[a.interface for a in interfaces])

    async with airmon(interface) as mon:
        async with pyrcrack.AirodumpNg() as pdump:
            # TODO: Maybe copy this object upon __call__ so we can do, paralell
            # async for result in pdump(foo) (the only relevant part would be
            # execn properties) within the same temporary path?
            async for aps in pdump(mon.monitor_interface):
                console.clear()
                console.print(aps.table)
                client = Prompt.ask(
                    'Select an AP',
                    choices=['continue', *[str(a) for a in range(len(aps))]])

                if client != 'continue':
                    break

        async with pyrcrack.AirodumpNg() as pdump:
            console.print(
                ":vampire:",
                f"Selected client: [red] {aps[int(client)].bssid} [/red]")

            async for result in pdump(mon.monitor_interface,
                                      **aps[int(client)].airodump):
                console.clear()
                console.print(result.table)
                await asyncio.sleep(3)


asyncio.run(scan_for_targets())
