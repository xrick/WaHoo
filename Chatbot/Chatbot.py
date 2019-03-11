import importlib
import json
import os
import pickle
import os
import redis

import config
from IntentLoader.IntentLoader import IntentLoader
from IntentSelector.IntentSelector import DomainSelector
from IntentContent.IntentRecord import IntentRecord
from Engine.EngineQueryResult import EngineQueryResult
from ContextManager.ContextManager import ContextManager
from Preprocessor.SynonymPreprocessor import SynonymPreprocessor


class Chatbot():
    DOMAINS_FOLDER_NAME = 'AnswerFormatters'
    FILTER_FOLDERS = ['AnswerFormatters', '__pycache__']
    ANSWER_FORMATTER_FILE_NAME = 'AnswerFormatter.py'
    NO_ANSWER = '抱歉我不懂你說什麼...'
    NO_ANSWER_INTENT_ID = 0
    JUST_GET_PARA_INTENT_ID = 1
    NOTHING_ELSE_INTENT_ID = 2
    NONE_STATE_ID = 1
    LACK_PARA_STATE_ID = 2
    PARA_SATISFIED_STATE_ID = 3

    def __init__(self):
        # system
        self.intent_dic = {}
        self.engine_list = [] 
        self.domain_list = []
        self.answer_formatter_dic = {}

        self._intent_loader = IntentLoader()
        self._domain_selector = DomainSelector()
        self._context_manager = ContextManager()
        self._global_preprocessors = [SynonymPreprocessor()]

        self._get_dialog_state, self._set_dialog_state = self._decide_get_and_set_dialog_state_method()
        self._load_domain()

    def interact(self, raw_input, user_id):
        def get_intent_record_fit_intent_id_in_intent_record_list(user_intent_id, intent_record_list, current_intent):
            match_intent_record = next(
                (record for record in intent_record_list if record.intent_id == user_intent_id), None)
            if not match_intent_record:
                match_intent_record = IntentRecord(
                    user_intent_id, current_intent.initial_state_id)

            match_intent_record = fill_slot_with_default(
                current_intent, match_intent_record)

            return match_intent_record

        def fill_slot_with_default(intent, intent_record):
            for para in intent.parameters:
                if para.default_value and para.name not in intent_record.user_paramenters:
                    intent_record.user_paramenters[para.name] = para.default_value
            return intent_record

        def flush_parameters(selected_intent_record):
            if selected_intent_record.state_id == self.PARA_SATISFIED_STATE_ID:
                selected_intent_record.user_paramenters = {}
                selected_intent_record.state_id = self.NONE_STATE_ID

        def formate_output_json_string(current_domain, input_string, reply_dic):
            reply_dic['current_domain'] = current_domain
            reply_dic['input'] = input_string
            return json.dumps(reply_dic, ensure_ascii=False)

        def global_preprocess(raw_input):
            processed_input = raw_input
            for preprocessor in self._global_preprocessors:
                processed_input = preprocessor.process(processed_input)
            return processed_input

        user_intent_record_list, last_domain = self._get_dialog_state(user_id)

        intend_dic = dict()
        user_state_list = [self.NONE_STATE_ID]
        user_state_list.extend([
            intent_content.state_id for intent_content in user_intent_record_list if intent_content.state_id not in user_state_list])

        user_input = global_preprocess(raw_input)

        for engine in self.engine_list:
            query_result = engine.parse(user_input, user_state_list)
            intend_dic.update({engine.get_engine_name(): query_result})

        current_domain, query_result = self._domain_selector.select_doamin(
            self.domain_list, intend_dic, last_domain, user_intent_record_list, self.intent_dic)
        query_result, nothing_else_flag = self._substitude_spcific_intent_id(
            query_result, user_intent_record_list)
        if query_result.intent_id == self.NO_ANSWER_INTENT_ID:
            current_domain = 'None'
            reply_dic = {'output': self.NO_ANSWER, 'action': {}}
        else:
            current_intent = self.intent_dic[query_result.intent_id]
            selected_intent_record = get_intent_record_fit_intent_id_in_intent_record_list(
                query_result.intent_id, user_intent_record_list, current_intent)

            selected_intent_record = self._fill_slot(
                query_result, selected_intent_record, current_intent)

            last_state_id = selected_intent_record.state_id
            selected_intent_record = self._context_manager.state_transition(
                query_result, selected_intent_record, current_intent, nothing_else_flag)
            reply = self._context_manager.get_reply_template(
                current_intent, selected_intent_record, last_state_id)

            if selected_intent_record.state_id != self.LACK_PARA_STATE_ID \
                    and current_intent.domain in self.answer_formatter_dic:
                reply_dic = self.answer_formatter_dic[current_intent.domain].formate_answer(
                    selected_intent_record, reply)
                flush_parameters(selected_intent_record)
            else:
                reply_dic = {'output': reply, 'action': {}}

            if selected_intent_record in user_intent_record_list:
                user_intent_record_list.remove(selected_intent_record)
            user_intent_record_list.insert(0, selected_intent_record)

            self._set_dialog_state(
                user_id, user_intent_record_list, current_domain)

        reply_json = formate_output_json_string(
            current_domain, user_input, reply_dic)

        if config.IS_LOG_TO_FILE:
            self._log_to_file(user_id, raw_input, user_input,
                              current_domain, query_result, reply_json)

        return reply_json

    def _decide_get_and_set_dialog_state_method(self):
        if config.SAVE_DIALOG_STATE_TO_REDIS:
            self._redis_context = redis.Redis(
                host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
            return self._get_dialog_state_from_redis, self._set_dialog_state_from_redis

        self._user_intent_dic = {}
        self._last_domain = {}
        return self._get_dialog_state_inside, self._set_dialog_state_inside

    def _get_dialog_state_inside(self, user_id):
        def initialize_user_data(user_id):
            if user_id not in self._user_intent_dic:
                self._user_intent_dic[user_id] = []
                self._last_domain[user_id] = ''

        initialize_user_data(user_id)
        user_intent_dic = self._user_intent_dic[user_id]
        last_domain = self._last_domain[user_id]
        return user_intent_dic, last_domain

    def _set_dialog_state_inside(self, user_id, user_intent_dic, last_domain):
        self._user_intent_dic[user_id] = user_intent_dic
        self._last_domain[user_id] = last_domain

    def _get_dialog_state_from_redis(self, user_id):
        user_dialog_state = self._redis_context.get(user_id)
        if not user_dialog_state:
            return list(), None
        user_dialog_state = pickle.loads(user_dialog_state)
        intent_list = user_dialog_state.get('intent_list', list())
        last_domain = user_dialog_state.get('last_domain', None)
        return intent_list, last_domain

    def _set_dialog_state_from_redis(self, user_id, user_intent_dic, last_domain):
        user_dialog_state = {
            'intent_list': user_intent_dic, 'last_domain': last_domain}
        user_dialog_state_pickle = pickle.dumps(user_dialog_state)
        self._redis_context.set(user_id, user_dialog_state_pickle)

    def _load_domain(self):
        self.domain_list = self._intent_loader.get_domain_list()
        self.intent_dic = self._intent_loader.get_intent_dic()
        self.engine_list = self._intent_loader.get_engine_list(
            self.domain_list)
        self.answer_formatter_dic = self._get_answer_formatters()
        return

    def _get_answer_formatters(self):
        return_dic = {}
        for root, _, files in os.walk(self.DOMAINS_FOLDER_NAME):
            domain_name = os.path.basename(root)
            for file in files:
                if file == self.ANSWER_FORMATTER_FILE_NAME:
                    i = importlib.import_module(
                        "AnswerFormatters.{0}.AnswerFormatter".format(domain_name))
                    return_dic[domain_name] = i.AnswerFormatter(
                    )
        return return_dic

    def _substitude_spcific_intent_id(self, query_result, intent_record_list):
        def substitude_just_get_para_intent_id(user_intent_id):
            if user_intent_id == self.JUST_GET_PARA_INTENT_ID:
                if intent_record_list:
                    user_intent_id = get_first_intent_id_fit_parameter()
                else:
                    user_intent_id = self.NO_ANSWER_INTENT_ID
            return user_intent_id

        def get_first_intent_id_fit_parameter():
            last_intent_record = intent_record_list[0]
            for parameter in self.intent_dic[last_intent_record.intent_id].parameters:
                for entity_type, _ in query_result.entities:
                    if parameter.keyword_name == entity_type:
                        return last_intent_record.intent_id
            return self.NO_ANSWER_INTENT_ID

        def substitude_nothing_else_id(user_intent_id):
            nothing_else_flag = False
            if user_intent_id == self.NOTHING_ELSE_INTENT_ID:
                if intent_record_list:
                    user_intent_id = intent_record_list[0].intent_id
                    nothing_else_flag = True
                else:
                    user_intent_id = self.NO_ANSWER_INTENT_ID
            return user_intent_id, nothing_else_flag

        user_intent_id = query_result.intent_id
        user_intent_id = substitude_just_get_para_intent_id(user_intent_id)
        user_intent_id, nothing_else_flag = substitude_nothing_else_id(
            user_intent_id)
        query_result.intent_id = user_intent_id
        return query_result, nothing_else_flag

    def _fill_slot(self, query_result, selected_intent_record, intent):
        def macth_parameter_with_keyword(query_result, selected_intent_record, intent, filled_parameter):
            # TODO: consider about order.
            for keyword_name, keyword_vaule in query_result.entities:
                if filled_parameter:
                    unfilled_parameter = [para for para in intent.parameters if para.name not in filled_parameter]
                else:
                    unfilled_parameter = intent.parameters
                for intent_parameter in unfilled_parameter:
                    parameter_name = intent_parameter.name
                    if keyword_name == intent_parameter.keyword_name:
                        if intent_parameter.max_num > 1:
                            fill_mutivaule_slot(
                                parameter_name, selected_intent_record, keyword_vaule)
                        else:
                            selected_intent_record.user_paramenters[parameter_name] = keyword_vaule
                            filled_parameter.append(parameter_name)
                        continue

        def fill_mutivaule_slot(parameter_name, selected_intent_record, keyword_vaule):
            if parameter_name in selected_intent_record.user_paramenters:
                selected_intent_record.user_paramenters[parameter_name].append(
                    keyword_vaule)
            else:
                selected_intent_record.user_paramenters[parameter_name] = [
                    keyword_vaule]

        filled_parameter = []
        if query_result.intent_parameters:
            selected_intent_record.user_paramenters.update(
                query_result.intent_parameters)
            filled_parameter = list(query_result.intent_parameters.keys())

        macth_parameter_with_keyword(
            query_result, selected_intent_record, intent, filled_parameter)
        return selected_intent_record

    def _log_to_file(self, user_id, raw_input, user_input, current_domain, query_result, reply_json):
        with open(config.LOG_PATH, mode='a', encoding='utf-8') as log_file:
            log_string = ' '.join([
                user_id,
                raw_input,
                user_input,
                current_domain,
                str(query_result.intent_id),
                reply_json,
                '\n'])
            log_file.write(log_string)


if __name__ == "__main__":
    bot = Chatbot()
    while True:
        question = input('Q:')
        answer = bot.interact(question, '')
        print('A:{0}'.format(answer))
