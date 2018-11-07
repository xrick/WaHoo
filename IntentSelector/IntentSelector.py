class DomainSelector:
    NO_ANSWER_ID = 0
    JUST_FIT_PARA_ID = 1

    LAST_DOMAIN_WEIGHT = 5
    NOT_NO_ANSWER_WEIGHT = 10
    JUST_FIT_PARA_WEIGHT = 3
    PROB_WEIGHT = 20

    def select_doamin(self, domain_sorted_list, domain_intend_dic, last_domain, user_intent_record_list, intend_dic):
        '''
            Calculate score and return the highest one
        '''

        domain_score_dic = dict()
        for domain in domain_sorted_list:
            domain_score_dic[domain] = 0
        if last_domain:
            domain_score_dic[last_domain] += self.LAST_DOMAIN_WEIGHT

        for domain, query_result in domain_intend_dic.items():
            if query_result.intent_id == self.NO_ANSWER_ID:
                pass
            elif query_result.intent_id == self.JUST_FIT_PARA_ID:
                domain_score_dic[domain] += query_result.prob * self.PROB_WEIGHT
                for intent_record in user_intent_record_list:
                    if intend_dic[intent_record.intent_id].domain == domain:
                        domain_score_dic[domain] += self.JUST_FIT_PARA_WEIGHT
                        break
            else:
                domain_score_dic[domain] += self.NOT_NO_ANSWER_WEIGHT
                domain_score_dic[domain] += query_result.prob * self.PROB_WEIGHT

        #TODO:score up by user_intent_list

        max_score_domain = max(domain_score_dic, key=domain_score_dic.get)

        return max_score_domain, domain_intend_dic[max_score_domain]
