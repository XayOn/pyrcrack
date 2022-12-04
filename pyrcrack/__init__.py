"""pyrcrack.

Aircrack-NG python bindings
"""

from contextvars import ContextVar

from .airbase import AirbaseNg  # noqa
from .aircrack import AircrackNg  # noqa
from .airdecap import AirdecapNg  # noqa
from .airdecloack import AirdecloackNg  # noqa
from .aireplay import AireplayNg  # noqa
from .airmon import AirmonNg  # noqa
from .airodump import AirodumpNg  # noqa

MONITOR = ContextVar("monitor_interface")

__version__ = "1.2.5"
