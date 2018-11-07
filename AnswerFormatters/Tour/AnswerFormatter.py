import urllib
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    TOUR_QUERY_PARTIAL_URI = r'tourismSearch?city={0}&query_type={1}&access_token={2}'
    TYPE_SPOT = 'ScenicSpot'
    TYPE_RESTAURANT = 'Restaurant'
    ERROR_INFOMATION_NOT_EXIST = '無該城市資訊'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -- None

        Return: dict
        """
        intent_id = intent_record.intent_id
        answer = reply_template
        if intent_id == 1401:
            query_uri = self._internal_service_uri_base + self.TOUR_QUERY_PARTIAL_URI
            query_uri = query_uri.format(
                urllib.parse.quote(intent_record.user_paramenters['tour_query_city'][:2]),
                self.TYPE_SPOT,
                self._internal_service_token
            )
            answer = self._query_tour_infomation(query_uri)
        elif intent_id == 1402:
            query_uri = self._internal_service_uri_base + self.TOUR_QUERY_PARTIAL_URI
            query_uri = query_uri.format(
                urllib.parse.quote(intent_record.user_paramenters['tour_query_city'][:2]),
                self.TYPE_RESTAURANT,
                self._internal_service_token
            )
            answer = self._query_tour_infomation(query_uri)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_tour_infomation(self, query_uri):
        query_result = self._query_external_api_json(query_uri)

        if not query_result['data']:
            return self.ERROR_INFOMATION_NOT_EXIST

        reply = query_result['data'][0]['robot_say']

        return reply
