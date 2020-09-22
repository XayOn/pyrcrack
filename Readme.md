# pyrcrack

**Python aircrack-ng bindings**

PyrCrack is a Python API exposing a common aircrack-ng API. As AircrackNg will
run in background processes, and produce parseable output both in files and
stdout, the most pythonical approach are context managers, cleaning up after 

<span style="display:block;text-align:center">![](https://img.shields.io/pypi/l/pyrcrack) ![](https://img.shields.io/librariesio/release/pypi/pyrcrack) ![](https://img.shields.io/pypi/dm/pyrcrack) ![](https://img.shields.io/pypi/pyversions/pyrcrack) ![](https://img.shields.io/pypi/v/pyrcrack) [![codecov](https://codecov.io/gh/XayOn/pyrcrack/branch/develop/graph/badge.svg)](https://codecov.io/gh/XayOn/pyrcrack) [![Actions Status](https://github.com/XayOn/pyrcrack/workflows/CI%20commit/badge.svg)](https://github.com/XayOn/pyrcrack/actions)</span>

# Installation

This library is available on [pypi](https://pypi.org/project/pyrcrack/), you can install it directly with pip

```bash
pip install pycrack
```

# Usage

This library exports a basic aircrack-ng API aiming to keep always a small readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite commands
and auto-detects its usage instructions. Based on that, it dinamically builds
classes inheriting that usage as docstring and a run() method that accepts
keyword parameters and arguments, and checks them BEFORE trying to run them.

You can find some example usages in examples/ directory.

```python
    async with pyrcrack.AircrackNg() as pcrack:
        await pcrack.run(sys.argv[1])
        # This also sets pcrack.proc as the running
        # process, wich is a `Process` instance.

        # get_result() is specific of AircrackNg class.
        print(await pcrack.get_result())

    # This will create temporary files needed, and
    # cleanup process after if required.
```

There are some syntactic sugar methods, like "result_updater" on pyrcrack class.

The following example will automatically keep updating, for 10 seconds, a
meta["results"] property on pdump.

```python

    import pyrcrack
    import sys
    import asyncio
    from async_timeout import timeout

    async def test(max_timeout):
        async with pyrcrack.AirodumpNg() as pdump:
            with suppress(asyncio.TimeoutError):
                async with timeout(max_timeout):
                    await pdump.run(sys.argv[1])
                    while True:
                        await asyncio.sleep(1)
                        print(pdump.meta)
            return await pdump.proc.terminate()


    asyncio.run(test(10))
```


You can also list all available airmon interfaces, like so:

```python
    async with pyrcrack.AirmonZc() as airmon:
        print(await airmon.list_wifis())
```

This will return a nice dict with all information as is returned by airmon-zc
