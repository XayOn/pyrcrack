"""Airmon-ng"""
from .executor import ExecutorHelper
from .models import Interfaces


class AirmonNg(ExecutorHelper):
    """ Airmon-NG
    Usage: airmon-ng <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'
    requires_tempfile = False
    requires_tempdir = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dirty = False
        self.monitor_enabled = []

    async def run(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        self.dirty = True
        if args:
            assert any(a in args[0] for a in ('start', 'stop', 'check'))
        return await super().run(*args, **kwargs)

    async def __aenter__(self):
        """Put selected interface in monitor mode."""
        if not self.run_args[0][0]:
            raise RuntimeError('Should be called (airmon()) first.')
        ifaces = await self.interfaces
        if not any(a.interface == self.run_args[0][0] for a in ifaces):
            raise ValueError('Invalid interface selected')
        await self.run('start', self.run_args[0][0])
        # Save interface data while we're on the async cm.
        self._interface_data = await self.interfaces
        return self

    async def __aexit__(self, *args, **kwargs):
        """Set monitor-enabled interfaces back to normal"""
        await self.run('stop', self.monitor_interface)

    @property
    def monitor_interface(self):
        iface = next(a for a in self._interface_data
                     if a.interface == self.run_args[0][0])
        return iface.monitor

    @property
    async def interfaces(self):
        """List of currently available interfaces as reported by airmon-ng

        This is an awaitable property, use it as in::

        async with AirmonNg() as airmon:
            await airmon.interfaces

        Returns: None
        """
        if not self.dirty:
            await self.run()
            self.dirty = False
        return Interfaces(await self.readlines())
