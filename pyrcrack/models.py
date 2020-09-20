"""Models."""
from dataclasses import dataclass

DICTS = ('WLAN_', 'JAZZTEL', 'Movistar', 'movistar', 'MOVISTAR')


@dataclass
class AccessPoint:
    """Represents an AP, as outputted by airodump-ng."""
    clients: dict
    speed: str
    channel: str
    first_time_seen: str
    beacons: str
    lan_ip: str
    essid: str
    last_time_seen: str
    privacy: str
    key: str
    iv: str
    cipher: str
    authentication: str
    power: str
    bssid: str
    id_length: str

    @property
    def score(self):
        """**Kinda-hackability** orientative score"""
        beacons_score = int(self.iv) / 1000 if int(self.iv) < 1000 else 1
        enc_score = {'WEP': 1, 'WPA2': 0.3, 'WPA': 0.3}.get(self.cipher, 0)
        power_score = -float(self.power) / 100
        dict_score = int(any(a in self.essid for a in DICTS))
        clients_score = len(self.clients)
        total_score = (beacons_score + enc_score + clients_score +
                       power_score + dict_score)
        return round((total_score / 5) * 100)


@dataclass
class Client:
    """Represents a client."""
    probed_essids: str
    first_time_seen: str
    power: str
    bssid: str
    station_mac: str
    last_time_seen: str
    packets: str
