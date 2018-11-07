import unittest
import sys
sys.path.append('..')
from AnswerFormatters.Hospital.AnswerFormatter import AnswerFormatter
from IntentContent.Intent import Intent
from IntentContent.IntentRecord import IntentRecord


class HospitalAnswerFormatterTest(unittest.TestCase):

    def test_ask_division_depression_headache(self):
        answer_formatter = AnswerFormatter()

        intent_record = IntentRecord(200, 3)
        intent_record.user_paramenters = {'symptom': ['憂鬱', '頭痛']}
        reply_template = '建議您至{0}就診'
        answer = answer_formatter.formate_answer(intent_record, reply_template)
        self.assertEqual(answer['output'], '建議您至精神科就診')

    def test_ask_division_cough_headache(self):
        answer_formatter = AnswerFormatter()

        intent_record = IntentRecord(200, 3)
        intent_record.user_paramenters = {'symptom': ['咳嗽', '頭痛']}
        reply_template = '建議您至{0}就診'
        answer = answer_formatter.formate_answer(intent_record, reply_template)
        self.assertEqual(answer['output'], '建議您至耳鼻喉科就診')


if __name__ == '__main__':
    unittest.main()
