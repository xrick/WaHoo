import urllib.request
import urllib
import xml.etree.ElementTree as ET
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    NEWS_QUERY_URI = r'https://news.google.com/news/rss/?hl=zh-tw&gl=TW&ned=zh-tw_tw'
    SPECIFIED_TYPE_NEWS_QUERY_URI = r'https://news.google.com/news/rss/headlines/section/topic/{0}?ned=zh-tw_tw&hl=zh-tw&gl=TW'
    NEWS_QUERY_URI_WITH_KEYWORD = r'https://news.google.com/news/rss/search/section/q/{0}/{0}?hl=zh-tw&gl=TW&ned=zh-tw_tw'
    MAX_TITLE_DISPLAY = 10
    TITLE_head = '第{0}則:'
    TITLE_TAIL = '.'
    NEWS_TYPE_CH_EN_MAPPING = {
        "地方": "local",
        "世界": "WORLD",
        "國際": "WORLD",
        "台灣": "NATION",
        "經濟": "BUSINESS",
        "財經": "BUSINESS",
        "娛樂": "ENTERTAINMENT",
        "運動": "SPORTS",
        "體育": "SPORTS",
        "健康": "HEALTH"
    }

    def formate_answer(self, intent_record, reply_template):
        intent_id = intent_record.intent_id
        answer = reply_template
        if intent_id == 300:
            answer = self._query_news(reply_template, intent_record.user_paramenters)
        elif intent_id == 301:
            answer = self._query_news_with_keyword(
                reply_template, intent_record.user_paramenters)

        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic

    def _query_news_with_keyword(self, reply, user_paramenters):
        keyword = user_paramenters['search_keyword']
        keyword_unicode = urllib.parse.quote(keyword)
        uri = self.NEWS_QUERY_URI_WITH_KEYWORD.format(keyword_unicode)
        ordinal_titles_string = self._get_news_title_string(uri)
        return reply.format(keyword, ordinal_titles_string)

    def _query_news(self, reply, user_paramenters):
        news_type = user_paramenters['news_type']
        if news_type in self.NEWS_TYPE_CH_EN_MAPPING:
            uri = self.SPECIFIED_TYPE_NEWS_QUERY_URI.format(
                self.NEWS_TYPE_CH_EN_MAPPING[news_type])
        else:
            uri = self.NEWS_QUERY_URI
        ordinal_titles_string = self._get_news_title_string(uri)
        return reply.format(news_type, ordinal_titles_string)

    def _get_news_title_string(self, uri):
        def normalize_titles_to_ordinal_titles():
            ordinal_titles = []
            for i, title in enumerate(titles):
                if i == self.MAX_TITLE_DISPLAY:
                    break
                ordinal_titles.append(self.TITLE_head.format(
                    i+1) + title + self.TITLE_TAIL)

            return ''.join(ordinal_titles)

        titles = self._query_external_api_and_parse_titles(uri)
        ordinal_titles_string = normalize_titles_to_ordinal_titles()
        return ordinal_titles_string

    def _query_external_api_and_parse_titles(self, uri):
        contents = self._query_external_api(uri)
        contents = ET.fromstring(contents)
        titles = []
        for item in contents.iter('item'):
            titles.append(item.find('title').text)

        return titles
