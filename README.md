
<div align="center">
<img src="https://github.com/XayOn/pyrcrack/raw/develop/docs/pythonlovesaircrack.png" role=img>

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/xayon/pyrcrack/actions/workflows/test.yml/badge.svg)](https://github.com/xayon/pyrcrack/actions/workflows/test.yml) [![CD - Build Package](https://github.com/xayon/pyrcrack/actions/workflows/release.yml/badge.svg)](https://github.com/xayon/pyrcrack/actions/workflows/release.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/pyrcrack.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pyrcrack/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pyrcrack.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/pyrcrack/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyrcrack.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/pyrcrack/) |
| Meta | [![code style - yapf](https://img.shields.io/badge/code%20style-yapf-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) 

</div>

**Python aircrack-ng bindings**

PyrCrack is a Python API exposing a common aircrack-ng API. As AircrackNg will
run in background processes, and produce parseable output both in files and
stdout, the most pythonical approach are context managers, cleaning up after 

This library exports a basic aircrack-ng API aiming to keep always a small
readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite commands
and auto-detects its usage instructions. Based on that, it dinamically builds
classes inheriting that usage as docstring and a run() method that accepts
keyword parameters and arguments, and checks them BEFORE trying to run them.

Some classes expose themselves as async iterators, as airodump-ng's wich
returns access points with its associated clients.

## Documentation

The [documentation](https://davidfrancos.net/pyrcrack) is made with [Material
for MkDocs](https://github.com/squidfunk/mkdocs-material) and is hosted by
[GitHub Pages](https://docs.github.com/en/pages).

### Examples

Be sure to check the python [notebook example](./docs/examples/example.ipynb)

You can have also have a look at the examples/ folder for some usage examples,
such as the basic "scan for targets", that will list available interfaces, let
you choose one, put it in monitor mode, and scan for targets updating results
each 2 seconds.

```python
import asyncio

import pyrcrack

from rich.console import Console
from rich.prompt import Prompt


async def scan_for_targets():
    """Scan for targets, return json."""
    console = Console()
    console.clear()
    console.show_cursor(False)
    airmon = pyrcrack.AirmonNg()

    interface = Prompt.ask(
	'Select an interface',
	choices=[a['interface'] for a in await airmon.interfaces])

    async with airmon(interface) as mon:
	async with pyrcrack.AirodumpNg() as pdump:
	    async for result in pdump(mon.monitor_interface):
		console.clear()
		console.print(result.table)
		await asyncio.sleep(2)


asyncio.run(scan_for_targets())
 ```

This snippet of code will produce the following results:

![scan](https://raw.githubusercontent.com/XayOn/pyrcrack/master/docs/scan.png)



# Contributors

![contributors](https://contrib.rocks/image?repo=xayon/pyrcrack)


## License

Pyrcrack is distributed under the terms of the [GPL2+](https://spdx.org/licenses/GPL2.html) license.

