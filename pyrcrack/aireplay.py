"""Aireplay-ng"""
import asyncio

from .executor import ExecutorHelper
from .models import AireplayResults


class AireplayNg(ExecutorHelper):
    """ Aireplay-ng 1.6  - (C) 2006-2020 Thomas d'Otreppe
    https://www.aircrack-ng.org

    Usage: aireplay-ng <options> <replay interface>

    Options:

        -b bssid  : MAC address, Access Point
        -d dmac   : MAC address, Destination
        -s smac   : MAC address, Source
        -m len    : minimum packet length
        -n len    : maximum packet length
        -u type   : frame control, type    field
        -v subt   : frame control, subtype field
        -t tods   : frame control, To      DS bit
        -f fromds : frame control, From    DS bit
        -w iswep  : frame control, WEP     bit
        -D        : disable AP detection
        -x nbpps  : number of packets per second
        -p fctrl  : set frame control word (hex)
        -a bssid  : set Access Point MAC address
        -c dmac   : set Destination  MAC address
        -h smac   : set Source       MAC address
        -g value  : change ring buffer size (default: 8)
        -F        : choose first matching packet
        -e essid  : set target AP SSID
        -o npckts : number of packets per burst (0=auto, default: 1)
        -q sec    : seconds between keep-alives
        -Q        : send reassociation requests
        -y prga   : keystream for shared key auth
        -T n      : exit after retry fake auth request n time
        -j        : inject FromDS packets
        -k IP     : set destination IP in fragments
        -l IP     : set source IP in fragments
        -B        : activates the bitrate test
        -i iface  : capture packets from this interface
        -r file   : extract packets from this pcap file
        -R                    : disable /dev/rtc usage
        --ignore-negative-one  : if the interface's channel can't be determined
        --deauth-rc <rc>      : Deauthentication reason code [0-254]
        --deauth <count>    : deauthenticate 1 or all stations (-0)
        --fakeauth <delay>  : fake authentication with AP (-1)
        --interactive       : interactive frame selection (-2)
        --arpreplay         : standard ARP-request replay (-3)
        --chopchop          : decrypt/chopchop WEP packet (-4)
        --fragment          : generates valid keystream   (-5)
        --caffe-latte       : query a client for new IVs  (-6)
        --cfrag             : fragments against a client  (-7)
        --migmode           : attacks WPA migration mode  (-8)
        --test              : tests injection and quality (-9)
        --help              : Displays this usage screen
    """

    command = 'aireplay-ng'
    requires_tempfile = False
    requires_tempdir = False
    requires_root = True

    async def run(self, *args, **kwargs):
        """Run async, with prefix stablished as tempdir."""
        asyncio.create_task(self.result_updater())
        return await super().run(*args, **kwargs)

    @property
    async def results(self):
        return self.meta.get('result', AireplayResults(''))

    async def result_updater(self):
        """Set result on local object."""
        # TODO: There might be a situation here where proc is never != None.
        # This should have some timeout logic as airodump has
        while not self.proc:
            await asyncio.sleep(1)

        while self.proc.returncode is None:
            self.meta['result'] = await self.get_results()
            await asyncio.sleep(2)

    async def get_results(self):
        """Get results list."""
        if not self.proc:
            return AireplayResults('')
        return AireplayResults((await self.proc.communicate())[0].decode())
