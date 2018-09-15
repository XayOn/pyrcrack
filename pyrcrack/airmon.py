"""Airmon-ng and zc."""
from .executor import ExecutorHelper


class Airmon(ExecutorHelper):
    """Base executor for airmon-ng and zc."""
    command = None
    requires_tempfile = False
    requires_tempdir = False

    def run_sync(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        assert any(a in args[0] for a in ('start', 'stop', 'check'))
        assert len(args) > 1
        return super().run_sync(*args, **kwargs)

    async def run_async(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        assert any(a in args[0] for a in ('start', 'stop', 'check'))
        assert len(args) > 1
        return await super().run_async(*args, **kwargs)


class AirmonNG(Airmon):
    """ Airmon-ZC
    Usage: airmon-zc <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'


class AirmonZc(Airmon):
    """ Airmon-ZC
    Usage: airmon-nc <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-zc'
