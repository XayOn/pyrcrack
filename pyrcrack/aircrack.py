"""Aircrack-ng."""
from .executor import ExecutorHelper


class AircrackNg(ExecutorHelper):
    """ Aircrack-ng 1.2 beta3 - (C) 2006-2013 Thomas d'Otreppe
  http://www.aircrack-ng.org

  Usage: aircrack-ng [options] <file>...

  Options:

      -a <amode> : force attack mode (1/WEP, 2/WPA-PSK)
      -e <essid> : target selection: network identifier
      -b <bssid> : target selection: access point's MAC
      -p <nbcpu> : # of CPU to use  (default: all CPUs)
      -q         : enable quiet mode (no status output)
      -C <macs>  : merge the given APs to a virtual one
      -l <file>  : write key to file
      -c         : search alpha-numeric characters only
      -t         : search binary coded decimal chr only
      -h         : search the numeric key for Fritz!BOX
      -d <mask>  : use masking of the key (A1:XX:CF:YY)
      -m <maddr> : MAC address to filter usable packets
      -n <nbits> : WEP key length :  64/128/152/256/512
      -i <index> : WEP key index (1 to 4), default: any
      -f <fudge> : bruteforce fudge factor,  default: 2
      -k <korek> : disable one attack method  (1 to 17)
      -x or -x0  : disable bruteforce for last keybytes
      -x1        : last keybyte bruteforcing  (default)
      -x2        : enable last  2 keybytes bruteforcing
      -X         : disable  bruteforce   multithreading
      -y         : experimental  single bruteforce mode
      -K         : use only old KoreK attacks (pre-PTW)
      -s         : show the key in ASCII while cracking
      -M <num>   : specify maximum number of IVs to use
      -D         : WEP decloak, skips broken keystreams
      -P <num>   : PTW debug:  1: disable Klein, 2: PTW
      -1         : run only 1 try to crack key with PTW
      -w <words> : path to wordlist(s) filename(s)
      -E <file>  : create EWSA Project file v3
      -J <file>  : create Hashcat Capture file
      -S         : WPA cracking speed test
      -r <DB>    : path to airolib-ng database (Cannot be used with -w)
      -u         : Displays # of CPUs & MMX/SSE support
      --help     : Displays this usage screen
    """
    command = "aircrack-ng"
    requires_tempfile = True
    requires_tempdir = False

    async def run_async(self, *args, **kwargs):
        if self.tempfile:
            kwargs['l'] = self.tempfile.name
        return await super().run_async(*args, **kwargs)

    def run_sync(self, *args, **kwargs):
        if self.tempfile:
            kwargs['l'] = self.tempfile.name
        return super().run(*args, **kwargs)

    async def get_result(self):
        await self.proc.wait()
        return self.tempfile.read()
