import sys
import unittest

sys.path.append('..')
from Engine.Engine import Engine
from Engine.EngineQueryResult import EngineQueryResult
from IntentLoader.ReIntentMapping import ReIntentMapping


class EngineTest(unittest.TestCase):
    NONE_STATE_ID = 0        
    def test_parse_keyword_only_sentence(self):
        test_keyword_name = 'keyword1'
        test_re = 'test_re'
        engine = Engine('test_engine', {test_keyword_name: test_re}, {}, {}, [], {})
        result = engine.parse(test_re, [])

        expected_list = [(test_keyword_name, test_re)]
        self.assertListEqual(expected_list, result.entities)

    def test_parse_sentence_contain_keyword(self):
        test_keyword_name = 'keyword1'
        test_re = 'test_re'
        engine = Engine('test_engine', {test_keyword_name: test_re}, {}, {}, [], {})

        test_query = 'test_prefix' + test_re + 'test_postfix'
        result = engine.parse(test_query, [])

        expected_list = [(test_keyword_name, test_re)]
        self.assertListEqual(expected_list, result.entities)
    
    def test_parse_from_None_sate_to_None_state(self):
        state_id_list = [self.NONE_STATE_ID]
        test_intent_id = 1
        test_re = 'test_re'
        engine = Engine('test_engine', {}, {}, [ReIntentMapping(test_re, test_intent_id, self.NONE_STATE_ID, self.NONE_STATE_ID)], [], {})

        test_query = test_re
        result = engine.parse(test_query, state_id_list)

        self.assertEqual(test_intent_id, result.intent_id)

    def test_parse_no_answer(self):
        state_id_list = [self.NONE_STATE_ID]
        test_intent_id = 1
        no_answer_id = 0
        test_re = 'test_re(test_para)'
        engine = Engine('test_engine', {}, {}, [ReIntentMapping(test_re, test_intent_id, self.NONE_STATE_ID, self.NONE_STATE_ID)], [], {})

        test_query = ''
        result = engine.parse(test_query, state_id_list)

        self.assertEqual(no_answer_id, result.intent_id)
    
    def test_parse_extract_group_name(self):
        
        test_intent_id = 1
        test_re = 'testprefix(?P<test_group_name>test_para)testpostfix'
        engine = Engine('test_engine', {}, {}, [ReIntentMapping(test_re, test_intent_id, self.NONE_STATE_ID, self.NONE_STATE_ID)], [], {})
        test_query = 'testprefixtest_paratestpostfix'

        state_id_list = [self.NONE_STATE_ID]
        result = engine.parse(test_query, state_id_list)

        self.assertEqual(1, len(result.intent_parameters))
        self.assertEqual('test_para', result.intent_parameters['test_group_name'])


if __name__ == '__main__':
    unittest.main()
