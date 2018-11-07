import unittest
import numpy as np
from unittest.mock import Mock

from IntentClassifier.Preprocessor import Preprocessor


class IntentPreprocessor(unittest.TestCase):
    def test_validate_dataset_input_lack_dataset_raise_error(self):
        test_dict = {}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_input_dataset_is_not_a_list_raise_error(self):
        test_dict = {'dataset': ''}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_domain_lack_domain_name_raise_error(self):
        test_dict = {'dataset': [{"sentences": [], "intent_id":[]}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_domain_name_is_not_str_raise_error(self):
        test_dict = {'dataset': [
            {"domain_name": 0, "sentences": [], "intent_id":[]}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_domain_lack_sentences_raise_error(self):
        test_dict = {'dataset': [{"domain_name": 'test', "intent_id": []}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_sentences_is_not_a_list_raise_error(self):
        test_dict = {'dataset': [
            {"domain_name": 'test', "sentences": 0, "intent_id": []}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_domain_lack_intent_id_raise_error(self):
        test_dict = {'dataset': [{"domain_name": 'test', "sentences": []}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_validate_dataset_intent_id_is_not_a_list_raise_error(self):
        test_dict = {'dataset': [
            {"domain_name": 'test', "sentences": [], "intent_id": 0}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)\


    def test_validate_dataset_sentences_and_intent_id_len_are_not_equal_raise_error(self):
        test_dict = {'dataset': [
            {"domain_name": 'test', "sentences": ['test'], "intent_id": []}]}
        self.assertRaises(
            AssertionError, Preprocessor.validate_dataset, test_dict)

    def test_fit_transform_featurizer_correct_dataset_should_call_fit_transform(self):
        test_obj = Preprocessor()
        test_obj._featurizer.fit_transform = Mock()
        test_sentences = ['test']
        test_obj.fit_transform_featurizer(test_sentences)
        test_obj._featurizer.fit_transform.assert_called_once()

    def test_transform_should_call_transform(self):
        test_obj = Preprocessor()
        test_obj._featurizer.transform = Mock()
        test_sentences = ['test']
        test_obj.transform(test_sentences)
        test_obj._featurizer.transform.assert_called_once()

    def test_get_domain_data_with_noise_domain_data_none_should_return_empty_list(self):
        test_domain_name = 'test_domain'
        test_dataset = {'dataset': [
            {"domain_name": test_domain_name, "sentences": [], "intent_id": []}]}
        result = Preprocessor.get_domain_data_with_noise(test_dataset, test_domain_name)
        self.assertEqual(len(result), 0)

    def test_get_domain_data_with_noise_3_domain_data_should_return_list_with_noise(self):
        test_domain_name = 'test_domain'
        test_dataset = {'dataset': [
            {"domain_name": test_domain_name, "sentences": ['test_sentence_1'], "intent_id": [1]},
            {"domain_name": 'test_domain_2', "sentences": ['test_sentence_2', 'test_sentence_21'], "intent_id": [2, 21]},
            {"domain_name": 'test_domain_3', "sentences": ['test_sentence_3'], "intent_id": [3]}]}
        result = Preprocessor.get_domain_data_with_noise(test_dataset, test_domain_name)
        self.assertEqual(len(result), 2)
    
    def test_normalize_label_None_should_return_empty_ndarray_and_empty_dict(self):
        label_list = None
        result_ndarray, result_dict = Preprocessor.normalize_labels(label_list)
        self.assertEqual(type(result_ndarray), np.ndarray)
        self.assertEqual(len(result_ndarray), 0)
        self.assertEqual(type(result_dict), dict)
        self.assertEqual(len(result_dict), 0)

    def test_normalize_label_empty_list_should_return_empty_nparray_and_empty_dict(self):
        label_list = []
        result_ndarray, result_dict = Preprocessor.normalize_labels(label_list)
        self.assertEqual(type(result_ndarray), np.ndarray)
        self.assertEqual(len(result_ndarray), 0)
        self.assertEqual(type(result_dict), dict)
        self.assertEqual(len(result_dict), 0)
    
    def test_normalize_label_list_contains_0_and_other_should_return_expected_ndarray_and_dict(self):
        label_list = [0, 1001, 1001]
        result_ndarray, result_dict = Preprocessor.normalize_labels(label_list)
        self.assertEqual(type(result_ndarray), np.ndarray)
        expected_list = [0, 1, 1]
        result_list = list(result_ndarray)
        expected_dic = {0:0, 1:1001}
        self.assertDictEqual(result_dict, expected_dic)

if __name__ == '__main__':
    unittest.main()
