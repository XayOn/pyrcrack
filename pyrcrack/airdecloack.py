"""Airdecloack-ng."""

from .executor import ExecutorHelper


class AirdecloackNg(ExecutorHelper):
    """ Airdecloak-ng 1.6  - (C) 2008-2020 Thomas d'Otreppe
    https://www.aircrack-ng.org
    Available filters::

         signal:               Try to filter based on signal.
         duplicate_sn:         Remove all duplicate sequence numbers
                               for both the AP and the client.
         duplicate_sn_ap:      Remove duplicate sequence number for
                               the AP only.
         duplicate_sn_client:  Remove duplicate sequence number for the
                               client only.
         consecutive_sn:       Filter based on the fact that IV should
                               be consecutive (only for AP).
         duplicate_iv:         Remove all duplicate IV.
         signal_dup_consec_sn: Use signal (if available), duplicate and
                               consecutive sequence number (filtering is
                                much more precise than using all these
                                filters one by one).

    Usage: airdecloak-ng [options]

    Options:
       -i <file>             : Input capture file
       --ssid <ESSID>        : ESSID of the network to filter
       --bssid <BSSID>       : BSSID of the network to filter
       -o <file>             : Output packets (valid) file
       -c <file>             : Output packets (cloaked) file
       -u <file>             : Output packets (unknown/ignored) file
       --filters <filters>   : Apply filters (separated by a comma).
       --null-packets        : Assume that null packets can be cloaked.
       --disable-base_filter : Do not apply base filter.
       --drop-frag           : Drop fragmented packets
       --help                : Displays this usage screen
    """
    command = "airdecloack-ng"
    requires_tempfile = False
    requires_tempdir = False
    requires_root = False
