"""Airdecap-ng."""
from .executor import ExecutorHelper


class AirdecapNg(ExecutorHelper):
    """Airdecap-ng 1.2 beta3 - (C) 2006-2013 Thomas d'Otreppe

    http://www.aircrack-ng.org

    Usage: airdecap-ng [options] <pcap file>

    Options:

        -l         : don't remove the 802.11 header
        -b <bssid> : access point MAC address filter
        -e <essid> : target network SSID
        -w <key>   : target network WEP key in hex
        -p <pass>  : target network WPA passphrase
        -k <pmk>   : WPA Pairwise Master Key in hex

        --help     : Displays this usage screen
    """

    command = 'airdecap-ng'
    sync = False
    requires_tempfile = False
    requires_tempdir = False
