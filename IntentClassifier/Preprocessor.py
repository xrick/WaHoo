import random
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from IntentClassifier.Tokenizer import Tokenizer


class Preprocessor:
    def __init__(self):
        self._featurizer = TfidfVectorizer(
            tokenizer=lambda x: Tokenizer.cut(x))

    @classmethod
    def validate_dataset(cls, data_set):
        """        
        Arguments:
            data_set {[dict]}
        """
        assert 'dataset' in data_set
        assert type(data_set['dataset']) == list
        for domain in data_set['dataset']:
            assert 'domain_name' in domain
            assert type(domain['domain_name']) == str
            assert 'sentences' in domain
            assert type(domain['sentences']) == list
            assert 'intent_id' in domain
            assert type(domain['intent_id']) == list
            assert len(domain['sentences']) == len(domain['intent_id'])

    @classmethod
    def get_domain_data_with_noise(cls, data_set, domain_name):
        """Get specific domain data with noise which obtain from other domains.

        Arguments:
            data_set {dict} -- {'domain_name': str, 'sentences': list of str, 'intent_id', list of int}
            domain_name {[str]} -- specific domain
        """
        def get_domain_data(data_set, domain_name):
            return list(next((zip(data['sentences'], data['intent_id'])
                              for data in data_set['dataset'] if data['domain_name'] == domain_name), []))

        def get_noise_data(domain_data, domain_name, max_len):
            noise_pairs = [(sentence, 0)
                           for data in data_set['dataset'] if data['domain_name'] != domain_name
                           for sentence in data['sentences']]

            if len(noise_pairs) > max_len:
                noise_pairs = random.sample(noise_pairs, k=max_len)
            return noise_pairs

        domain_data = get_domain_data(data_set, domain_name)
        noise_data = get_noise_data(
            data_set, domain_name, len(domain_data))
        return domain_data + noise_data

    @classmethod
    def normalize_labels(cls, label_list):
        """normalize label list, for example:[0,2,100,100]->[0,1,2,2],{0:0, 1:2, 2:100}
        
        Arguments:
            label_list {list} -- list of int
        Return:
            list, dict
        """
        def reverse_dict_key_value(input_dict):
            return  {vaule : key for key, vaule in input_dict.items()}

        processed_label_list = []
        intent_id_label_mapping = {}
        label_intent_id_mapping = {}

        if label_list:
            intent_id_label_mapping[0] = 0
            label_index = 1
            for label in label_list:
                if label not in intent_id_label_mapping:
                    intent_id_label_mapping[label] = label_index
                    label_index += 1
                processed_label_list.append(intent_id_label_mapping[label])
            label_intent_id_mapping = reverse_dict_key_value(intent_id_label_mapping)

        return np.asarray(processed_label_list), label_intent_id_mapping

    def fit_transform_featurizer(self, sentences):
        return self._featurizer.fit_transform(
            sentences)

    def transform(self, sentences):
        return self._featurizer.transform(
            sentences)
