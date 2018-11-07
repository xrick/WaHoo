import json
import urllib
import urllib.request
import datetime
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    INFO_TYPE_MEDICINE = 'medicine'
    KINGNET_QUERY_PARTIAL_URI = r'queryKnInfo?keyword={0}&info_type={1}&access_token={2}'
    ERROR_MEDICINE_NOT_EXIST = '查無此藥品資訊'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -{0}:{1}

        Return: dict
        """
        intent_id = intent_record.intent_id
        answer = reply_template
        if intent_id == 701:
            answer = self._query_medecine_information(intent_record.user_paramenters, reply_template)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_medecine_information(self, user_paramenters, reply_template):
        query_uri = self._internal_service_uri_base + self.KINGNET_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            urllib.parse.quote(user_paramenters['medicine_name']),
            self.INFO_TYPE_MEDICINE,
            self._internal_service_token,
        )
        query_result = self._query_external_api_json(query_uri)

        if not query_result['data']:
            return self.ERROR_MEDICINE_NOT_EXIST

        first_medicine = query_result['data'][0]

        reply = first_medicine['robot_say']

        return reply