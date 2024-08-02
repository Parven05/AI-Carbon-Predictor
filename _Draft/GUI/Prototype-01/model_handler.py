import pickle
import numpy as np
from Utils.feature_preparation import prepare_features

class ModelHandler:
    def __init__(self, model_path, total_features):
        self.total_features = total_features
        self.model = self.load_model(model_path)
        
    def load_model(self, model_path):
        with open(model_path, 'rb') as model_file:
            return pickle.load(model_file)
        
    def predict(self, categorical_value, numeric_features, encoding_map):
        feature_vector = prepare_features(categorical_value, numeric_features, encoding_map, self.total_features)
        return self.model.predict([feature_vector])
