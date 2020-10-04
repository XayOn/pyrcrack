pyrcrack
--------

**Python aircrack-ng bindings**

PyrCrack is a Python API exposing a common aircrack-ng API. As AircrackNg will
run in background processes, and produce parseable output both in files and
stdout, the most pythonical approach are context managers, cleaning up after 

|pypi| |release| |downloads| |python_versions| |pypi_versions| |coverage| |actions|

.. |pypi| image:: https://img.shields.io/pypi/l/pyrcrack
.. |release| image:: https://img.shields.io/librariesio/release/pypi/pyrcrack
.. |downloads| image:: https://img.shields.io/pypi/dm/pyrcrack
.. |python_versions| image:: https://img.shields.io/pypi/pyversions/pyrcrack
.. |pypi_versions| image:: https://img.shields.io/pypi/v/pyrcrack
.. |coverage| image:: https://codecov.io/gh/XayOn/pyrcrack/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/XayOn/pyrcrack
.. |actions| image:: https://github.com/XayOn/pyrcrack/workflows/CI%20commit/badge.svg
    :target: https://github.com/XayOn/pyrcrack/actions

Installation
------------

This library is available on `Pypi <https://pypi.org/project/pyrcrack/>`_, you can install it directly with pip::

        pip install pyrcrack

Usage
-----

This library exports a basic aircrack-ng API aiming to keep always a small readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite commands
and auto-detects its usage instructions. Based on that, it dinamically builds
classes inheriting that usage as docstring and a run() method that accepts
keyword parameters and arguments, and checks them BEFORE trying to run them.

You can find some example usages in examples/ directory::

    async with pyrcrack.AircrackNg() as pcrack:
        await pcrack.run(sys.argv[1])
        # This also sets pcrack.proc as the running
        # process, wich is a `Process` instance.

        # get_result() is specific of AircrackNg class.
        print(await pcrack.get_result())

    # This will create temporary files needed, and
    # cleanup process after if required.


Some classes expose themselves as async iterators, as airodump-ng's wich
returns access points with its associated clients.

The following example will automatically keep printing results each 2 seconds::

        async def scan_for_targets():
            """Scan for targets, return json."""
            async with pyrcrack.AirodumpNg() as pdump:
                async for result in pdump(sys.argv[1]):
                    console.print(result)
                    await asyncio.sleep(2)

You can also list all available airmon interfaces, like so::

    async with pyrcrack.AirmonNg() as airmon:
        print(await airmon.list_wifis())

This will return a nice dict with all information as is returned by airmon-ng
