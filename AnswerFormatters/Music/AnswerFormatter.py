import urllib


from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    QUERY_MUSIC_BY_TYPE_PARTIAL_URI = r'kkboxSearchAlbumByCategories?query={0}&access_token={1}'
    QUERY_MUSIC_BY_SINGER_OR_SONG_PARTIAL_URI = r'kkboxSearchByAlbum?query={0}&access_token={1}'
    ERROR_RESULT = 'category is not exist'
    ERROR_MUSIC_NOT_EXIST = '沒有該音樂的資訊'

    def formate_answer(self, intent_record, reply_template):
        """
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -string

        Return: dict
        """
        intent_id = intent_record.intent_id
        parameters = intent_record.user_paramenters
        action_dic = {}
        
        if intent_id == 1301:
            query_uri = self._internal_service_uri_base + self.QUERY_MUSIC_BY_TYPE_PARTIAL_URI
            query_uri = query_uri.format(
                urllib.parse.quote(parameters['music_type']),
                self._internal_service_token
            )
        elif intent_id == 1302:
            query_uri = self._internal_service_uri_base + self.QUERY_MUSIC_BY_SINGER_OR_SONG_PARTIAL_URI
            query_uri = query_uri.format(
                urllib.parse.quote(parameters['singer']),
                self._internal_service_token
            )
        elif intent_id == 1303:
            query_uri = self._internal_service_uri_base + self.QUERY_MUSIC_BY_SINGER_OR_SONG_PARTIAL_URI
            query_uri = query_uri.format(
                urllib.parse.quote(parameters['song']),
                self._internal_service_token
            )

        reply, action_dic = self._query_music_infomation(query_uri)

        reply_dic = self._formate_to_dict(reply, action_dic)
        return reply_dic

    def _query_music_infomation(self, query_uri):
        query_result = self._query_external_api_json(query_uri)

        if query_result['data'] == self.ERROR_RESULT or not query_result['data']['playList']:
            return self.ERROR_MUSIC_NOT_EXIST, {}
        action_dic = {'action': '"kkbox_play', 'track_ids': query_result['data']['playList']}
        return query_result['data']['robot_say'], action_dic
