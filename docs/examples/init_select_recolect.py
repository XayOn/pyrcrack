"""Scan for targets and and pretty print some data."""
import asyncio

from pyrcrack import AirmonNg, AirodumpNg, MONITOR

from rich.console import Console
from rich.prompt import Prompt

import logging
logging.basicConfig(level=logging.DEBUG)


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    airmon = AirmonNg()
    interfaces = await airmon.interfaces
    console.print(interfaces.table)
    interface = Prompt.ask('Select an interface',
                           choices=[str(a) for a in interfaces])
    client = None
    ap_ = None

    async with airmon(interface):
        async with AirodumpNg() as pdump:
            async for aps in pdump(MONITOR):
                console.clear()
                console.print(aps.table)
                client = Prompt.ask(
                    'Select an AP',
                    choices=['continue', *[str(a) for a in range(len(aps))]])
                if client != 'continue':
                    ap_ = aps[int(client)]
                    break

        if not ap_:
            return

        async with AirodumpNg() as pdump:
            console.print(
                ":vampire:",
                f"Selected client: [red] {ap_.bssid} [/red]")

            async for result in pdump(MONITOR, **ap_.airodump):
                console.clear()
                console.print(result.table)
                await asyncio.sleep(3)


asyncio.run(scan_for_targets())
