"""Airbase-ng."""

from .executor import ExecutorHelper


class AirbaseNg(ExecutorHelper):
    """Airbase-ng 1.6  - (C) 2008-2020 Thomas d'Otreppe
    Original work: Martin Beck
    https://www.aircrack-ng.org

    Usage: airbase-ng <options> <replay interface>

    Options:

        -a <bssid>       : set Access Point MAC address
        -i <iface>       : capture packets from this interface
        -w <key>         : use this WEP key to en-/decrypt packets
        -h <MAC>         : source mac for MITM mode
        -f <disallow>    : disallow specified client MACs (default: allow)
        -W 0|1           : [don't] set WEP flag in beacons 0|1 (default: auto)
        -q               : quiet (do not print statistics)
        -v               : verbose (print more messages)
        -A               : Ad-Hoc Mode (allows other clients to peer)
        -Y <proc>        : (in|out|both) external packet processing
        -c <channel>     : sets the channel the AP is running on
        -X               : hidden ESSID
        -s               : force shared key authentication (default: auto)
        -S               : set shared key challenge length (default: 128)
        -L               : Caffe-Latte WEP attack
        -N               : cfrag WEP attack (recommended)
        -x <nbpps>       : number of packets per second (default: 100)
        -y               : disables responses to broadcast probes
        -0               : set all WPA,WEP,open tags.
        -z <type>        : sets WPA1 tags.
        -Z <type>        : same as -z, but for WPA2
        -V <type>        : fake EAPOL 1=MD5 2=SHA1 3=auto
        -F <prefix>      : write all sent and received frames into pcap file
        -P               : respond to all probes, even when specifying ESSIDs
        -I <interval>    : sets the beacon interval value in ms
        -C <seconds>     : enables beaconing of probed ESSID values
        -n <hex>         : User specified ANonce when doing the 4-way handshake
        --bssid <MAC>    : BSSID to filter/use
        --bssids <file>  : read a list of BSSIDs out of that file
        --client <MAC>   : MAC of client to filter
        --clients <file> : read a list of MACs out of that file
        --essid <ESSID>  : specify a single ESSID (default: default)
        --essids <file>  : read a list of ESSIDs out of that file
        --help           : Displays this usage screen
    """

    command = "airbase-ng"
    requires_tempfile = False
    requires_tempdir = False
    requires_root = True
