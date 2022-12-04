# How it works
As AircrackNg will run in background processes, and produce parseable output
both in files and stdout, the most pythonical approach are context managers,
**cleaning up after**.

!!! note 

    This library exports a basic aircrack-ng API aiming to keep always a small
    readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite
commands and auto-detects its usage instructions. Based on that, it dinamically
builds classes inheriting that usage as docstring and a `run()` method that
accepts keyword parameters and arguments, and checks them **before** trying to
run them.

Some classes expose themselves as async iterators, as airodump-ng's wich
returns access points with its associated clients.
