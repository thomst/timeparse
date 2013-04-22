timeparse
=========

timeparse is an extension for argparse. It parses commandline-arguments as time-, datetime-, date- or timedelta-objects of the datetime-module. Just use his classes as action-parameter for the add_argument-method of an argument-parser.


Latest Version
--------------
The latest version of this project can be found at : http://github.com/thomst/timeparse.


Installation
------------
* Option 1 : Install via pip ::

    pip install timeparse

* Option 2 : If you have downloaded the source ::

    python setup.py install


Documentation
-------------
How to use? ::

    import argparse
    from timeparse import ParseDateTime

    parser = argparse.ArgumentParser()
    parser.add_argument('--datetime', action=ParseDateTime, nargs='+')

    parser.parse_args("--datetime 2.4.2013 23:02".split()).datetime
    #this is what you get: datetime.datetime(2013, 4, 2, 23, 2)


Reporting Bugs
--------------
Please report bugs at github issue tracker:
https://github.com/thomst/timeparse/issues


Author
------
thomst <thomaslfuss@gmx.de>
Thomas Leichtfuß

* http://github.com/thomst
