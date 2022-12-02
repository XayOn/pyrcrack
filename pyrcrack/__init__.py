"""pyrcrack.

Aircrack-NG python bindings
"""

from contextvars import ContextVar

from .aircrack import AircrackNg  # noqa
from .airdecap import AirdecapNg  # noqa
from .aireplay import AireplayNg  # noqa
from .airmon import AirmonNg  # noqa
from .airbase import AirbaseNg  # noqa
from .airdecloack import AirdecloackNg  # noqa
from .airodump import AirodumpNg  # noqa

MONITOR = ContextVar('monitor_interface')

__version__ = '1.1.3'
