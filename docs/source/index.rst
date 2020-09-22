.. pyrcrack documentation master file, created by
   sphinx-quickstart on Tue Jan  9 03:18:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyrcrack's documentation!
====================================

PyrCrack is a Python API exposing a common aircrack-ng API. As AircrackNg will
run in background processes, and produce parseable output both in files and
stdout, the most pythonical approach are context managers, cleaning up after 

Each pyrcrack's class is an async context manager exposing a `run` coroutine
that will start up an aircrack-ng suite's process, communicate with it and
clean up residual files.

You can see the example usages on examples/ directory.

.. toctree::
   api/modules
   :maxdepth: 2
   :caption: Contents:
