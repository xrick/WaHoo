import json
import urllib.request
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    WEATHER_QUERY_PARTIAL_URI = r'queryWeatherDescription?city={0}&access_token={1}'
    AIR_POLLUTION_QUERY_PARTIAL_URI = r'todayAQI?city={0}&access_token={1}'
    UV_INDEX_QUERY_PARTIAL_URI = r'todayUV?city={0}&access_token={1}'
    ERROR_NO_INFO = '查詢天氣時遇到了一點問題,請稍後在試'
    def formate_answer(self, intent_record, reply_template):
        intent_id = intent_record.intent_id
        answer = reply_template

        if intent_id == 102:
            query_uri = self._internal_service_uri_base + self.WEATHER_QUERY_PARTIAL_URI
            answer = self.query_weather_api(
                answer, intent_record.user_paramenters, query_uri)
        elif intent_id == 103:
            query_uri = self._internal_service_uri_base + self.WEATHER_QUERY_PARTIAL_URI
            answer = self.query_weather_api(
                answer, intent_record.user_paramenters, query_uri)
        elif intent_id == 104:
            query_uri = self._internal_service_uri_base + self.WEATHER_QUERY_PARTIAL_URI
            answer = self.query_weather_api(
                answer, intent_record.user_paramenters, query_uri)
        elif intent_id == 105:
            query_uri = self._internal_service_uri_base + self.AIR_POLLUTION_QUERY_PARTIAL_URI
            answer = self.query_weather_api(
                answer, intent_record.user_paramenters, query_uri)
        elif intent_id == 106:
            query_uri = self._internal_service_uri_base + self.UV_INDEX_QUERY_PARTIAL_URI
            answer = self.query_weather_api(
                answer, intent_record.user_paramenters, query_uri)
        
        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def query_weather_api(self, reply, user_paramenters, query_uri):
        query_uri = query_uri.format(
            urllib.parse.quote(user_paramenters['weather_query_city'][:2]),
            self._internal_service_token,
        )
        query_result = self._query_external_api_json(query_uri)

        if not query_result['data']:
            return self.ERROR_NO_INFO

        reply = query_result['data']['robot_say']

        return reply
