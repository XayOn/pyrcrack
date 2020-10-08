"""Airmon-ng"""
import io
import csv
import re
from .executor import ExecutorHelper

MONITOR_RE = re.compile(
    r'\t\t\((\w+) (\w+) mode vif (\w+) for \[\w+\](\w+) on \[\w+\](\w+)\)')


class AirmonNg(ExecutorHelper):
    """ Airmon-NG
    Usage: airmon-ng <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'
    requires_tempfile = False
    requires_tempdir = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitor_enabled = []

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

    @property
    def interface(self):
        return self.run_args[0][0]

    async def __aenter__(self):
        """Put selected interface in monitor mode."""
        if not self.interface:
            raise RuntimeError('Should be called (airmon()) first.')
        self.interface_data = await self.set_monitor(self.interface)
        return self

    @property
    def monitor_interface(self):
        return self.interface_data[self.interface]['monitor']['interface']

    async def __aexit__(self, *args, **kwargs):
        """Set monitor-enabled interfaces back to normal"""
        for interface in self.monitor_enabled:
            await self.stop(interface)

    async def stop(self, wifi, *args):
        """Stop monitor mode"""
        await self.run('stop', wifi, *args)

    async def set_monitor(self, wifi, *args):
        """Set monitor mode interface"""
        assert any(a.get('interface') == wifi
                   for a in await self.interfaces), 'Wrong interface selected'

        await self.run('start', wifi, *args)
        res = [a for a in (await self.proc.communicate())[0].split(b'\n') if a]
        pos = res.index(b'PHY	Interface	Driver		Chipset')
        ifaces_data = self.parse(b'\n'.join(
            [a for a in res[pos:] if a and not a.startswith(b'\t\t')]))
        ifaces = {k['interface']: k for k in ifaces_data}
        keys = ['driver', 'mode', 'status', 'original_interface', 'interface']
        monitor_lines = res[pos + len(ifaces_data) + 1:]
        monitor_data = (dict(zip(keys,
                                 MONITOR_RE.match(a.decode()).groups()))
                        for a in monitor_lines if MONITOR_RE.match(a.decode()))
        for data in monitor_data:
            ifaces[data['original_interface']][data['mode']] = data
            if data['mode'] == 'monitor':
                self.monitor_enabled.append(data['interface'])

        return ifaces

    @property
    async def interfaces(self):
        """List of currently available interfaces as reported by airmon-ng

        This is an awaitable property, use it as in::

        async with AirmonNg() as airmon:
            await airmon.interfaces

        Returns: None
        """
        await self.run()
        return self.parse((await self.proc.communicate())[0])
