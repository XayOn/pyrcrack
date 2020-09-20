"""Aidorump."""

from glob import glob
import asyncio
import csv
import io
from contextlib import suppress
from .executor import ExecutorHelper
from .models import AccessPoint, Client


class AirodumpNg(ExecutorHelper):
    """Airodump-ng 1.3  - (C) 2006-2018 Thomas d'Otreppe
       https://www.aircrack-ng.org

       usage: airodump-ng <options> <interface>[,<interface>,...]

       Options:
           --ivs                 : Save only captured IVs
           --gpsd                : Use GPSd
           --write <prefix>      : Dump file prefix
           -w <prefix>           : same as --write
           --beacons             : Record all beacons in dump file
           --update <secs>       : Display update delay in seconds
           --showack             : Prints ack/cts/rts statistics
           -h                    : Hides known stations for --showack
           -f <msecs>            : Time in ms between hopping channels
           --berlin <secs>       : Time before removing the AP/client
                                   from the screen when no more packets
                                   are received (Default: 120 seconds)
           -r <file>             : Read packets from that file
           -x <msecs>            : Active Scanning Simulation
           --manufacturer        : Display manufacturer from IEEE OUI list
           --uptime              : Display AP Uptime from Beacon Timestamp
           --wps                 : Display WPS information (if any)
           --output-format
                       <formats> : Output format. Possible values:
                                   pcap, ivs, csv, gps, kismet, netxml
           --ignore-negative-one : Removes the message that says
                                   fixed channel <interface>: -1
           --write-interval <seconds> : Output file(s) write
                                        interval in seconds
           --background <enable> : Override background detection.

       Filter options:
           --encrypt <suite>     : Filter APs by cipher suite
           --netmask <netmask>   : Filter APs by mask
           --bssid <bssid>       : Filter APs by BSSID
           --essid <essid>       : Filter APs by ESSID
           --essid-regex <regex> : Filter APs by ESSID using a regular
                                   expression
           -a                    : Filter unassociated clients

       By default, airodump-ng hop on 2.4GHz channels.
       You can make it capture on other/specific channel(s) by using:
           --ht20                : Set channel to HT20 (802.11n)
           --ht40-               : Set channel to HT40- (802.11n)
           --ht40+               : Set channel to HT40+ (802.11n)
           --channel <channels>  : Capture on specific channels
           --band <abg>          : Band on which airodump-ng should hop
           -C <frequencies>      : Uses these frequencies in MHz to hop
           --cswitch <method>    : Set channel switching method
                         0       : FIFO (default)
                         1       : Round Robin
                         2       : Hop on last
           -s                    : same as --cswitch

           --help                : Displays this usage screen
    """
    requires_tempfile = False
    requires_tempdir = True
    command = "airodump-ng"

    async def run(self, *args, **kwargs):
        """Run async, with prefix stablished as tempdir."""
        if not ('write' in kwargs or 'w' in kwargs):
            kwargs.pop('w', None)
            kwargs['write'] = self.tempdir.name + "/" + self.uuid
        asyncio.create_task(self.result_updater())
        return await super().run(*args, **kwargs)

    async def result_updater(self):
        """Set result on local object."""
        while not self.proc:
            await asyncio.sleep(1)
        while self.proc.returncode is None:
            self.meta['result'] = self.get_results()
            await asyncio.sleep(2)

    @property
    def csv_file(self):
        """Return csv file, not kismet one."""
        glb = glob(self.tempdir.name + "/" + self.uuid + "-*.csv")
        with suppress(StopIteration):
            return next(a for a in glb if 'kismet' not in a)

    def get_results(self):
        """Return results at this moment."""

        if not self.csv_file:
            return {'clients': [], 'aps': []}

        def clean(line):
            """Format name."""
            for name, value in line.items():
                res = name.strip().lower().replace(' ', '_')
                yield res.replace('#_', '').replace('-', '_'), value.strip()

        def get_data(content):
            """Read using a temporary csv file."""
            with io.StringIO() as fio:
                fio.write(content)
                fio.seek(0)
                for line in [c for c in csv.DictReader(fio, dialect='excel')]:
                    yield dict(clean(line))

        def get_clients(apoint, clients):
            """Get clients for a specific ap."""
            return [c for c in clients if c.bssid == apoint["bssid"]]

        lines = open(self.csv_file).readlines()
        inx = lines.index('Station MAC, First time seen, Last time seen,'
                          ' Power, # packets, BSSID, Probed ESSIDs\n')

        clients = ''.join([a for a in lines[inx:] if a.strip()])
        clients = [Client(**d) for d in get_data(''.join(clients))]
        aps = ''.join([a for a in lines[:inx] if a.strip()])
        aps = [
            AccessPoint(**d, clients=get_clients(d, clients))
            for d in get_data(''.join(aps))
        ]

        return {'aps': aps, 'clients': clients}

    def sorted_aps(self):
        """Return sorted aps by score."""
        return sorted(self.meta['result']['aps'],
                      key=lambda x: x.score,
                      reverse=True)
