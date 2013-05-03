timeparse
==========

A python-module to parse strings to time-, date-, datetime- or timedelta-objects.
Which formats are accepted is configurable. The module also provides classes to
use with the argparse-module for parsing command-line arguments.

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

    >>> import timeparse
    >>>
    >>> timeparse.parsedate('24.4.13')
    datetime.date(2013, 4, 24)
    >>>
    >>> timeparse.parsedate('24 Apr 2013')
    datetime.date(2013, 4, 24)
    >>>
    >>> timeparse.parsetime('234405')
    datetime.time(23, 44, 5)
    >>>
    >>> timeparse.TimeFormats.config(allow_no_sep=False)
    >>> timeparse.parsetime('234405')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "timeparse.py", line 398, in parsetime
        raise ValueError("couldn't parse %s as time" % string)
    ValueError: couldn't parse 234405 as time
    >>>
    >>> timeparse.parsedatetime('24-04-13_23:44:05')
    datetime.datetime(2013, 4, 24, 23, 44, 5)

or with argparse ::

    >>> import argparse
    >>> from timeparse import ParseDatetime
    >>>
    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--datetime', action=ParseDatetime, nargs='+')
    >>>
    >>> parser.parse_args("--datetime 2.4.2013 23:02".split()).datetime
    datetime.datetime(2013, 4, 2, 23, 2)




Reporting Bugs
--------------
Please report bugs at github issue tracker:
https://github.com/thomst/timeparse/issues


Author
------
thomst <thomaslfuss@gmx.de>
Thomas Leichtfuß

* http://github.com/thomst
