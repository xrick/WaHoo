import sys
import unittest
from unittest.mock import Mock
from unittest.mock import patch


sys.path.append('.')
from Preprocessor.SynonymPreprocessor import SynonymPreprocessor


class SynonymPreprocessorTest(unittest.TestCase):

    def test_process_empty_synonym_dic_return_same(self):
        with patch.object(SynonymPreprocessor, "_get_gloabl_synonym_list", lambda x: []):
            synonym_preprocessor = SynonymPreprocessor()
        test_input = 'test_input'
        result = synonym_preprocessor.process(test_input)
        self.assertEqual(result, test_input)

    def test_process_replace_word_one(self):
        with patch.object(SynonymPreprocessor, "_get_gloabl_synonym_list", lambda x: [('問題','問句')]):
            synonym_preprocessor = SynonymPreprocessor()
        test_input = '測試問句'
        result = synonym_preprocessor.process(test_input)
        self.assertEqual(result, '測試問題')


if __name__ == '__main__':
    unittest.main()
