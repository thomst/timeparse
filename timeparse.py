"""
An :mod:`argparse`-extension for parsing command-line arguments as objects of the
:mod:`datetime`-module.
"""
import warnings
import datetime
import re
import subprocess
import shlex
import argparse
import timeparser
from daytime import Daytime

from argparse import ArgumentError

__version__ = '0.5.3'


class TimeArgsMixin:
    ERR = "'%s' couldn't be parsed as %s"

    def combine_datetime(self, datestring, timestring):
        date = timeparser.parsedate(datestring)
        time = timeparser.parsetime(timestring)
        return datetime.datetime.combine(date, time)

    def time_or_datetime(self, values):
        if len(values) == 1: return timeparser.parsetime(values[0])
        elif len(values) == 2: return self.combine_datetime(*values)
        else: raise ValueError("'%s' couldn't be parsed as time or datetime" % values)

    def append(self, namespace, obj):
        if getattr(namespace, self.dest):
            getattr(namespace, self.dest).append(obj)
        else:
            setattr(namespace, self.dest, [obj])



class ParseTime(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters as :class:`datetime.time`.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--time',
        ... action=timeparse.ParseTime
        ... )
        >>> parser.parse_args('--time 23:20:33'.split()).time
        datetime.time(23, 20, 33)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            if type(values) == str: time = timeparser.parsetime(values)
            else: time = [timeparser.parsetime(d) for d in values]
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'time'))
        else: setattr(namespace, self.dest, time)


class ParseDaytime(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters as :class:`datetime.time`.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--daytime',
        ... action=timeparse.ParseDaytime
        ... )
        >>> parser.parse_args('--daytime 23:20:33'.split()).daytime
        Daytime(23, 20, 33)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            if type(values) == str:
                daytime = Daytime.fromtime(timeparser.parsetime(values))
            else:
                daytime = [Daytime.fromtime(timeparser.parsetime(d)) for d in values]
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'daytime'))
        else: setattr(namespace, self.dest, daytime)


class ParseDate(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters as :class:`datetime.date`.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--date',
        ... action=timeparse.ParseDate
        ... )
        >>> parser.parse_args('--date 24/04/2013'.split()).date
        datetime.date(2013, 4, 24)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            if type(values) == str: date = timeparser.parsedate(values)
            else: date = [timeparser.parsedate(d) for d in values]
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'date'))
        else: setattr(namespace, self.dest, date)


class ParseTimedelta(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters as :class:`datetime.timedelta`.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--days',
        ... nargs='+',
        ... action=timeparse.ParseTimedelta
        ... )
        >>> parser.parse_args('--days 20 12 4'.split()).days
        datetime.timedelta(20, 43440)

        >>> parser.parse_args('--days 20h 12m 4s'.split()).days
        datetime.timedelta(0, 72724)

    If the dest-property of argparse.Action (which is by default the literal part
    of the option-string) matches one of the kwargs accepted by
    :class:`datetime.timedelta` the values are interpreted starting with this
    unit with the next lesser unit following.
    If the values could be flagged with some letters matching those kwargs.
    In the first exemple above the values are interpreted as 20 days, 12 hours
    and 4 min. In the second one as 20 hours, 12 minutes and 4 seconds.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        value = ' '.join(values) if isinstance(values, list) else values
        kwords = ('weeks', 'days', 'hours', 'minutes', 'seconds')
        key = map(lambda k: k if re.match(self.dest, k) else 'days', kwords)[0]
        try: timedelta = timeparser.parsetimedelta(value, key)
        except ValueError:
            raise ArgumentError(self, self.ERR % (value, 'timedelta'))
        else: setattr(namespace, self.dest, timedelta)


class ParseDatetime(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters as :class:`datetime.datetime`.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--datetime',
        ... nargs='+',
        ... action=timeparse.ParseDatetime
        ... )
        >>> parser.parse_args('--datetime 24/04/2013 23:22'.split()).datetime
        datetime.datetime(2013, 4, 24, 23, 22)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        values = values if isinstance(values, list) else [values]
        try:
            if len(values) == 2: datetime = self.combine_datetime(*values)
            else: datetime = timeparser.parsedatetime(' '.join(values))
        except ValueError:
            raise ArgumentError(self, self.ERR % (values, 'datetime'))
        else: setattr(namespace, self.dest, datetime)


class ParseTimeOrDatetime(argparse.Action, TimeArgsMixin):
    """
    Action for :meth:`argparse.ArgumentParser.add_argument` to parse
    cmdline-parameters either as :class:`datetime.time` or :class:`datetime.datetime`..

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--time-or-datetime',
        ... nargs='+',
        ... action=timeparse.ParseTimeOrDatetime
        ... )
        >>> parser.parse_args('--time-or-datetime 24/04/2013 23:22'.split()).time_or_datetime
        datetime.datetime(2013, 4, 24, 23, 22)

        >>> parser.parse_args('--time-or-datetime 23:22'.split()).time_or_datetime
        datetime.time(23, 22)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        values = values if isinstance(values, list) else [values]
        try: obj = self.time_or_datetime(values)
        except ValueError:
            raise ArgumentError(self, self.ERR % (values, 'time or datetime'))
        else: setattr(namespace, self.dest, obj)


class AppendTime(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseTime` with support for multiple use of arguments.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--time',
        ... action=timeparse.AppendTime
        ... )
        >>> parser.parse_args('--time 23:20:33 --time 22:20'.split()).time
        [datetime.time(23, 20, 33), datetime.time(22, 20)]
    """
    def __call__(self, parser, namespace, values, option_string=None):
        value = ' '.join(values) if isinstance(values, list) else values
        try: time = timeparser.parsetime(value)
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'time'))
        else: self.append(namespace, time)


class AppendDaytime(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseDaytime` with support for multiple use of arguments.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--daytime',
        ... action=timeparse.AppendDaytime
        ... )
        >>> parser.parse_args('--daytime 23:20:33 --daytime 22:20'.split()).daytime
        [Daytime(23, 20, 33), Daytime(22, 20)]
    """
    def __call__(self, parser, namespace, values, option_string=None):
        value = ' '.join(values) if isinstance(values, list) else values
        try: daytime = Daytime.fromtime(timeparser.parsetime(values))
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'daytime'))
        else: self.append(namespace, daytime)


class AppendDate(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseDate` with support for multiple use of arguments.

    usage:
        >>> import argparse
        >>> import timeparse

        >>> parser = argparse.ArgumentParser(prog='PROG')
        >>> parser.add_argument(
        ... '--date',
        ... action=timeparse.AppendDate
        ... )
        >>> parser.parse_args('--date 23.4.13 --date 24.4.13'.split()).date
        [datetime.date(2013, 4, 23), datetime.date(2013, 4, 24)]
    """
    def __call__(self, parser, namespace, values, option_string=None):
        value = ' '.join(values) if isinstance(values, list) else values
        try: date = timeparser.parsedate(value)
        except ValueError: raise ArgumentError(self, self.ERR % (values, 'date'))
        else: self.append(namespace, date)


class AppendTimedelta(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseTimedelta` with support for multiple use of arguments.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        value = ' '.join(values) if isinstance(values, list) else values
        try: timedelta = timeparser.parsetimedelta(value)
        except ValueError:
            raise ArgumentError(self, self.ERR % (values, 'timedelta'))
        else: self.append(namespace, timedelta)


class AppendDatetime(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseDatetime` with support for multiple use of arguments.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        values = values if isinstance(values, list) else [values]
        try:
            if len(values) == 2: datetime = self.combine_datetime(*values)
            else: datetime = timeparser.parsedatetime(' '.join(values))
        except ValueError:
            raise ArgumentError(self, self.ERR % (values, 'datetime'))
        else: self.append(namespace, datetime)


class AppendTimeOrDatetime(argparse.Action, TimeArgsMixin):
    """
    Like :class:`ParseTimeOrDatetime` with support for multiple use of arguments.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        values = values if isinstance(values, list) else [values]
        try: obj = self.time_or_datetime(values)
        except ValueError:
            raise ArgumentError(self, self.ERR % (values, 'time or datetime'))
        else: self.append(namespace, obj)



