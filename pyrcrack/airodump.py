"""Airodump."""

import os
from glob import glob
import asyncio
import csv
import io
import xml
from contextlib import suppress
from .executor import ExecutorHelper

from async_timeout import timeout
import xmltodict
import dotmap

from .models import Result
from .models import Client
from .models import AccessPoint

DICTS = ('WLAN_', 'JAZZTEL_', 'MOVISTAR_')


class AirodumpNg(ExecutorHelper):
    """Airodump-ng 1.6  - (C) 2006-2020 Thomas d'Otreppe
       https://www.aircrack-ng.org

       usage: airodump-ng <options> <interface>[,<interface>,...]

       Options:
           --ivs                 : Save only captured IVs
           --gpsd                : Use GPSd
           --write <prefix>      : Dump file prefix
           -w                    : same as --write
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
           --write-interval <seconds> : Output file(s) write interval in seconds
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
    command = "airodump-ng"

    def __init__(self, *args, **kwargs):
        self.called = False
        self.proc = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.run_args = args, kwargs
        return self

    def __aiter__(self):
        """Defines us as an async iterator."""
        return self

    async def __anext__(self):
        """Get the next result batch."""
        if not self.called:
            self.called = True
            self.proc = await self.run(*self.run_args[0], **self.run_args[1])

        if not self.running:
            raise StopAsyncIteration

        return await self.results

    async def run(self, *args, **kwargs):
        """Run async, with prefix stablished as tempdir."""
        self.execn += 1
        kwargs['background'] = 1
        if not ('write' in kwargs or 'w' in kwargs):
            kwargs.pop('w', None)
            kwargs['write'] = self.tempdir.name + "/" + self.uuid
        if not 'write_interval' in kwargs:
            kwargs['write_interval'] = 1

        # Ensure kismet xml is going to be written
        if kwargs.get('write-format', None) is not None:
            kwargs['write-format'] = 'kismet,csv,logcsv'
        elif kwargs.get('write-format') and 'kismet' not in kwargs.get(
                'write-format', ''):
            kwargs['write-format'] += ',kismet'

        return await super().run(*args, **kwargs)

    @property
    def running(self):
        return self.proc.returncode is None

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
            async with timeout(3):
                while not os.path.exists(file):
                    await asyncio.sleep(1)

                while not self.proc:
                    await asyncio.sleep(1)
        except asyncio.exceptions.TimeoutError:
            raise Exception(await self.proc.communicate())

        while self.running:
            # Update results each second.
            with suppress(ValueError, xml.parsers.expat.ExpatError):
                xmla = xmltodict.parse(open(file).read())
                dotmap_data = dotmap.DotMap(xmla)
                results = dotmap_data['detection-run']['wireless-network']
                if results:
                    return Result(
                        sorted([AccessPoint(ap) for ap in results],
                               key=lambda x: x.score,
                               reverse=True))
                return []

            await asyncio.sleep(1)
