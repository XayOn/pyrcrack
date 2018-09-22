"""Aidorump."""

from glob import glob
import asyncio
import csv
from .executor import ExecutorHelper


class AirodumpNg(ExecutorHelper):
    """Airodump-ng 1.2 beta3 - (C) 2006-2013 Thomas d'Otreppe
       http://www.aircrack-ng.org

       usage: airodump-ng <options> <interface>[,<interface>,...]

       Options:
           --ivs                 : Save only captured IVs
           --gpsd                : Use GPSd
           --write <prefix> : Dump file prefix
           -w                    : same as --write
           --beacons             : Record all beacons in dump file
           --update       <secs> : Display update delay in seconds
           --showack             : Prints ack/cts/rts statistics
           -h                    : Hides known stations for --showack
           -f            <msecs> : Time in ms between hopping channels
           --berlin       <secs> : Time before removing the AP/client
                                   from the screen when no more packets
                                   are received (Default: 120 seconds)
           -r             <file> : Read packets from that file
           -x            <msecs> : Active Scanning Simulation
           --manufacturer        : Display manufacturer from IEEE OUI list
           --uptime              : Display AP Uptime from Beacon Timestamp
           --output-format
                       <formats> : Output format. Possible values:
                                   pcap, ivs, csv, gps, kismet, netxml
           --ignore-negative-one : Removes the message that says
                                   fixed channel <interface>: -1

       Filter options:
           --encrypt   <suite>   : Filter APs by cipher suite
           --netmask <netmask>   : Filter APs by mask
           --bssid     <bssid>   : Filter APs by BSSID
           --essid     <essid>   : Filter APs by ESSID
           --essid-regex <regex> : Filter APs by ESSID using a regular
                                   expression
           -a                    : Filter unassociated clients

       By default, airodump-ng hop on 2.4GHz channels.
       You can make it capture on other/specific channel(s) by using:
           --channel <channels>  : Capture on specific channels
           --band <abg>          : Band on which airodump-ng should hop
           -C    <frequencies>   : Uses these frequencies in MHz to hop
           --cswitch  <method>   : Set channel switching method
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

    def get_results(self):
        """Return results at this moment."""
        filename = glob(self.tempdir.name + "/" + self.uuid + "*.csv")
        if not filename:
            return []
        with open(filename[0]) as fileo:
            return [dict(a) for a in csv.DictReader(fileo, delimiter=';')]
