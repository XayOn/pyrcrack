"""Scan for targets and and pretty print some data."""
import asyncio

import pyrcrack

from rich.console import Console
from rich.prompt import Prompt


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    pyrc = pyrcrack.Pyrcrack()
    interface = Prompt.ask('Select an interface',
                           choices=await pyrc.interfaces)

    await pyrc.set_interface(interface)
    aps = await pyrc.access_points
    console.print(aps.table)


asyncio.run(scan_for_targets())
