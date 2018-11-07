import sys
import unittest

sys.path.append('..')
from Engine.EngineQueryResult import EngineQueryResult
from IntentContent.Intent import Intent
from IntentSelector.IntentSelector import DomainSelector
from IntentContent.IntentRecord import IntentRecord


class AnswerFormatterTest(unittest.TestCase):
    DETERMINISTIC_RESULT_PROB = 1

    def test_select_doamin_2domain_no_answer_vs_noraml(self):
        domain_intend_dic = {'Weather': EngineQueryResult(
            0, self.DETERMINISTIC_RESULT_PROB, 0, None, []), 'News': EngineQueryResult(100, self.DETERMINISTIC_RESULT_PROB, 0, None, [])}

        domain_selector = DomainSelector()
        result = domain_selector.select_doamin(
            self._get_domain_sorted_list(),
            domain_intend_dic,
            '',
            [],
            self._get_intend_dic()
        )
        self.assertEqual(result[0], 'News')
        self.assertEqual(result[1].intent_id, 100)

    def test_select_doamin_2domain_noraml_vs_noraml(self):
        domain_intend_dic = {'Weather': EngineQueryResult(
            200, self.DETERMINISTIC_RESULT_PROB, 0, None, []), 'News': EngineQueryResult(100, self.DETERMINISTIC_RESULT_PROB, 0, None, [])}

        intent_selector = DomainSelector()
        result = intent_selector.select_doamin(
            self._get_domain_sorted_list(),
            domain_intend_dic,
            '',
            [],
            self._get_intend_dic()
        )
        self.assertEqual(result[0], 'Weather')
        self.assertEqual(result[1].intent_id, 200)

    def test_select_doamin_2domain_noraml_vs_just_fit_para_fit_intent_para(self):
        domain_intend_dic = {
            'Weather': EngineQueryResult(200, self.DETERMINISTIC_RESULT_PROB, 0, None, []),
            'News': EngineQueryResult(1, self.DETERMINISTIC_RESULT_PROB, 0, None, [])}

        intent_selector = DomainSelector()
        result = intent_selector.select_doamin(
            self._get_domain_sorted_list(),
            domain_intend_dic,
            '',
            [self._get_IntentRecord(100, 0)],
            self._get_intend_dic()
        )
        self.assertEqual(result[0], 'Weather')
        self.assertEqual(result[1].intent_id, 200)

    def test_select_doamin_2domain_noraml_vs_just_fit_para_no_fit_intent_para(self):
        domain_intend_dic = {
            'Weather': EngineQueryResult(200, self.DETERMINISTIC_RESULT_PROB, 0, None, []),
            'News': EngineQueryResult(1, self.DETERMINISTIC_RESULT_PROB, 0, None, [])}

        intent_selector = DomainSelector()
        result = intent_selector.select_doamin(
            self._get_domain_sorted_list(),
            domain_intend_dic,
            '',
            [],
            self._get_intend_dic()
        )
        self.assertEqual(result[0], 'Weather')
        self.assertEqual(result[1].intent_id, 200)

    def _get_domain_sorted_list(self):
        return ['Weather', 'News']

    def _get_intend_dic(self):
        return {100: Intent(100, 'News', 2, 'reply', None), 200: Intent(100, 'Weather', 2, 'reply', None)}

    def _get_IntentRecord(self, id, state_id):
        return_obj = IntentRecord(id, state_id)
        return_obj.user_paramenters = {'test_para_name': 'test_para_value'}
        return return_obj


if __name__ == '__main__':
    unittest.main()
