import sys
import unittest

sys.path.append('..')
from ContextManager.ContextManager import ContextManager
from Engine.EngineQueryResult import EngineQueryResult
from IntentContent.Intent import Intent
from IntentContent.IntentRecord import IntentRecord
from IntentContent.IntentParameter import IntentParameter


class ContextManagerTest(unittest.TestCase):
    LACK_PARA_STATE_ID = 2
    PARA_SATISFIED_STATE_ID = 3
    TEST_INTENT_ID = 1
    DETERMINISTIC_RESULT_PROB = 1

    def test_state_transition_no_parameter_state_transfer(self):
        from_state_id = 99
        to_state_id = 100
        engine_query_result = EngineQueryResult(
            self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, to_state_id, {}, [])
        intent_record = IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent = Intent(self.TEST_INTENT_ID, 'test_domain', from_state_id, {
                        (from_state_id, None): 'test_reply'}, {})
        context_manager = ContextManager()
        result = context_manager.state_transition(
            engine_query_result, intent_record, intent, False)

        self.assertEqual(self.TEST_INTENT_ID, result.intent_id)
        self.assertEqual(to_state_id, result.state_id)

    def test_state_transition_None_to_parameter_not_satisfied(self):
        from_state_id = 99
        to_state_id = 100
        engine_query_result = EngineQueryResult(
            self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, to_state_id, {}, [])
        intent_record = IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent=Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, from_state_id): 'test_reply'},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 1, None, None, 'string')])
            
        context_manager=ContextManager()
        result=context_manager.state_transition(
            engine_query_result, intent_record, intent, False)

        self.assertEqual(self.TEST_INTENT_ID, result.intent_id)
        self.assertEqual(self.LACK_PARA_STATE_ID, result.state_id)

    def test_state_transition_multi_value_slot_less_than_max(self):
        from_state_id=99
        to_state_id=100
        engine_query_result=EngineQueryResult(
            self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, to_state_id, {}, [])
        intent_record=IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent_record.user_paramenters={'test_para': ['test_value']}
        intent=Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, from_state_id): 'test_reply'},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.state_transition(
            engine_query_result, intent_record, intent, False)

        self.assertEqual(self.TEST_INTENT_ID, result.intent_id)
        self.assertEqual(self.LACK_PARA_STATE_ID, result.state_id)

    def test_state_transition_multi_value_slot_less_than_max_but_stop(self):
        from_state_id=99
        to_state_id=100
        engine_query_result=EngineQueryResult(
            self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, to_state_id, {}, [])
        intent_record=IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent_record.user_paramenters={'test_para': ['test_value']}
        intent=Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, from_state_id): 'test_reply'},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.state_transition(
            engine_query_result, intent_record, intent, True)

        self.assertEqual(self.TEST_INTENT_ID, result.intent_id)
        self.assertEqual(self.PARA_SATISFIED_STATE_ID, result.state_id)

    def test_state_transition_multi_value_slot_equal_to_max(self):
        from_state_id=99
        to_state_id=100
        engine_query_result=EngineQueryResult(
            self.TEST_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, to_state_id, {}, [])
        intent_record=IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent_record.user_paramenters={
            'test_para': ['test_value', 'test_value2']}
        intent = Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, from_state_id): 'test_reply'},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.state_transition(
            engine_query_result, intent_record, intent, False)

        self.assertEqual(self.TEST_INTENT_ID, result.intent_id)
        self.assertEqual(self.PARA_SATISFIED_STATE_ID, result.state_id)

    def test_get_reply_template_no_para_default_reply(self):
        last_state_id=0
        from_state_id=99
        intent_record=IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent_record.user_paramenters={
            'test_para': ['test_value', 'test_value2']}
        intent = Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, None): ['test_reply']},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.get_reply_template(
            intent, intent_record, last_state_id)

        self.assertEqual('test_reply', result)

    def test_get_reply_template_no_para_reply_with_last_state(self):
        last_state_id=98
        from_state_id=99
        intent_record=IntentRecord(self.TEST_INTENT_ID, from_state_id)
        intent_record.user_paramenters={
            'test_para': ['test_value', 'test_value2']}
        intent = Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            from_state_id,
            {(from_state_id, last_state_id): ['test_reply'],
             (from_state_id, None): 'test_reply_default'},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.get_reply_template(
            intent, intent_record, last_state_id)

        self.assertEqual('test_reply', result)

    def test_get_reply_template_lack_para_ask(self):
        default_state=0
        last_state_id=98
        intent_record=IntentRecord(
            self.TEST_INTENT_ID, self.LACK_PARA_STATE_ID)
        intent=Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            default_state,
            {},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.get_reply_template(
            intent, intent_record, last_state_id)

        self.assertEqual('ask', result)

    def test_get_reply_template_lack_para_reask(self):
        default_state=0
        last_state_id=98
        intent_record=IntentRecord(
            self.TEST_INTENT_ID, self.LACK_PARA_STATE_ID)
        intent_record.user_paramenters={
            'test_para': ['test_value', 'test_value2']}
        intent = Intent(
            self.TEST_INTENT_ID,
            'test_domain',
            default_state,
            {},
            [IntentParameter('test_keyword_name', 'test_para', 'ask', 2, 're_ask', None, 'string')])
        context_manager=ContextManager()
        result=context_manager.get_reply_template(
            intent, intent_record, last_state_id)

        self.assertEqual('re_ask', result)


if __name__ == '__main__':
    unittest.main()
