import json
import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch

sys.path.append('..')
from Chatbot.Chatbot import Chatbot
from IntentLoader.IntentLoader import IntentLoader
from IntentSelector.IntentSelector import DomainSelector
from IntentContent.IntentRecord import IntentRecord
from IntentContent.Intent import Intent
from IntentContent.IntentParameter import IntentParameter
from Engine.EngineQueryResult import EngineQueryResult
from Engine.Engine import Engine
from ContextManager.ContextManager import ContextManager


class ChatbotTest(unittest.TestCase):
    TEST_USER_ID = ''
    TEST_INTENT_ID = 100
    TEST_TO_STATE_ID = 100
    NO_ANSWER_INTENT_ID = 0
    JUST_GET_PARA_INTENT_ID = 1
    NOTHING_ELSE_INTENT_ID = 2
    NONE_STATE_ID = 1
    LACK_PARA_STATE_ID = 2
    TEST_USER_INPUT = '123'
    TEST_DOMAIN_NAME = 'test_domain_name'
    TEST_DOMAIN_NAME_2 = 'test_domain_name_2'
    TEST_REPLY_TEMPLATE = 'test_reply_template'
    TEST_REPLY_STRING = 'test_reply'
    TEST_REPLY_DIC = {'output': TEST_REPLY_STRING}
    TEST_PARA_KEYWORD_NAME = 'test_keyword_name'
    TEST_PARA_NAME = 'test_name'
    TEST_PARA_ASK = 'test_ask'
    TEST_PARA_DATA_TYPE = 'test_data_type'
    DETERMINISTIC_RESULT_PROB = 1

    def test_interact_normal_intent_id_no_para(self):
        test_obj = self._get_test_Chatbot_obj(self.TEST_TO_STATE_ID)
        result = test_obj.interact(self.TEST_USER_INPUT, self.TEST_USER_ID)
        result = json.loads(result)['output']
        self.assertEqual(result, self.TEST_REPLY_STRING)

    def test_interact_normal_intent_id_ask_para(self):
        test_obj = self._get_test_Chatbot_obj(self.LACK_PARA_STATE_ID)
        result = test_obj.interact(self.TEST_USER_INPUT, self.TEST_USER_ID)
        result = json.loads(result)['output']
        self.assertEqual(result, self.TEST_REPLY_TEMPLATE)

    def _get_test_Chatbot_obj(self, state_id_after_transition):
        def mock_Chatbot_init(test_obj):
            test_obj._is_save_dialog_state_to_redis = False
            test_obj.intent_dic = {}
            test_obj.engine_list = []
            test_obj.domain_list = []
            test_obj.answer_formatter_dic = {}
            test_obj._is_log_to_file = False

            test_obj._intent_loader = get_mock_IntentLoader()
            test_obj._domain_selector = get_mock_DomainSelector()
            test_obj._context_manager = get_mock_ContextManager()
            test_obj._global_preprocessors = []
            test_obj._get_dialog_state, test_obj._set_dialog_state = test_obj._decide_get_and_set_dialog_state_method()
            test_obj._get_answer_formatters = Mock(
                return_value={self.TEST_DOMAIN_NAME: get_mock_answer_formatter()})
            test_obj._load_domain()

        def get_mock_answer_formatter():
            mock_answer_formatter = Mock()
            mock_answer_formatter.formate_answer = Mock(
                return_value=self.TEST_REPLY_DIC)
            return mock_answer_formatter

        def get_mock_ContextManager():
            mock_ContextManager = ContextManager()
            mock_ContextManager.state_transition = Mock(
                return_value=IntentRecord(self.TEST_INTENT_ID, state_id_after_transition))
            mock_ContextManager.get_reply_template = Mock(
                return_value=self.TEST_REPLY_TEMPLATE)
            return mock_ContextManager

        def get_mock_DomainSelector():
            return_DomainSelector = DomainSelector()
            return_DomainSelector.select_doamin = Mock(
                return_value=(self.TEST_DOMAIN_NAME, EngineQueryResult(self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, self.TEST_TO_STATE_ID, {}, [])))
            return return_DomainSelector

        def get_mock_IntentLoader():
            with patch.object(IntentLoader, "__init__", lambda x: None):
                return_IntentLoader = IntentLoader()
            return_IntentLoader.get_domain_list = Mock(
                return_value=[self.TEST_DOMAIN_NAME, self.TEST_DOMAIN_NAME_2])
            return_IntentLoader.get_intent_dic = Mock(return_value={
                self.TEST_INTENT_ID: Intent(
                    self.TEST_INTENT_ID,
                    self.TEST_DOMAIN_NAME,
                    0,
                    {(self.TEST_TO_STATE_ID, None): self.TEST_REPLY_TEMPLATE},
                    [])})
            return_IntentLoader.get_engine_list = Mock(
                return_value=get_mock_engine_list())
            return return_IntentLoader

        def get_mock_engine_list():
            with patch.object(Engine, "__init__", lambda x: None):
                mock_engine = Engine()
            mock_engine.get_engine_name = lambda: self.TEST_DOMAIN_NAME
            mock_engine._preprocess = Mock(return_value=self.TEST_USER_INPUT)
            mock_engine._extract_entities = Mock(return_value=[])
            mock_engine._map_utterance = Mock(return_value=(self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, self.TEST_TO_STATE_ID, None))
            return [mock_engine]

        with patch.object(Chatbot, "__init__", lambda x: None):
            test_obj = Chatbot()

        mock_Chatbot_init(test_obj)
        test_obj._load_settings = Mock(return_value=None)
        return test_obj


if __name__ == '__main__':
    unittest.main()
