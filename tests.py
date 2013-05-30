import unittest
import datetime
import timeparse
import argparse
import timeparser

from argparse import ArgumentError

timeparser.ENDIAN.set('little')

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
        timeparser.TimeFormats.config(allow_no_sep=False)
        self.assertRaises(SystemExit, self.parser.parse_args, ('--time 104522'.split()))

        timeparser.TimeFormats.config(allow_no_sep=True)
        self.assertEqual(datetime.time(10, 45, 22), self.parser.parse_args('--time 104522'.split()).time)

    def test_ParseDate(self):
        self.parser.add_argument(
            '--date',
            action=timeparse.ParseDate,
            )
        timeparser.TODAY.set(1,2,3)
        today = timeparse.timeparser.TODAY
        self.assertEqual(datetime.date(today.year, today.month, 23), self.parser.parse_args('--date 23'.split()).date)
        timeparser.TODAY.set()

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
            self.parser.parse_args('--datetime 22.4_220316'.split()).datetime
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



if __name__ == '__main__':
    unittest.main()
