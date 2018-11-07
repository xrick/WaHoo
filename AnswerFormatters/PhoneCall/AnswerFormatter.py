import urllib
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):
    def formate_answer(self, intent_record, reply_template):
        """        
        Arguments:
            intent_record {IntentRecord Obj} -- users data
            reply_template {string} -- None

        Return: dict
        """
        intent_id = intent_record.intent_id
        reply_dic = self._formate_to_dict(reply_template, None)
        if intent_id == 901:
            reply_dic['action'] = {'action':'phone_call', 'name':intent_record.user_paramenters['callee']}

        return reply_dic

