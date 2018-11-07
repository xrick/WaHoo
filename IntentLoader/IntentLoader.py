import importlib
import json

from Engine import Engine
from IntentContent.Intent import Intent
from IntentContent.IntentParameter import IntentParameter
from IntentLoader.ReIntentMapping import ReIntentMapping
from DbInteractor.DbInteractor import DbInteractor
from config import ENALBE_MACHINE_LEARNING, DATA_SET_PATH, JIEBA_DICT_PATH
from IntentClassifier.Preprocessor import Preprocessor
from IntentClassifier.Tokenizer import Tokenizer


class IntentLoader:
    def __init__(self):
        self._db_interactor = DbInteractor()

    def get_domain_list(self):
        return self._db_interactor.get_domain_list_from_sql()

    def get_intent_dic(self):
        def select_intent_parameter_by_intent_id():
            return [intent_parameter for intent_parameter in intent_parameter_list if intent_parameter[1] == intent_id]

        def select_intent_reply_by_intent_id():
            return_dic = {}
            for reply_intent_id, state_id, reply, last_state_id in intent_reply_list:
                if reply_intent_id == intent_id:
                    dic_key = (state_id, last_state_id)
                    if dic_key in return_dic:
                        return_dic[dic_key].append(reply)
                    else:
                        return_dic[dic_key] = [reply]

            return return_dic

        def parameter_dic_to_object():
            return [IntentParameter(p[0], p[2], p[3], p[4], p[5], p[6], p[7]) for p in this_intent_parameter_list]

        return_dic = {}

        intent_list, intent_parameter_list, intent_reply_list = self._db_interactor.get_intent_list_from_db()

        for intent_id, domain_name, initial_state_id in intent_list:
            this_intent_parameter_list = select_intent_parameter_by_intent_id()
            this_intent_reply_dic = select_intent_reply_by_intent_id()
            this_intent_parameter_object_list = parameter_dic_to_object()
            return_dic[intent_id] = Intent(
                intent_id, domain_name, initial_state_id, this_intent_reply_dic, this_intent_parameter_object_list)

        return return_dic

    def get_engine_list(self, domain_list):
        def get_engine(domain_name, domain_data):
            keywords = self._db_interactor.get_keywords_dic(domain)
            intent_replacer = self._db_interactor.get_intent_replacer_dic()
            re_intent_id_mapping_list = self._db_interactor.get_re_intentId_mapping(
                domain)
            re_intent_id_mapping_object_list = [
                ReIntentMapping(re, intent_id, from_state_id, to_state_id) for intent_re_mapping_id, re, intent_id, from_state_id, to_state_id in re_intent_id_mapping_list]
            local_preprocessors = get_local_preprocessor_list(domain)

            return Engine.Engine(
                domain, keywords, intent_replacer, re_intent_id_mapping_object_list, local_preprocessors, domain_data)

        def get_local_preprocessor_list(domain):
            preprocessor_name_list = self._db_interactor.get_local_preprocessor_list_from_sql(
                domain)
            preprocessor_list = []
            for preprocessor_name in preprocessor_name_list:
                module = importlib.import_module(
                    "Preprocessor.{0}".format(preprocessor_name))
                temp_class = getattr(module, preprocessor_name)
                preprocessor_list.append(temp_class(domain))
            return preprocessor_list

        engine_list = []

        if ENALBE_MACHINE_LEARNING:
            data_set = self._load_json_file(DATA_SET_PATH)
            Preprocessor.validate_dataset(data_set)
            Tokenizer.set_dict(JIEBA_DICT_PATH)
        else:
            data_set = None

        for domain in domain_list:
            domain_data = Preprocessor.get_domain_data_with_noise(
                data_set, domain) if ENALBE_MACHINE_LEARNING else None

            engine = get_engine(domain, domain_data)
            engine_list.append(engine)

        return engine_list

    def _load_json_file(self, path):
        """return dict:{"dataset":[{"domain_id": int "sentence":[str,...],"intent_id":[int,...]}]}
        """
        with open(path, encoding='utf-8') as f:
            data = f.read()
        data = json.loads(data)
        return data
