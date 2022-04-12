"""Airodump."""

import os
import asyncio
import xml
from contextlib import suppress
from .executor import ExecutorHelper

from async_timeout import timeout
import xmltodict
import dotmap

from .models import Result
from .models import AccessPoint


class AirodumpNg(ExecutorHelper):
    """Airodump-ng 1.6  - (C) 2006-2020 Thomas d'Otreppe
       https://www.aircrack-ng.org

       usage: airodump-ng <options> <interface>[,<interface>,...]

       Options:
           --ivs                 : Save only captured IVs
           --gpsd                : Use GPSd
           --write <prefix>      : Dump file prefix
           --beacons             : Record all beacons in dump file
           --update <secs>       : Display update delay in seconds
           --showack             : Prints ack/cts/rts statistics
           -h                    : Hides known stations for --showack
           -f <msecs>            : Time in ms between hopping channels
           --berlin <secs>       : Time before removing the AP/client
                                   from the screen when no more packets
                                   are received (Default: 120 seconds)
           -r  <file>            : Read packets from that file
           -T                    : While reading packets from a file,
                                   simulate the arrival rate of them
                                   as if they were "live".
           -x <msecs>            : Active Scanning Simulation
           --manufacturer        : Display manufacturer from IEEE OUI list
           --uptime              : Display AP Uptime from Beacon Timestamp
           --wps                 : Display WPS information (if any)
           --output-format <formats> : Output format. Possible values:
                                       pcap, ivs, csv, gps, kismet, netxml,
                                       logcsv
           --ignore-negative-one : Removes the message that says
                                   fixed channel <interface>: -1
           --write-interval <seconds> : Output file(s) write interval in
                                        seconds
           --background <enable> : Override background detection.
           -n <int>              : Minimum AP packets recv'd before for
                                   displaying it
           --encrypt <suite>     : Filter APs by cipher suite
           --netmask <netmask>   : Filter APs by mask
           --bssid <bssid>       : Filter APs by BSSID
           --essid <essid>       : Filter APs by ESSID
           --essid-regex <regex> : Filter APs by ESSID using a regular
                                   expression
           -a                    : Filter unassociated clients
           --ht20                : Set channel to HT20 (802.11n)
           --ht40-               : Set channel to HT40- (802.11n)
           --ht40+               : Set channel to HT40+ (802.11n)
           --channel <channels>  : Capture on specific channels
           --band <abg>          : Band on which airodump-ng should hop
           -C <frequencies>      : Uses these frequencies in MHz to hop
           --cswitch <method>    : Set channel switching method
           -s                    : same as --cswitch
           --help                : Displays this usage screen
    """
    requires_tempfile = False
    requires_tempdir = True
    requires_root = True
    command = "airodump-ng"

    async def run(self, *args, **kwargs):
        """Run async, with prefix stablished as tempdir."""
        self.execn += 1

        kwargs = {
            'background': 1,
            'write': self.tempdir.name + '/' + self.uuid,
            'write-interval': 1,
            'output-format': 'netxml,logcsv',
            **kwargs
        }

        if 'kismet' not in kwargs.get('output-format', ''):
            kwargs['output-format'] += ',netxml'

        return await super().run(*args, **kwargs)

    def get_file(self, format) -> str:
        """Return csv file, not kismet one.

        Arguments:

            format: File extension to retrieve (kismet.csv kismet.xml csv
                    log.csv or pcap)

        Returns: full filename
        """
        return f"{self.tempdir.name}/{self.uuid}-{self.execn:02}.{format}"

    @property
    async def results(self) -> list:
        """Return a list of currently detected access points

        Returns: List of AccessPoint instances
        """
        file = self.get_file('kismet.netxml')
        try:
            # Wait for a sensible 3 seconds for netxml file to be generated and
            # process to be running
            async with timeout(3):
                while not os.path.exists(file):
                    await asyncio.sleep(1)

                while not self.proc:
                    # Check if airodump is running, otherwise wait more.
                    await asyncio.sleep(1)
        except asyncio.exceptions.TimeoutError:
            # No file had been generated or process hadn't started in 3
            # seconds.
            res = "Unknown"
            if self.proc:
                res = await self.proc.communicate()
            raise Exception('\n'.join([a.decode() for a in res]))

        while self.running:
            # Avoid crashing on file creation
            with suppress(ValueError, xml.parsers.expat.ExpatError):
                xmla = xmltodict.parse(open(file).read())
                dotmap_data = dotmap.DotMap(xmla)
                results = dotmap_data['detection-run']['wireless-network']
                if results:
                    if isinstance(results, list):
                        return Result(
                            sorted([AccessPoint(ap) for ap in results],
                                   key=lambda x: x.score,
                                   reverse=True))
                    else:
                        return Result([AccessPoint(results)])
                return Result([])

            await asyncio.sleep(1)
        return Result([])
