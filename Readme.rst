pyrcrack
-----------------------------

.. image:: https://travis-ci.org/XayOn/pyrcrack.svg?branch=master
    :target: https://travis-ci.org/XayOn/pyrcrack

.. image:: https://coveralls.io/repos/github/XayOn/pyrcrack/badge.svg?branch=master
 :target: https://coveralls.io/github/XayOn/pyrcrack?branch=master

.. image:: https://badge.fury.io/py/pyrcrack.svg
    :target: https://badge.fury.io/py/pyrcrack

Python aircrack-ng bindings


Usage
-----

This library exports a basic aircrack-ng API aiming to keep always a small readable codebase.

This has led to a simple library that executes each of the aircrack-ng's suite commands
and auto-detects its usage instructions. Based on that, it dinamically builds
classes inheriting that usage as docstring and a run() method that accepts
keyword parameters and arguments, and checks them BEFORE trying to run them.

This can be easily understood as::

        # Run aircrack-ng in quiet mode against foo.cap
        from pyrcrack import AircrackNg

        AircrackNg().run('foo.cap', q=True)


Or, returning a coroutine::

        from pyrcrack import AircrackNg
        cmd = AircrackNg()
        cmd.sync = False
        cmd.run('foo.cap')


Distributing
------------

Distribution may be done in the usual setuptools way.
If you don't want to use pipenv, just use requirements.txt file as usual and
remove Pipfile, setup.py will auto-detect Pipfile removal and won't try to
update requirements.

Note that, to enforce compatibility between PBR and Pipenv, this updates the
tools/pip-requires and tools/test-requires files each time you do a *dist*
command

General notes
--------------

This package uses PBR and pipenv.
Pipenv can be easily replaced by a virtualenv by keeping requirements.txt
instead of using pipenv flow.
If you don't need, or you're not actually using git + setuptools distribution
system, you can enable PBR manual versioning by creating a METADATA file with
content like::

    Name: pyrcrack
    Version: 0.0.1

Generating documentation
------------------------

This package contains a extra-requires section specifiying doc dependencies.
There's a special hook in place that will automatically install them whenever
we try to build its dependencies, thus enabling us to simply execute::

        pipenv run python setup.py build_sphinx

to install documentation dependencies and buildd HTML documentation in docs/build/


Passing tests
--------------

Running tests should always be done inside pipenv.
This package uses behave for TDD and pytest for unit tests, you can execute non-wip
tests and behavioral tests using::

        pipenv run python setup.py test
