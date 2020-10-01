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
from rich.table import Table
import xmltodict
import dotmap

DICTS = ('WLAN_', 'JAZZTEL_', 'MOVISTAR_')

class Result(list):
    @property
    def table(self):
        """Return a nicely formatted table with results."""
        table = Table(show_header=True,
                      header_style='bold magenta',
                      show_footer=False)
        table.add_column('Name')
        table.add_column('Bssid')
        table.add_column('Power')
        table.add_column('Captured packets')
        table.add_column('Score')
        for wireless in self: 
            table.add_row(wireless.essid, wireless.bssid, str(wireless.dbm),
                          str(wireless.packets.total), str(wireless.score))
        return table



class Client:
    def __init__(self, data):
        self.data = data

    @property
    def bssid(self):
        return self.data['client-mac']

    @property
    def packets(self):
        return self.data.packets.total

    @property
    def dbm(self):
        return self.data['snr-info'].last_signal_dbm


class AccessPoint:
    """Represents an access point.
    
    Stores internal data in "data" property
    """
    def __init__(self, data):
        """Initialize an access point

        Arguments:

            data: Dot data structure from kismet xml file.
        """
        self.data = data

    def __repr__(self):
        return f"{self.essid} - ({self.bssid})"

    @property
    def clients(self):
        """List of connected clients.

        Returns:

            List of Client instance.
        """
        if isinstance(self.data['wireless-client'], list):
            return [Client(d) for d in self.data['wireless-client']]
        else:
            return [Client(self.data['wireless-client'])]

    @property
    def essid(self):
        """Essid"""
        return self.data.SSID.essid.get('#text', '')

    @property
    def bssid(self):
        """Mac (BSSID)"""
        return self.data.BSSID

    @property
    def score(self):
        """Score, used to sort networks.

        Score will take in account the total packets received, the dbm and if a
        ssid is susceptible to have dictionaries.
        """
        packet_score = int(self.packets.total)
        dbm_score = -int(self.dbm)
        dict_score = bool(any(self.essid.startswith(a) for a in DICTS))
        name_score = -1000 if not self.essid else 0
        return packet_score + dbm_score + dict_score

    @property
    def packets(self):
        """Return list of packets."""
        return self.data.packets

    @property
    def dbm(self):
        """Return dbm info"""
        return self.data['snr-info'].last_signal_dbm

    def __lt__(self, other):
        """Compare with score."""
        return self.score


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
                    return Result(sorted([AccessPoint(ap) for ap in results],
                                  key=lambda x: x.score,
                                  reverse=True))
                return []

            await asyncio.sleep(1)
