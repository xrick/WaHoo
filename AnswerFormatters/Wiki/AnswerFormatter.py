import json
import urllib
import urllib.request
import datetime
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    WIKI_APU_QUERY_PARTIAL_URI = r'wikiSearch?input={0}&access_token={1}'
    ERROR_KNOWLEDGE_NOT_EXIST = '查無此關鍵字資訊'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -None

        Return: String
        """
        intent_id = intent_record.intent_id
        answer = reply_template
        if intent_id == 801:
            answer = self._query_wiki_information(intent_record.user_paramenters, reply_template)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_wiki_information(self, user_paramenters, reply_template):
        query_uri = self._internal_service_uri_base + self.WIKI_APU_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            urllib.parse.quote(user_paramenters['search_keyword']),
            self._internal_service_token,
        )
        query_result = self._query_external_api_json(query_uri)

        if not query_result['data']:
            return self.ERROR_KNOWLEDGE_NOT_EXIST

        reply = query_result['data']

        return reply