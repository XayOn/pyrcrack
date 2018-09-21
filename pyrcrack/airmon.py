"""Airmon-ng and zc."""
import io
import csv
from .executor import ExecutorHelper


class Airmon(ExecutorHelper):
    """Base executor for airmon-ng and zc."""
    command = None
    requires_tempfile = False
    requires_tempdir = False

    async def run(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        if args:
            assert any(a in args[0] for a in ('start', 'stop', 'check'))
        return await super().run(*args, **kwargs)


class AirmonNg(Airmon):
    """ Airmon-NG
    Usage: airmon-ng <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'


class AirmonZc(Airmon):
    """ Airmon-ZC
    Usage: airmon-nc <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-zc'

    async def list_wifis(self):
        """Return a list of wireless networks as advertised by airmon-zc"""
        with io.StringIO() as fileo:
            await self.run()
            res = await self.proc.communicate()
            fileo.write(res[0].decode().strip().replace('\t\t', '\t'))
            fileo.seek(0)
            reader = csv.DictReader(fileo, dialect='excel-tab')
            return [{a.lower(): b for a, b in row.items()} for row in reader]
