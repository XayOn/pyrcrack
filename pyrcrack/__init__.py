"""pyrcrack.

Aircrack-NG python bindings
"""
import subprocess

from .aircrack import AircrackNg  # noqa
from .airdecap import AirdecapNg  # noqa
from .aireplay import AireplayNg  # noqa
from .airmon import AirmonNg  # noqa
from .airbase import AirbaseNg  # noqa
from .airdecloack import AirdecloackNg  # noqa
from .airodump import AirodumpNg  # noqa


def check():
    """Check if aircrack-ng is compatible."""
    assert '1.6' in subprocess.check_output(['aircrack-ng', '-v'])
