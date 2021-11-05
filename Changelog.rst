Changelog
=========


1.1.2 (2021-11-05)
------------------

Fix
~~~
- Added run-as-root message. [David Francos]
- Fixed airmon test. [David Francos]

Other
~~~~~
- Chore: Fixed aireplay example (and improved it a bit) [David Francos]
- Fixed pep8. [David Francos]
- Feat: Added debug mode. Don't delete tempfiles. [David Francos]
- Closes: #24 Added total_packets property. [David Francos]
- Merge branch 'develop' of github.com:XayOn/pyrcrack into develop.
  [David Francos]
- Create codeql-analysis.yml. [David Francos]


1.1.1 (2021-03-21)
------------------
- Version bump to 1.1.1. [David Francos]
- Closes: #20 Fix optimization on mon iface search. [David Francos]

  Seems like on some scenarios (still unclear), assuming an extra newline
  character will break monitor interface lookup. As this is only an
  optimization, it can be safely removed.
- Trying rich approach to GH detecting poetry packages. [David Francos]
- Trying rich approach to GH detecting poetry packages. [David Francos]
- Updated ipnb example. [David Francos]
- Fixed ipynb. [David Francos]
- Added example notebook to readme. [David Francos]


1.1.0 (2020-10-09)
------------------
- Fixed PEP-8. [David Francos]
- Added ipython notebook example. [David Francos]
- Merge tag '1.1.0' into develop. [David Francos]

  1.1.0
- Merge branch 'release/1.1.0' into master. [David Francos]
- Version bump to 1.1.0. [David Francos]
- Added encryption to ap list. [David Francos]
- Updated examples. [David Francos]
- Refactor on airodump. [David Francos]

  - Added channel
  - Fixed default params behaviour (it was a mess and it wasnt working)
- Fixed PEP-8. [David Francos]
- Closes: #18 Refactor on airodump-ng module. [David Francos]
- Added logo. [David Francos]
- Added logo. [David Francos]
- Not overriding __call__ on airmon. [David Francos]
- Updated readme. [David Francos]
- Merge branch 'develop' into master. [David Francos]
- Updated readme. [David Francos]
- Removed Pyrcrack class. [David Francos]

  With the new airmon-ng and airodump-ng APIs with async context managers,
  proper properties for results and interfaces and callable objects, the
  "simplified" interface that exposed the Pyrcrack class is no longer
  needed.

  Usage is more comprehensive now, and cleanup afterwards should work.
  Altough examples seem to not wait for __aexit__ to cleanup (thus
  airmon-ng's created interface would prevail) upon KeyboardInterrupt.

  Might be caused by https://bugs.python.org/issue29988 wich relates to
  bpo-29988 ( https://github.com/python/cpython/pull/18334 )
- Improved airmon-ng API to look like airodump's. [David Francos]
- PEP-8 fixes. [David Francos]
- Removed print from airodump. [David Francos]
- Removed debug mode on logs by default. [David Francos]
- Added new example using Pyrcrack simplified api. [David Francos]
- Fixed access_points shortcut on Pyrcrack class. [David Francos]
- Moved async iterator logic to main executor class. [David Francos]
- Fixed airmon-ng monitor mode parsing for 1.6. [David Francos]
- Updated examples. [David Francos]
- Feature/16 (#17) [David Francos]

  * wip: #16 Aircrack-ng 1.6 and new AirodumpNG API

  This introduces the changes stated in #16.
  A new async iterator for airodump-ng class, uses netxml files, detects
  process finish and issues trying to launch the current command (and
  reports the issues wich didn't before, as stated in #8
- Closes: #16 Fixed tests. [David Francos]

  Lowered test coverage for the moment.
- Wip: #16 Migrated to aircrack-ng. [David Francos]
- Wip: #16 Aircrack-ng 1.6 and new AirodumpNG API. [David Francos]

  This introduces the changes stated in #16.
  A new async iterator for airodump-ng class, uses netxml files, detects
  process finish and issues trying to launch the current command (and
  reports the issues wich didn't before, as stated in #8
- Closes: #13 Fixed readme install instructions. [David Francos]
- Fixed image position on readme. [David Francos]
- Fixed image position on readme. [David Francos]
- Merge tag '1.0.2' into develop. [David Francos]

  1.0.2
- Fixed image position on readme. [David Francos]


1.0.2 (2020-09-23)
------------------
- Merge branch 'release/1.0.2' [David Francos]
- Version bump to 1.0.2. [David Francos]
- Merge tag '1.0.1' into develop. [David Francos]

  1.0.1
- Fixed prev release name. [David Francos]


1.0.1 (2020-09-23)
------------------
- Merge branch 'release/1.0.1' [David Francos]
- Version bump to 1.0.1. [David Francos]
- Fixed twine not passing checks. [David Francos]


1.0.0 (2020-09-23)
------------------

Fix
~~~
- [#10] Using codecov badge. [David Francos]
- [#10] Migrating to codecov. [David Francos]

Other
~~~~~
- Trying to get gitchangelog to get release info. [David Francos]
- Last try on release for today. [David Francos]
- Feat: closes: #11 Added pypi to github flow. [David Francos]
- Merge branch 'master' into develop. [David Francos]
- Added build step. [David Francos]
- Fixed release build. [David Francos]
- Merge tag '1.0.0' into develop. [David Francos]

  1.0.0
- Merge branch 'release/1.0.0' [David Francos]
- Version bump to 1.0.0. [David Francos]
- Fixed coveralls. [David Francos]
- Re-added coveralls and updated readme. [David Francos]
- Chore: [#9] Fixed workflows. [David Francos]
- Feature/9 (#10) [David Francos, David Francos]

  * chore: [#9] Fixed badges, build and readme

  - Added new badges to readme, fixed examples and PEP-8 and improved readme
  itself with markdown.
  - Updated python to 3.8
  - Added experimental GH workflows
  - Added base docs
  - Added experimental new workflows
  - Moved directory structure around, removed coveragerc, updated readthedocs config
- PEP-8. [David Francos]
- Version bump. [David Francos]
- Added result helper for aireplay. [David Francos]
- Version bump. [David Francos]
- Updated to poetry. [David Francos]
- Merge pull request #7 from XayOn/develop. [David Francos]

  Fixed setup.py
- Fixed setup.py. [David Francos]
- Added more tests. [David Francos]
- Trying deadsnakes ppa, travis still has problems with 3.7... [David
  Francos]
- Fixed travis. [David Francos]


0.1.2 (2018-10-13)
------------------
- Merge branch 'develop' of https://github.com/XayOn/pyrcrack into
  develop. [David Francos]
- Added documentation. [David Francos]
- Fixing readthedocs. [David Francos]
- Added most aircrack-ng suite commands. [David Francos]

  - Airbase
  - Airdecap
  - Airdecloack
  - Aireplay
  - Airmon-ng and Airmon-zc
- Compatibility with all versions won't be a thing, sorry. [David
  Francos]
- Updated readme. [David Francos]
- Added working ExecutorHelper and AircrackNg class. [David Francos]

  Added a base working executor helper with 100% code coverage that would
  construct a command class based on its output.

  If customization is required (i.e the command does not follow docopt
  specifications) you can subclass ExecutorHelper and append a custom
  docstring to the class.
- Only python3.6 supported right now. [David Francos]
- Added fixmes to pyrcrack main lib and updated readme. [David Francos]

  There's two major blocking problems with the docopt-based
  runner right now.
- Added some base tests. [David Francos]
- Added pipenv to travis. [David Francos]
- Fixed readme. [David Francos]
- Merge branch 'master' into develop. [David Francos]
- Initial commit. [David Francos]
- Initial commit. [David Francos Cuartero]
- Initial commit. [David Francos Cuartero]
- Added a few more utilities and examples. [David Francos]
- Fixed TOX. [David Francos]
- Added score. [David Francos]
- Merge branch 'master' of https://github.com/XayOn/pyrcrack. [David
  Francos]
- Updated readme. [David Francos]
- Added asynchronous result updater for airodump-ng. [David Francos]
- Added client list to AP automatically. [David Francos]
- Added models. [David Francos]
- Added scan example. [David Francos]
- Updated to aircrack-ng 1.3. [David Francos]
- Updated readme. [David Francos]
- Added asynchronous result updater for airodump-ng. [David Francos]
- Removed sync code. Everything is a coroutine now. [David Francos]
- Added airodump. [David Francos]
- Fixed tests. [David Francos]
- Removed unneded tempfile import. [David Francos]
- New API for async and sync requests, added context managers. [David
  Francos]
- Added documentation. [David Francos]
- Fixing readthedocs. [David Francos]
- Added most aircrack-ng suite commands. [David Francos]

  - Airbase
  - Airdecap
  - Airdecloack
  - Aireplay
  - Airmon-ng and Airmon-zc
- Compatibility with all versions won't be a thing, sorry. [David
  Francos]
- Updated readme. [David Francos]
- Added working ExecutorHelper and AircrackNg class. [David Francos]

  Added a base working executor helper with 100% code coverage that would
  construct a command class based on its output.

  If customization is required (i.e the command does not follow docopt
  specifications) you can subclass ExecutorHelper and append a custom
  docstring to the class.
- Only python3.6 supported right now. [David Francos]
- Added fixmes to pyrcrack main lib and updated readme. [David Francos]

  There's two major blocking problems with the docopt-based
  runner right now.
- Added some base tests. [David Francos]
- Added pipenv to travis. [David Francos]
- Fixed readme. [David Francos]
- Merge branch 'master' into develop. [David Francos]
- Initial commit. [David Francos]
- Initial commit. [David Francos]
- Initial commit. [David Francos]


0.1.1 (2016-01-20)
------------------
- Merge branch 'release/0.1.1' [David Francos Cuartero]
- Setup and history. [David Francos Cuartero]
- Improved readme. [David Francos Cuartero]
- Marked as todo remaining ones. [David Francos Cuartero]
- Airmon and airdecap docs. [David Francos Cuartero]
- Added wesside-ng docs. [David Francos Cuartero]
- Improved aircrack-ng docs. [David Francos Cuartero]
- Added moduleinfo. [David Francos Cuartero]
- Documented aircrack-ng class. [David Francos Cuartero]
- Merge tag '0.1.0' into develop. [David Francos Cuartero]

  v0.1.0


0.1.0 (2016-01-19)
------------------
- Merge branch 'release/0.1.0' [David Francos Cuartero]
- Setup and history. [David Francos Cuartero]
- Added wesside-ng. [David Francos Cuartero]
- Added airdecap-ng. [David Francos Cuartero]
- Implemented aircrack-ng. [David Francos Cuartero]
- Moved ctx to parent. [David Francos Cuartero]
- Added aireplay-ng (quite basic, not yet parsing output for anything)
  [David Francos Cuartero]
- Removed py35 toxenv. [David Francos Cuartero]
- Even empty tests where failing. [David Francos Cuartero]
- Nopy3.5 on travis seems. [David Francos Cuartero]
- Version stuff. [David Francos Cuartero]
- The template added literal ' there =P. [David Francos Cuartero]
- The template added literal ' there =P. [David Francos Cuartero]
- Psutil requirement. [David Francos Cuartero]
- Made csv parsing more clear. [David Francos Cuartero]
- Replaced aps for a tree. [David Francos Cuartero]
- Small fixes. [David Francos Cuartero]
- Improved documentation. [David Francos Cuartero]
- Fixed argument handling. [David Francos Cuartero]
- Sleeping first. [David Francos Cuartero]
- Fix. [David Francos Cuartero]
- Initial commit. [David Francos Cuartero]


