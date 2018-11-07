import datetime
import sys
import unittest
from unittest.mock import Mock

sys.path.append('.')
from AnswerFormatters.DateTimeParser import DateTimeParser


class DateTimeParserTest(unittest.TestCase):

    def test_parse_today(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('今天')
        assert_date = datetime.datetime.today()
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_yesterday(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('昨天')
        assert_date = datetime.datetime.today() - datetime.timedelta(days=1)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_the_day_before_yesterday(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('前天')
        assert_date = datetime.datetime.today() - datetime.timedelta(days=2)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_three_days_ago(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('大前天')
        assert_date = datetime.datetime.today() - datetime.timedelta(days=3)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_tomorrow(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('明天')
        assert_date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_tomorrow_synonym(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('隔天')
        assert_date = datetime.datetime.today() + datetime.timedelta(days=1)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_the_day_after_tomorrow(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('後天')
        assert_date = datetime.datetime.today() + datetime.timedelta(days=2)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_3_day_after(self):
        datetime_parser = DateTimeParser()
        result = datetime_parser.parse('大後天')
        assert_date = datetime.datetime.today() + datetime.timedelta(days=3)
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_week_day(self):
        datetime_parser = DateTimeParser()
        today_weekday = datetime.datetime.today().weekday()
        assert_date = datetime.datetime.today() + datetime.timedelta(days=-today_weekday)
        result = datetime_parser.parse('星期一')
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_week_day_synonym(self):
        datetime_parser = DateTimeParser()
        today_weekday = datetime.datetime.today().weekday()
        assert_date = datetime.datetime.today() + datetime.timedelta(days=-today_weekday)
        result = datetime_parser.parse('週一')
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_week_day_synonym2(self):
        datetime_parser = DateTimeParser()
        today_weekday = datetime.datetime.today().weekday()
        assert_date = datetime.datetime.today() + datetime.timedelta(days=-today_weekday)
        result = datetime_parser.parse('禮拜一')
        self.assertEqual(result.date(), assert_date.date())

    def test_parse_next_week_day(self):
        datetime_parser = DateTimeParser()
        today_weekday = datetime.datetime.today().weekday()
        assert_date = datetime.datetime.today() + datetime.timedelta(days=-today_weekday+7)
        result = datetime_parser.parse('下星期一')
        self.assertEqual(result.date(), assert_date.date())


if __name__ == '__main__':
    unittest.main()
