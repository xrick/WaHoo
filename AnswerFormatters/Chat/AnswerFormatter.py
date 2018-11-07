from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    def formate_answer(self, intent_record, reply_template):
        reply_dic = self._formate_to_dict(reply_template, None)
        return reply_dic
