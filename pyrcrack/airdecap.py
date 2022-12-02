"""Airdecap-ng."""
from .executor import ExecutorHelper


class AirdecapNg(ExecutorHelper):
    """Airdecap-ng 1.6  - (C) 2006-2020 Thomas d'Otreppe

    https://www.aircrack-ng.org

    Usage: airdecap-ng [options] <pcap file>

    Options:

        -l         : don't remove the 802.11 header
        -b <bssid> : access point MAC address filter
        -e <essid> : target network SSID
        -o <fname> : output file for decrypted packets (default <src>-dec)
        -w <key>   : target network WEP key in hex
        -c <fname> : output file for corrupted WEP packets (default <src>-bad)
        -p <pass>  : target network WPA passphrase
        -k <pmk>   : WPA Pairwise Master Key in hex
        --help     : Displays this usage screen

    """

    command = "airdecap-ng"
    sync = False
    requires_tempfile = False
    requires_tempdir = False
    requires_root = False
