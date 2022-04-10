"""Scan for a specific ap and pretty print some data."""
import sys
import subprocess
import asyncio

import pyrcrack


async def scan_for_targets_on_bssid():
    """Scan for targets, return json."""

    async with pyrcrack.AirodumpNg() as pdump:
        await pdump.run(sys.argv[1], essid=sys.argv[2], write_interval=1)
        while True:
            await asyncio.sleep(1)
            subprocess.check_call('clear')
            for apo in pdump.meta['result']['aps']:
                print(f'{apo.essid} ({apo.bssid}) C: {len(apo.clients)})')


asyncio.run(scan_for_targets_on_bssid())
