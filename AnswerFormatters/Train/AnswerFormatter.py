import json
import urllib
import urllib.request
import datetime
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    TRAIN_QUERY_PARTIAL_URI = r'trainSearch?origin_station_name={0}&destination_station_name={1}&search_date={2}&access_token={3}'
    ERROR_TRAIN_NOT_EXIST = '查無此時間之班次資訊'
    API_QUERY_DATE_TIME_FORMATE = '{0}+08:00'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -- string contains {0}~{7}

        Return: dict
        """
        intent_id = intent_record.intent_id
        answer = reply_template

        if intent_id == 601:
            normalized_date_time = self._normalize_date_time(
                intent_record.user_paramenters['departure_date'], intent_record.user_paramenters['departure_time'])
            answer = self._query_train(
                reply_template, intent_record.user_paramenters, normalized_date_time)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_train(self, reply, user_paramenters, normalized_date_time):
        query_uri = self._internal_service_uri_base + self.TRAIN_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            urllib.parse.quote(user_paramenters['departure_station']),
            urllib.parse.quote(user_paramenters['arrive_station']),
            urllib.parse.quote(normalized_date_time),
            self._internal_service_token,
        )
        query_result = self._query_external_api_json(query_uri)

        if 'data' not in query_result or 'robot_say' not in query_result['data']:
            return self.ERROR_TRAIN_NOT_EXIST

        reply = query_result['data']['robot_say']

        return reply

    def _normalize_date_time(self, date, time):
        normalized_date_time = self.API_QUERY_DATE_TIME_FORMATE.format(
            datetime.datetime.now().isoformat())
        return normalized_date_time