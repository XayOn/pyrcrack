"""Set monitor."""
import asyncio

import pyrcrack


async def set_monitor():
    """Scan for targets, return json."""
    async with pyrcrack.AirmonNg() as airmon:
        interfaces = await airmon.list_wifis()
        print(interfaces)
        interface = await airmon.set_monitor(interfaces[0]['interface'])
        print(interface[0])


asyncio.run(set_monitor())
