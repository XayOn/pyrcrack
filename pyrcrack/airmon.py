from .executor import ExecutorHelper


class AirmonZc(ExecutorHelper):
    """ Airmon-ZC
    Usage: airmon-zc <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-zc'
    sync = False

    def run(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        assert any(a in args[0] for a in ('start', 'stop', 'check'))
        assert len(args) > 1
        return super().run(*args, **kwargs)


class AirmonNg(ExecutorHelper):
    """ Airmon-ZC
    Usage: airmon-zc <start|stop|check> <interface> [channel or frequency]
    """

    command = 'airmon-ng'
    sync = False

    def run(self, *args, **kwargs):
        """Check argument position. Forced for this one."""
        assert any(a in args[0] for a in ('start', 'stop', 'check'))
        assert len(args) > 1
        return super().run(*args, **kwargs)
