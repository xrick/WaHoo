import json
import urllib
import urllib.request
import datetime
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    ORIGIN = '台北車站'
    NAVIGATION_API_QUERY_PARTIAL_URI = r'googleDirection?origin={0}&destination={1}&access_token={2}'
    ERROR_NAVIGATION_NOT_EXIST = '查無此路線資訊'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -None

        Return: dict
        """
        intent_id = intent_record.intent_id
        answer = reply_template
        if intent_id == 1001:
            answer = self._query_navigation_information(intent_record.user_paramenters, reply_template)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_navigation_information(self, user_paramenters, reply_template):
        query_uri = self._internal_service_uri_base + self.NAVIGATION_API_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            urllib.parse.quote(self.ORIGIN),
            urllib.parse.quote(user_paramenters['destination']),
            self._internal_service_token,
        )
        query_result = self._query_external_api_json(query_uri)

        if not query_result['data'] or 'robot_say' not in query_result['data']:
            return self.ERROR_NAVIGATION_NOT_EXIST

        reply = query_result['data']['robot_say']

        return reply
