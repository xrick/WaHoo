import random

class ContextManager:
    LACK_PARA_STATE_ID = 2
    PARA_SATISFIED_STATE_ID = 3

    def state_transition(self, query_result, selected_intent_record, current_intent, nothing_else_flag):
        '''
            para:
            query_result: EngineQueryResult obj
            selected_intent_record: IntentRecord obj
            current_intent: Intent obj

            return:
            IntentRecord obj
        '''
        def is_slots_satisfied(current_intent, selected_intent_record):
            for para in current_intent.parameters:
                if para.name not in selected_intent_record.user_paramenters:
                    return False
            
            return True

        def is_multislot_full(current_intent, selected_intent_record):
            for para in current_intent.parameters:
                if para.max_num > 1 and len(selected_intent_record.user_paramenters[para.name]) < para.max_num:
                    return False
            return True

        transitted_state = 0
        if current_intent.parameters:
            if is_slots_satisfied(current_intent, selected_intent_record) and \
                    (is_multislot_full(current_intent, selected_intent_record) or nothing_else_flag):
                transitted_state = self.PARA_SATISFIED_STATE_ID
            else:
                transitted_state = self.LACK_PARA_STATE_ID
        else:
            transitted_state = query_result.to_state_id

        selected_intent_record.state_id = transitted_state

        return selected_intent_record

    def get_reply_template(self, intent, selected_intent_record, last_state_id):
        def get_first_ask_reply(intent, selected_intent_record):
            for intent_parameter in intent.parameters:
                parameter_name = intent_parameter.name
                if parameter_name not in selected_intent_record.user_paramenters:
                    return intent_parameter.ask
                elif type(selected_intent_record.user_paramenters[parameter_name]) == list:
                    return intent_parameter.re_ask
            return None

        def get_reply_base_on_current_and_last_state_or_default(intent, selected_intent_record, last_state_id):
            if (selected_intent_record.state_id, last_state_id) in intent.reply_dic:
                return intent.reply_dic[(selected_intent_record.state_id, last_state_id)]
            elif (selected_intent_record.state_id, None) in intent.reply_dic:
                return intent.reply_dic[(selected_intent_record.state_id, None)]                
            
            return next(iter(intent.reply_dic.values()))
        
        def select_reply_template_randomly(reply_template_list):
            return random.choice(reply_template_list)

        if selected_intent_record.state_id == self.LACK_PARA_STATE_ID:
            reply_template = get_first_ask_reply(
                intent, selected_intent_record)
        else:
            reply_template_list = get_reply_base_on_current_and_last_state_or_default(
                intent, selected_intent_record, last_state_id)
            reply_template = select_reply_template_randomly(reply_template_list)

        return reply_template
