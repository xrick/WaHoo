import sys
import unittest

sys.path.append('..')
from unittest.mock import Mock, patch
from IntentLoader.IntentLoader import IntentLoader
from IntentClassifier.Tokenizer import Tokenizer


class IntentLoaderTest(unittest.TestCase):

    def test_get_domain_list_2domain_should_call_get_domain_list_from_sql(self):
        intent_loader = IntentLoader()
        intent_loader._db_interactor.get_domain_list_from_sql = Mock()
        intent_loader.get_domain_list()

        intent_loader._db_interactor.get_domain_list_from_sql.assert_called_once()

    def test_get_intent_dic_should_call_get_intent_list_from_db(self):
        intent_loader = IntentLoader()
        intent_loader._db_interactor.get_intent_list_from_db = Mock(
            return_value=([], [], []))
        intent_loader.get_intent_dic()
        intent_loader._db_interactor.get_intent_list_from_db.assert_called_once()

    def test_get_intent_dic_1_intent_with_1_para(self):
        intent_loader = IntentLoader()
        intent_loader._db_interactor.get_intent_list_from_db = lambda: (
            [(1, 'test_domain_name', 1)],
            [('test_type_name', 1, 'test_para_name',
              'test_ask', 1, None, None, 'string')],
            [(1, 1, 'test_reply', None)])
        intent_dic = intent_loader.get_intent_dic()
        self.assertEqual(len(intent_dic), 1)
        self.assertEqual(intent_dic[1].domain, 'test_domain_name')
        self.assertEqual(intent_dic[1].id, 1)
        self.assertEqual(len(intent_dic[1].reply_dic), 1)
        self.assertEqual(len(intent_dic[1].reply_dic[(1, None)]), 1)
        self.assertEqual(intent_dic[1].reply_dic[(1, None)][0], 'test_reply')
        self.assertEqual(len(intent_dic[1].parameters), 1)
        self.assertEqual(intent_dic[1].parameters[0].ask, 'test_ask')
        self.assertEqual(
            intent_dic[1].parameters[0].keyword_name, 'test_type_name')
        self.assertEqual(intent_dic[1].parameters[0].max_num, 1)
        self.assertEqual(intent_dic[1].parameters[0].name, 'test_para_name')
        self.assertIsNone(intent_dic[1].parameters[0].default_value)
        self.assertIsNone(intent_dic[1].parameters[0].re_ask)
        self.assertEqual(intent_dic[1].parameters[0].data_type, 'string')

    def test_get_intent_dic_1_intent_0_para_two_reply(self):
        intent_loader = IntentLoader()
        intent_loader._db_interactor.get_intent_list_from_db = lambda: (
            [(1, 'test_domain_name', 1)],
            [],
            [(1, 1, 'test_reply', None), (1, 1, 'test_reply2', None)])
        intent_dic = intent_loader.get_intent_dic()
        self.assertEqual(len(intent_dic), 1)
        self.assertEqual(intent_dic[1].domain, 'test_domain_name')
        self.assertEqual(intent_dic[1].id, 1)
        self.assertEqual(len(intent_dic[1].reply_dic), 1)
        self.assertEqual(len(intent_dic[1].reply_dic[(1, None)]), 2)
        self.assertEqual(intent_dic[1].reply_dic[(1, None)][0], 'test_reply')
        self.assertEqual(intent_dic[1].reply_dic[(1, None)][1], 'test_reply2')

    def test_get_engine_list(self):
        with patch.object(Tokenizer, 'set_dict', new=lambda x: None):
            test_IntentReMappingId = 1
            intent_loader = IntentLoader()
            intent_loader._db_interactor.get_keywords_dic = lambda x: (
                {'test_keyword_name': 'test_keyword_re'})
            intent_loader._db_interactor.get_intent_replacer_dic = lambda: (
                {'test_replacer_name': 'test_replacer_re'})
            intent_loader._db_interactor.get_re_intentId_mapping = lambda x: (
                [(test_IntentReMappingId, 'test_intent_re', 'test_intent_id', 0, 0)])
            intent_loader._db_interactor._get_re_intentId_mapping_parameters = lambda: (
                [(test_IntentReMappingId, 1, 'test_parameter_name')])
            intent_loader._db_interactor.get_local_preprocessor_list_from_sql = lambda x: ([
                                                                                         'SynonymPreprocessor'])

            engine_list = intent_loader.get_engine_list(['test_domain'])
            self.assertEqual(len(engine_list), 1)
            self.assertEqual(engine_list[0].get_engine_name(), 'test_domain')


if __name__ == '__main__':
    unittest.main()
