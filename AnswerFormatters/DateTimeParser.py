import datetime
import re


class DateTimeParser:
    WEEKDAY_NUMBER_MAPPING = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '末': 6, '日': 7, '天': 7
    }
    WEEK_DAY_REX_OBJ = re.compile('(下{0,3})(禮拜|星期|週|周)([一二三四五六日天末])')

    def parse(self, date_time_string):
        def date_time_string_normalization(date_time_string):
            return date_time_string

        def parse_date(date_time_string, out_put_date_time):
            if '禮拜' in date_time_string or '星期' in date_time_string or '週' in date_time_string:
                out_put_date_time = parse_week_day(
                    date_time_string, out_put_date_time)
            else:
                out_put_date_time = parse_relative_day(
                    date_time_string, out_put_date_time)
            return out_put_date_time

        def parse_week_day(date_time_string, precessed_date_time):
            search_result = self.WEEK_DAY_REX_OBJ.search(date_time_string)
            if search_result:
                next_week_count = len(search_result[1])
                week_day_number = self.WEEKDAY_NUMBER_MAPPING[search_result[3]]
                day_shift = week_day_number - precessed_date_time.weekday() - 1
                day_shift += 7*next_week_count
                precessed_date_time += datetime.timedelta(days=day_shift)
            return precessed_date_time

        def parse_relative_day(date_time_string, out_put_date_time):
            if '昨' in date_time_string:
                out_put_date_time -= datetime.timedelta(days=1)
            elif '明' in date_time_string or '隔天' in date_time_string:
                out_put_date_time += datetime.timedelta(days=1)
            elif '大前' in date_time_string:
                out_put_date_time -= datetime.timedelta(days=3)
            elif '前' in date_time_string:
                out_put_date_time -= datetime.timedelta(days=2)
            elif '大後' in date_time_string:
                out_put_date_time += datetime.timedelta(days=3)
            elif '後' in date_time_string:
                out_put_date_time += datetime.timedelta(days=2)
            return out_put_date_time

        date_time_string = date_time_string_normalization(date_time_string)
        out_put_date_time = datetime.datetime.now()
        out_put_date_time = parse_date(date_time_string, out_put_date_time)

        return out_put_date_time
