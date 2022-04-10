"""Airmon-ng and zc."""
import io
import csv
from .executor import ExecutorHelper


class AirmonNg(ExecutorHelper):
    """ Airmon-NG
    Usage: airmon-ng <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'
    requires_tempfile = False
    requires_tempdir = False

    async def run(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        if args:
            assert any(a in args[0] for a in ('start', 'stop', 'check'))
        return await super().run(*args, **kwargs)

    @staticmethod
    def parse(res):
        """Parse csv results"""
        with io.StringIO() as fileo:
            fileo.write(res.decode().strip().replace('\t\t', '\t'))
            fileo.seek(0)
            reader = csv.DictReader(fileo, dialect='excel-tab')
            return [{a.lower(): b for a, b in row.items()} for row in reader]

    async def set_monitor(self, wifi, *args):
        """Set monitor mode interface"""
        await self.run('start', wifi, *args)
        res = (await self.proc.communicate())[0].split(b'\n')
        pos = res.index(b'PHY	Interface	Driver		Chipset')
        return self.parse(b'\n'.join([a for a in res[pos:] if a]))

    async def list_wifis(self):
        """Return a list of wireless networks as advertised by airmon-zc"""
        await self.run()
        return self.parse((await self.proc.communicate())[0])
