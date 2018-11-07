import numpy as np

from IntentClassifier.Preprocessor import Preprocessor
from sklearn.linear_model import SGDClassifier
from config import LOG_REG_ARGS

class LogisticRegressionClassfier:
    def __init__(self):
        self._preprocessor = Preprocessor()
        self._classifier = SGDClassifier(**LOG_REG_ARGS)
        self._label_intent_id_mapping = {}
    
    def fit(self, data_pair):
        """train LogisticRegressionClassfier
        
        Arguments:
            data_pair {list} -- list of tuple
        """
        features, labels = zip(*data_pair)    
        features, labels = list(features), list(labels)
        processed_features = self._preprocessor.fit_transform_featurizer(features)
        processed_lables, self._label_intent_id_mapping = Preprocessor.normalize_labels(labels)
        self._classifier.fit(processed_features, processed_lables)
    
    def predict(self, input):
        processed_input = self._preprocessor.transform([input])
        result = self._classifier.predict_proba(processed_input)
        intent_id, prob = self._postprocess(result)
        return intent_id, prob
    
    def _postprocess(self, input):
        max_probability_label_index = int(np.argmax(input[0]))
        max_probability = input[0][max_probability_label_index]
        intent_id = self._label_intent_id_mapping[max_probability_label_index]
        return intent_id, max_probability
