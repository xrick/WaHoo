import json
import unittest
from Chatbot.Chatbot import Chatbot


class ChatbotFuncTest(unittest.TestCase):
    NO_ANSWER = '抱歉我不懂你說什麼...'

    def test_air_pollution(self):
        chatbot = Chatbot()
        answer = chatbot.interact('台北市空氣汙染狀況', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:10], '台北的空氣品質指標為')

    def test_UV_Index(self):
        chatbot = Chatbot()
        answer = chatbot.interact('台北的紫外線指數', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:10], '臺北市的紫外線指數為')

    def test_finish_and_escape_domain(self):
        chatbot = Chatbot()
        answer = chatbot.interact('桃園有什麼好玩的', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:7], '老K舒眠文化館')
        answer = chatbot.interact('桃園天氣', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], '桃園市 ')

    def test_weather_specific_city(self):
        chatbot = Chatbot()
        answer = chatbot.interact('桃園天氣', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], '桃園市 ')

    def test_weather_default(self):
        chatbot = Chatbot()
        answer = chatbot.interact('天氣', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], '台北市 ')
    
    def test_weather_default_twice(self):
        chatbot = Chatbot()
        answer = chatbot.interact('天氣', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], '台北市 ')
        answer = chatbot.interact('天氣', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], '台北市 ')

    def test_hospital_multivalue_slot(self):
        chatbot = Chatbot()
        answer = chatbot.interact('醫生', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您有什麼症狀')
        answer = chatbot.interact('頭痛', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您還有什麼症狀')
        answer = chatbot.interact('憂鬱', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '建議您至精神科就診')

    def test_hospital_multivalue_slot_stop(self):
        chatbot = Chatbot()
        answer = chatbot.interact('醫生', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您有什麼症狀')
        answer = chatbot.interact('頭痛', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您還有什麼症狀')
        answer = chatbot.interact('沒有了', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '建議您至家庭醫學科就診')

    def test_hospital_multivalue_slot_one_question(self):
        chatbot = Chatbot()
        answer = chatbot.interact('醫生', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您有什麼症狀')
        answer = chatbot.interact('頭痛和憂鬱', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '建議您至精神科就診')

    def test_news_query_news_default(self):
        chatbot = Chatbot()
        answer = chatbot.interact('新聞', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:15], '以下為您播報焦點新聞:第1則:')

    def test_news_query_news_specified_type(self):
        chatbot = Chatbot()
        answer = chatbot.interact('體育新聞', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:15], '以下為您播報體育新聞:第1則:')

    def test_news_query_news_keyword(self):
        chatbot = Chatbot()
        answer = chatbot.interact('有關周杰倫的新聞', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:19], '以下為您播報周杰倫相關的新聞:第1則:')

    def test_chat_comeback(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我來了', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '你好!')
        answer = chatbot.interact('我走了', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '再見')
        answer = chatbot.interact('我來了', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '你又來了呀')

    def test_chat_empty(self):
        chatbot = Chatbot()
        answer = chatbot.interact('', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, self.NO_ANSWER)

    def test_stock_ask_price(self):
        chatbot = Chatbot()
        answer = chatbot.interact('台積電股價', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:8], '目前台積電股價為')

    def test_stock_ask_stock_no(self):
        chatbot = Chatbot()
        answer = chatbot.interact('台積電的股票代號', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '台積電的股票代號為2330')

    def test_stock_ask_stock_name(self):
        chatbot = Chatbot()
        answer = chatbot.interact('1234是哪支股票', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '1234的股票名稱為黑松')

    def test_stock_ask_price_reset_para_after_done(self):
        chatbot = Chatbot()
        answer = chatbot.interact('問股價', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您想問的股票代號或公司簡稱？')
        answer = chatbot.interact('台積電', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:8], '目前台積電股價為')
        answer = chatbot.interact('問股價', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您想問的股票代號或公司簡稱？')

    def test_train_given_depart_and_arrive_station(self):
        chatbot = Chatbot()
        answer = chatbot.interact('台北到板橋', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您要何時出發呢?')
        answer = chatbot.interact('現在', '')
        self.assertIn('車次', answer)

    def test_medicine_ask_effect_of_Panadol(self):
        chatbot = Chatbot()
        answer = chatbot.interact('查普拿疼的作用', '')
        answer = json.loads(answer)['output']
        self.assertEqual(
            answer, '普拿疼普拿炎酸痛凝膠 (PANAFLEX GEL)適應症暫時緩解局部疼痛。副作用暫無資料')

    def test_wiki_ask_jordan(self):
        chatbot = Chatbot()
        answer = chatbot.interact('周杰倫是誰', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:3], '周杰倫')

    def test_phone_call_dad(self):
        chatbot = Chatbot()
        reply_json = chatbot.interact('打給爸爸', '')
        reply = json.loads(reply_json)
        self.assertEqual(reply['output'], '已為您撥打電話,請稍後')
        self.assertEqual(reply['host']['action'], 'phone_call')
        self.assertEqual(reply['host']['name'], '爸爸')

    def test_navigation_to_taipei_station(self):
        chatbot = Chatbot()
        answer = chatbot.interact('導航至台北車站', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], ' 第1步')
    
    def test_navigation_to_Sun_Yat_Sen_Memorial_Hall(self):
        chatbot = Chatbot()
        answer = chatbot.interact('怎麼開車去國父紀念館', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:4], ' 第1步')
    
    def test_taxi_call_taxi(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要叫車', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請告訴我您的手機號碼，以便司機能跟您連絡。')
        answer = chatbot.interact('0912123456', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '正在為您叫車…')

    def test_radio_listen_to_radio(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽廣播', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '正在為您撥放廣播…')

    def test_music_listen_to_music_default_type(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽音樂', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:5], '將為您播放')
    
    def test_music_listen_to_music_rock_type(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽搖滾樂', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:5], '將為您播放')
    
    def test_music_listen_to_music_singer_jay_chou(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽周杰倫的歌', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:9], '將為您播放周杰倫,')
    
    def test_music_listen_to_music_song_name(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽告白氣球', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '將為您播放周杰倫,告白氣球')

    def test_music_listen_to_music_song_name_add_singer(self):
        chatbot = Chatbot()
        answer = chatbot.interact('我要聽周杰倫的告白氣球', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '將為您播放周杰倫,告白氣球')

    def test_tour_ask_nearby_information(self):
        chatbot = Chatbot()
        answer = chatbot.interact('附近有什麼好玩的', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您要查哪個城市的景點')
        answer = chatbot.interact('桃園', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:7], '老K舒眠文化館')
    
    def test_tour_ask_taoyuan_information(self):
        chatbot = Chatbot()
        answer = chatbot.interact('桃園有什麼好玩的', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:7], '老K舒眠文化館')

    def test_tour_ask_nearby_food(self):
        chatbot = Chatbot()
        answer = chatbot.interact('附近有什麼好吃的', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer, '請問您要查哪個城市的美食')
        answer = chatbot.interact('桃園', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:8], '東森山林渡假酒店')

    def test_tour_ask_taoyuan_food(self):
        chatbot = Chatbot()
        answer = chatbot.interact('桃園有什麼好吃的', '')
        answer = json.loads(answer)['output']
        self.assertEqual(answer[:8], '東森山林渡假酒店')
    
    def test_fit_specific_and_auto_parameter_in_the_same_time(self):
        '''
            上午11點為auto_parameter
            台北與高雄為specifi_parameter
        '''
        chatbot = Chatbot()
        answer = chatbot.interact('訂上午11點台北到高雄的車票', '')
        answer = json.loads(answer)['output']
        self.assertIn('從臺北出發', answer)


if __name__ == '__main__':
    unittest.main()
