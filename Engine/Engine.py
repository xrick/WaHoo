import re
import json

from Engine.EngineQueryResult import EngineQueryResult
from config import ENALBE_MACHINE_LEARNING
from IntentClassifier.LogisticRegressionClassfier import LogisticRegressionClassfier


class Engine:
    REPLACE_FORMATE = '${{{0}}}'
    RE_REPLACE_FORMATE = r'\$\{([^\$]*?)\}'
    ANCHOR_FORMATE = '^{0}$'

    NO_ANSWER_INTENT_ID = 0
    NO_ANSWER_TO_STATE_ID = 0
    JUST_GET_PARA_INTENT_ID = 1
    DETERMINISTIC_RESULT_PROB = 1
    ERROR_VARIABLE_NOT_FOUND = 'Variable:{0} is not found.'

    def __init__(self, engine_name, keywords, intent_items, re_intent_mapping_list, local_preprocessors, domain_data):
        self._engine_name = engine_name
        self._ReIntentMapping_list = []
        self._regex_keyword_list = []
        self._load_regex(keywords, intent_items, re_intent_mapping_list)
        self._local_preprocessors = local_preprocessors

        self._classifier = None
        if ENALBE_MACHINE_LEARNING and domain_data:
            self._classifier = LogisticRegressionClassfier()
            self._classifier.fit(domain_data)

    def _load_regex(self, keywords, intent_items, re_intent_mapping_list):
        def compile_keyword_re():
            output_list = []

            for name, reg in keywords.items():
                tmp_regex_obj = re.compile(reg)
                output_list.append((tmp_regex_obj, name))
            return output_list

        def compile_intent_mapping_re():
            for re_intent_mapping in re_intent_mapping_list:
                re_intent_mapping.re = replace_replacer_recursively(
                    re_intent_mapping.re)
                re_intent_mapping.re = add_boundary_anchors(
                    re_intent_mapping.re)
                re_intent_mapping.re = re.compile(re_intent_mapping.re)
            return re_intent_mapping_list

        def add_boundary_anchors(reg):
            return self.ANCHOR_FORMATE.format(reg)

        def replace_replacer_recursively(reg):
            compiled_re = re.compile(self.RE_REPLACE_FORMATE)
            result = compiled_re.search(reg)
            while result != None:
                variable_name_contain_symbol = result.group(0)
                variable_name = result.group(1)
                replaced_re = ''
                if variable_name in intent_items:
                    replaced_re = intent_items[variable_name]
                elif variable_name in keywords:
                    replaced_re = keywords[variable_name]
                else:
                    raise Exception(
                        self.ERROR_VARIABLE_NOT_FOUND.format(variable_name))

                replaced_re_with_parentheses = '({0})'.format(replaced_re)
                reg = reg.replace(
                    variable_name_contain_symbol, replaced_re_with_parentheses)
                result = compiled_re.search(reg)

            return reg

        self._regex_keyword_list = compile_keyword_re()
        self._ReIntentMapping_list = compile_intent_mapping_re()

    def get_engine_name(self):
        return self._engine_name

    def parse(self, user_input, state_id_list):
        '''
        Description:
            將使用者輸入的語音語句進行前處理、取出語句中的實體、進行utterance mapping
        Parameters:
            user_input:使用者語音語句
            state_id_list:
        return:
            EngineQueryResult object
        '''
        user_input = self._preprocess(user_input)
        entities = self._extract_entities(user_input)
        matched_intent_id, prob, transfer_to_state_id, intent_parameters = self._map_utterance(
            user_input, state_id_list, entities)

        return EngineQueryResult(
            matched_intent_id, prob, transfer_to_state_id, intent_parameters, entities)

    def _preprocess(self, user_input):
        processed_input = user_input
        for preprocessor in self._local_preprocessors:
            processed_input = preprocessor.process(processed_input)
        return processed_input

    def _extract_entities(self, user_input):
        '''
        Description:
            取出所需的實體
        Parameters:
            user_input : 使用者語音語句
        '''
        return_entities_list = []
        for reg, entities_type in self._regex_keyword_list:
            tmp_input_for_replace = user_input
            isfound = True
            while isfound:
                search_result = reg.search(tmp_input_for_replace)
                if search_result != None:
                    tmp_input_for_replace = reg.sub(
                        self.REPLACE_FORMATE.format(entities_type), #
                        tmp_input_for_replace,
                        count=1
                    )
                    return_entities_list.append(
                        (entities_type, search_result[0]))
                else:
                    isfound = False

        return return_entities_list

    def _map_utterance(self, user_input, state_id_list, entities):
        def map_utterance_with_regex(user_input, state_id_list):
            selected_ReIntentMapping_list = [
                re_intent_mapping for re_intent_mapping in self._ReIntentMapping_list if re_intent_mapping.from_state_id in state_id_list]

            for re_intent_mapping in selected_ReIntentMapping_list:
                match_result = re_intent_mapping.re.match(user_input)
                if match_result:
                    return (re_intent_mapping.intent_id, self.DETERMINISTIC_RESULT_PROB, re_intent_mapping.to_state_id, match_result.groupdict())
            return (self.NO_ANSWER_INTENT_ID, self.DETERMINISTIC_RESULT_PROB, self.NO_ANSWER_TO_STATE_ID, {})

        def map_utterance_with_classifier(user_input):
            result_intent_id, result_prob = self._classifier.predict(
                user_input)
            return (result_intent_id, result_prob, self.NO_ANSWER_TO_STATE_ID, {})

        result_intent_id, prob, transfer_to_state_id, intent_parameters = map_utterance_with_regex(user_input, state_id_list)
        if entities and result_intent_id == self.NO_ANSWER_INTENT_ID:
            result_intent_id = self.JUST_GET_PARA_INTENT_ID
        
        if result_intent_id == self.NO_ANSWER_INTENT_ID and ENALBE_MACHINE_LEARNING and self._classifier:
            result_intent_id, prob, transfer_to_state_id, intent_parameters = map_utterance_with_classifier(user_input)

        return result_intent_id, prob, transfer_to_state_id, intent_parameters
