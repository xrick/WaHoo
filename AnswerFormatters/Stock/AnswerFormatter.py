import json
import urllib
import urllib.request
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    STOCK_PRICE_QUERY_PARTIAL_URI = r'realTimeFinance?stock_name={0}&access_token={1}'
    STOCK_NO_QUERY_PARTIAL_URI = r'getStockNameOrNum?name={0}&access_token={1}'
    STOCK_NAME_QUERY_PARTIAL_URI = r'getStockNameOrNum?number={0}&access_token={1}'

    ERROR_STOCK_NOT_EXIST = '查無此股票資訊'
    API_QUERY_ERROR_MESSAGE = 'The Stock is not exist'

    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -- string contains {0},{1},etc.
        Return: dict
        """
        intent_id = intent_record.intent_id
        answer = reply_template

        if intent_id == 501:
            answer = self._query_stock_price(
                reply_template, intent_record.user_paramenters)
        elif intent_id == 502:
            answer = self._query_stock_no_by_name(
                reply_template, intent_record.user_paramenters)
        elif intent_id == 503:
            answer = self._query_stock_name_by_no(
                reply_template, intent_record.user_paramenters)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_stock_price(self, reply, user_paramenters):
        query_uri = self._internal_service_uri_base + self.STOCK_PRICE_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            self._encode_with_unicode(user_paramenters['target_stock']),
            self._internal_service_token
        )
        query_result = self._query_external_api_json(query_uri)

        if query_result['data'] == self.API_QUERY_ERROR_MESSAGE:
            return self.ERROR_STOCK_NOT_EXIST

        reply = reply.format(
            user_paramenters['target_stock'],
            query_result['data']['current_price'],
            query_result['data']['time']
        )

        return reply

    def _query_stock_no_by_name(self, reply, user_paramenters):
        query_uri = self._internal_service_uri_base + self.STOCK_NO_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            self._encode_with_unicode(user_paramenters['target_stock_name']),
            self._internal_service_token
        )
        query_result = self._query_external_api_json(query_uri)

        if query_result['data'] == self.API_QUERY_ERROR_MESSAGE:
            return self.ERROR_STOCK_NOT_EXIST

        reply = reply.format(
            user_paramenters['target_stock_name'],
            query_result['data']
        )

        return reply

    def _query_stock_name_by_no(self, reply, user_paramenters):
        query_uri = self._internal_service_uri_base + self.STOCK_NAME_QUERY_PARTIAL_URI
        query_uri = query_uri.format(
            self._encode_with_unicode(user_paramenters['target_stock_no']),
            self._internal_service_token
        )
        query_result = self._query_external_api_json(query_uri)

        if query_result['data'] == self.API_QUERY_ERROR_MESSAGE:
            return self.ERROR_STOCK_NOT_EXIST

        reply = reply.format(
            user_paramenters['target_stock_no'],
            query_result['data']
        )

        return reply

    def _encode_with_unicode(self, string):
        return urllib.parse.quote(string)


if __name__ == "__main__":
    class IntentRecord:
        def __init__(self, intent_id, para):
            self.intent_id = intent_id
            self.user_paramenters = para

    test_obj = AnswerFormatter()
    test_intent_record = IntentRecord(501, {'stock_name_no': '1234'})
    result = test_obj.formate_answer(
        test_intent_record, '目前{0}股價為{1},此為{2}的資料')
    test_intent_record = IntentRecord(503, {'stock_no': '1234'})
    result3 = test_obj.formate_answer(test_intent_record, '{0}的股票名稱為{1}')
    test_intent_record = IntentRecord(502, {'stock_name': '台積電'})
    result2 = test_obj.formate_answer(test_intent_record, '{0}的股票代號為{1}')
