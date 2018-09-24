"""Models."""
from dataclasses import dataclass


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
