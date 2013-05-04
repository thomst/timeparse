import unittest
import datetime
import timeparse
import argparse

from argparse import ArgumentError



class ParserTests(unittest.TestCase):
    def test_type(self):
        self.assertIsInstance(timeparse.parsetime('23:44'), datetime.time)
        self.assertIsInstance(timeparse.parsedate('24.3.2013'), datetime.date)
        self.assertIsInstance(timeparse.parsedatetime('24.3.2013,23:44'), datetime.datetime)
        self.assertIsInstance(timeparse.parsetimedelta('24.3.2013,23:44'), datetime.timedelta)

    def test_exceptions(self):
        self.assertRaises(ValueError, timeparse.parsetime, '23;44')
        self.assertRaises(ValueError, timeparse.parsedate, '2013-4.24')
        self.assertRaises(ValueError, timeparse.parsedatetime, '13.04.24#23:44')
        self.assertRaises(ValueError, timeparse.parsetime, str())
        self.assertRaises(TypeError, timeparse.parsedate, None)
        self.assertRaises(TypeError, timeparse.parsedatetime, None)
        self.assertRaises(TypeError, timeparse.parsetimedelta, None)
        timeparse.TimeFormats.config(allow_no_sep=False)
        self.assertRaises(ValueError, timeparse.parsetime, '2344')
        timeparse.DateFormats.config(allow_month_name=False)
        self.assertRaises(ValueError, timeparse.parsedate, '24 Apr 2013')

    def test_parsetime(self):
        parser = timeparse.parsetime
        time = datetime.time
        self.assertEqual(parser('2344'), time(23,44))

    def test_parsedate(self):
        parser = timeparse.parsedate
        date = datetime.date
        timeparse.TimeFormats.config(allow_no_sep=True)
        timeparse.DateFormats.config(allow_month_name=True)

        self.assertEqual(parser('24032013'), date(2013,3,24))
        self.assertEqual(parser('24 Apr 2013'), date(2013,4,24))

        today = date.today()
        self.assertEqual(parser('2403'), date(today.year, 3, 24))
        self.assertEqual(parser('24'), date(today.year, today.month, 24))
        self.assertEqual(parser('243'), date(today.year, 3, 24))

        today = date(1, 2, 3)
        self.assertEqual(parser('2403', today=today), date(today.year, 3, 24))
        self.assertEqual(parser('24', today=today), date(today.year, today.month, 24))
        self.assertEqual(parser('243', today=today), date(today.year, 3, 24))

    def test_parsedatetime(self):
        parser = timeparse.parsedatetime
        dtime = datetime.datetime
        self.assertEqual(parser('24.3.2013,23:44'), dtime(2013,3,24,23,44))

    def test_parsetimedelta(self):
        parser = timeparse.parsetimedelta
        delta = datetime.timedelta
        self.assertEqual(parser('w3 h4 s20'), delta(weeks=3, hours=4, seconds=20))
        self.assertEqual(parser('w3 h4 s20', 'min'), delta(weeks=3, hours=4, seconds=20))
        self.assertEqual(parser('1,2,3', 'H'), delta(hours=1, minutes=2, seconds=3))
        self.assertEqual(parser('1 2 3', 'delta-hours'), delta(hours=1, minutes=2, seconds=3))
        self.assertRaises(ValueError, parser, '20h 0s 4')


class TestTimeParser(unittest.TestCase):
    def setUp(self):
        self.parser = argparse.ArgumentParser()

    def test_ParseTimedelta(self):
        self.parser.add_argument(
            '--weeks',
            action=timeparse.ParseTimedelta,
            nargs='+',
            )
        self.assertEqual(datetime.timedelta(weeks=-20, hours=-4), self.parser.parse_args('--weeks -20 0 -4'.split()).weeks)
        self.assertRaises(SystemExit, self.parser.parse_args, ('--weeks 20h 10 4'.split()))

    def test_ParseTime(self):
        self.parser.add_argument(
            '--time',
            action=timeparse.ParseTime,
            nargs='+',
            )
        self.assertEqual(datetime.time(10, 45, 22), self.parser.parse_args('--time 104522'.split()).time)

    def test_ParseDate(self):
        self.parser.add_argument(
            '--date',
            action=timeparse.ParseDate,
            )
        today = timeparse.TODAY
        self.assertEqual(datetime.date(today.year, today.month, 23), self.parser.parse_args('--date 23'.split()).date)
        self.assertEqual(datetime.date(2013, 4, 22), self.parser.parse_args('--date 22.4.13'.split()).date)
        self.assertEqual(datetime.date(2013, 4, 22), self.parser.parse_args('--date 220413'.split()).date)
        self.assertEqual(datetime.date(2013, 4, 22), self.parser.parse_args('--date 22042013'.split()).date)

    def test_ParseDatetime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.ParseDatetime,
            nargs='+',
            )
        self.assertEqual(
            datetime.datetime(2013, 4, 22, 22, 3, 16),
            self.parser.parse_args('--datetime 22.4 220316'.split()).datetime
            )

    def test_ParseTimeOrDatetime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.ParseTimeOrDatetime,
            nargs='+',
            )
        self.assertEqual(
            datetime.datetime(2013, 4, 22, 22, 3, 16),
            self.parser.parse_args('--datetime 22.4 220316'.split()).datetime
            )
        self.assertEqual(
            datetime.time(22, 3, 16),
            self.parser.parse_args('--datetime 220316'.split()).datetime
            )

    def test_AppendTimeOrDatetime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.AppendTimeOrDatetime,
            nargs='+',
            )
        self.assertEqual(
            [datetime.time(22, 3, 16), datetime.time(13, 3)],
            self.parser.parse_args('--datetime 220316 --datetime 1303'.split()).datetime
            )

    def test_ParseTimeDelta(self):
        self.parser.add_argument(
            '--weeks',
            action=timeparse.ParseTimeDelta,
            nargs='+',
            )
        self.assertRaises(DeprecationWarning, self.parser.parse_args, ('--weeks -20 0 -4'.split()))

    def test_ParseDateTime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.ParseDateTime,
            nargs='+',
            )
        self.assertRaises(DeprecationWarning, self.parser.parse_args, ('--datetime 22.4 220316'.split()))

    def test_ParseDateTimeOrTime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.ParseDateTimeOrTime,
            nargs='+',
            )
        self.assertRaises(DeprecationWarning, self.parser.parse_args, ('--datetime 22.4 220316'.split()))

    def test_AppendDateTimeOrTime(self):
        self.parser.add_argument(
            '--datetime',
            action=timeparse.AppendDateTimeOrTime,
            nargs='+',
            )
        self.assertRaises(DeprecationWarning, self.parser.parse_args, ('--datetime 220316 --datetime 1303'.split()))


if __name__ == '__main__':
    unittest.main()
