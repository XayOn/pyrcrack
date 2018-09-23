"""Scan for targets and return a JSON with aps and clients."""
import pyrcrack
import sys
import asyncio


async def scan_for_targets():
    """Scan for targets, return json."""

    async with pyrcrack.AirodumpNg() as pdump:
        await pdump.run(sys.argv[1], write_interval=1)
        while True:
            await asyncio.sleep(1)
            print(pdump.meta)


asyncio.run(scan_for_targets())
