import json
import urllib.request
from AnswerFormatters.AnswerFormatterBase import AnswerFormatterBase


class AnswerFormatter(AnswerFormatterBase):

    DIVISION_SYMPTOM_MAPPING = {
        '家庭醫學科' :{'頭痛'},
        '精神科' : {'憂鬱', '頭痛'},
        '耳鼻喉科' : {'咳嗽', '頭痛'}
    }

    def formate_answer(self, intent_record, reply_template):
        intent_id = intent_record.intent_id
        reply = reply_template
        normalized_symptom_list = self._normalize_symptom_list(intent_record.user_paramenters['symptom'])
        answer = reply_template
        try:
            if intent_id == 200:
                answer = self._suggest_division(reply, normalized_symptom_list)
        except Exception as e:
            return e
        
        reply_dic = self._formate_to_dict(answer, None)
        return reply_dic
    
    def _normalize_symptom_list(self, symptom_list):
        def normalize_symptom(symptom):
            symptom = symptom.replace('不適', '痛')
            symptom = symptom.replace('不舒服', '痛')
            symptom = symptom.replace('疼', '痛')
            return symptom

        normalized_symptom_list = []
        for symptom in symptom_list:
            normalized_symptom = normalize_symptom(symptom)
            normalized_symptom_list.append(normalized_symptom)
        return normalized_symptom_list


    def _suggest_division(self, reply, normalized_symptom_list):
        answer = '抱歉我不清楚耶,請至服務中心詢問'
        normalized_symptom_set = set(normalized_symptom_list)
        for division, symptom_list in self.DIVISION_SYMPTOM_MAPPING.items():
            intersection = set.intersection(symptom_list, normalized_symptom_set)
            if len(intersection) == len(normalized_symptom_list):
                answer = reply.format(division)
                break
        return answer
