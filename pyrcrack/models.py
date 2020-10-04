from rich.table import Table

DICTS = ('WLAN_', 'JAZZTEL_', 'MOVISTAR_')


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

    def asdict(self):
        return {
            'essid': self.essid,
            'bssid': self.bssid,
            'packets': str(self.packets.total),
            'dbm': str(self.dbm),
            'score': str(self.score)
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
        packet_score = int(self.packets.total)
        dbm_score = -int(self.dbm)
        dict_score = bool(any(self.essid.startswith(a) for a in DICTS))
        name_score = -1000 if not self.essid else 0
        return packet_score + dbm_score + dict_score + name_score

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
