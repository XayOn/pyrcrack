import io
import csv
import re
from rich.table import Table
from parse import parse

DICTS = ('WLAN_', 'JAZZTEL_', 'MOVISTAR_')
APL_FMT = "{date}  Sending {attack} (code {num}) to {dest} -- BSSID: [{bssid}]"
MONITOR_RE = re.compile(
    r'\t\t\((\w+) (\w+) mode vif (\w+) for \[\w+\](\w+) on \[\w+\](\w+)\)')


class Result(list):

    @property
    def table(self):
        """Return a nicely formatted table with results."""
        table = Table(show_header=True,
                      header_style='bold magenta',
                      show_footer=False)
        if self:
            keys = self[0].asdict().keys()
            for key in keys:
                table.add_column(key.capitalize())

            for res in self:
                res = res.asdict()
                table.add_row(*[res[k] for k in keys])
        return table


class Interface:

    def __init__(self, data, monitor_data):
        self.data = data
        for data in monitor_data:
            if data['original_interface'] == self.data['interface']:
                self.data[data['mode']] = data

    @property
    def interface(self):
        return self.data['interface']

    def __eq__(self, other):
        if isinstance(other, Interface):
            return other.interface == self.interface
        return self.interface == other

    @property
    def monitor(self):
        return self.data.get('monitor', {}).get('interface',
                                                self.data['interface'])

    def asdict(self):
        return self.data

    def __str__(self):
        return self.interface


class Interfaces(Result):

    def __init__(self, data):
        if data == [b'Run it as root']:
            raise Exception('Pyrcrack must be run as root')
        pos = data.index(b'PHY	Interface	Driver		Chipset')
        ifaces_data = self.parse(b'\n'.join(
            [a for a in data[pos:] if a and not a.startswith(b'\t\t')]))
        monitor_data = filter(lambda x: MONITOR_RE.match(x.decode()),
                              data[pos + len(ifaces_data):])

        def groups(data):
            return MONITOR_RE.match(data.decode()).groups()

        keys = ['driver', 'mode', 'status', 'original_interface', 'interface']
        monitor_data = [dict(zip(keys, groups(a))) for a in monitor_data]
        self.extend([Interface(a, monitor_data) for a in ifaces_data])

    @staticmethod
    def parse(res):
        """Parse csv results"""
        with io.StringIO() as fileo:
            fileo.write(res.decode().strip().replace('\t\t', '\t'))
            fileo.seek(0)
            reader = csv.DictReader(fileo, dialect='excel-tab')
            return [{a.lower(): b for a, b in row.items()} for row in reader]


class Client:

    def __init__(self, data):
        self.data = data

    @property
    def bssid(self):
        return self.data['client-mac']

    @property
    def packets(self):
        return getattr(self.data.packets, "total", 0)

    @property
    def dbm(self):
        return self.data['snr-info'].last_signal_dbm


class AccessPoint(dict):
    """Represents an access point.

    Stores internal data in "data" property
    """

    def __init__(self, data):
        """Initialize an access point

        Arguments:

            data: Dot data structure from kismet xml file.
        """
        self.data = data
        self.update(self.asdict())

    def __repr__(self):
        return f"{self.essid} - ({self.bssid})"

    @property
    def airodump(self):
        return {'channel': self.channel, 'bssid': self.bssid}

    @property
    def channel(self):
        return self.data.channel

    @property
    def encryption(self):
        return self.data.SSID.encryption

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
    def total_packets(self):
        return getattr(self.packets, "total", 0)

    def asdict(self):
        return {
            'essid': self.essid,
            'bssid': self.bssid,
            'packets': str(self.total_packets),
            'dbm': str(self.dbm),
            'score': str(self.score),
            'channel': str(self.channel),
            'encryption': '/'.join(self.encryption)
        }

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
        packet_score = int(self.total_packets)
        dbm_score = -int(self.dbm)
        dict_score = bool(any(self.essid.startswith(a) for a in DICTS))
        name_score = -1000 if not self.essid else 0
        enc_score = 1000 if 'WEP' in self.encryption else 0
        return packet_score + dbm_score + dict_score + name_score + enc_score

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


class AireplayResult(dict):
    """Single aiplay result line"""

    def __init__(self, *args, **kwargs):
        self.update(parse(APL_FMT, kwargs.pop("_data")).named)
        super().__init__(*args, **kwargs)

    def asdict(self):
        return self


class AireplayResults(Result):
    """Aireplay results."""

    def __init__(self, data):
        self.extend((AireplayResult(_data=a) for a in data.split('\n')
                     if 'BSSID' in a))
