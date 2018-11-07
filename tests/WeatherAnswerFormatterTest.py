import sys
import unittest
from unittest.mock import Mock

sys.path.append('..')
from AnswerFormatters.Weather.AnswerFormatter import AnswerFormatter
from IntentContent.IntentRecord import IntentRecord


class WeatherAnswerFormatterTest(unittest.TestCase):

    def test_ask_weather_taipei(self):
        answer_formatter = AnswerFormatter()
        answer_formatter._query_external_api_json = self._get_mock_query_external_api()

        intent_record = IntentRecord(102, 3)
        intent_record.user_paramenters = {'weather_query_city': '台北'}
        reply_template = '今天{0}的天氣為{1}'
        answer = answer_formatter.formate_answer(intent_record, reply_template)

        self.assertEqual(answer['output'], '今天台北的天氣為晴,溫度為20度,濕度為50度')

    def test_ask_temperature_taipei(self):
        answer_formatter = AnswerFormatter()
        answer_formatter._query_external_api_json = self._get_mock_query_external_api()

        intent_record = IntentRecord(103, 3)
        intent_record.user_paramenters = {'weather_query_city': '台北'}
        reply_template = '今天{0}的溫度為{1}度'
        answer = answer_formatter.formate_answer(intent_record, reply_template)

        self.assertEqual(answer['output'], '今天台北的天氣為晴,溫度為20度,濕度為50度')

    def test_ask_humidity_taipei(self):
        answer_formatter = AnswerFormatter()
        answer_formatter._query_external_api_json = self._get_mock_query_external_api()

        intent_record = IntentRecord(104, 3)
        intent_record.user_paramenters = {'weather_query_city': '台北'}
        reply_template = '今天{0}的濕度為{1}%'
        answer = answer_formatter.formate_answer(intent_record, reply_template)

        self.assertEqual(answer['output'], '今天台北的天氣為晴,溫度為20度,濕度為50度')

    def _get_mock_query_external_api(self):
        mock_obj = Mock(
            return_value={"data": {"robot_say": "今天台北的天氣為晴,溫度為20度,濕度為50度"}})
        return mock_obj


if __name__ == '__main__':
    unittest.main()
