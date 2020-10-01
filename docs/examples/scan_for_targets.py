"""Scan for targets and and pretty print some data."""
import asyncio
import subprocess
import sys

import pyrcrack

from rich.console import Console


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    async with pyrcrack.AirodumpNg() as pdump:
        async for result in pdump(sys.argv[1]): 
            # Current running process will be stored in self.proc
            # Be careful, the process will only start when you iter trough results.
            # a simple await anext(pdump(...)) would do if you don't really
            # want to gather results.
            console.clear()
            console.print(result.table)
            await asyncio.sleep(2)

asyncio.run(scan_for_targets())
