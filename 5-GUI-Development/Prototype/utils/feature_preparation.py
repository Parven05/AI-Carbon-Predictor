import numpy as np

def prepare_features(categorical_value, numeric_features, encoding_map, total_features):
    feature_vector = np.zeros(total_features)
    if categorical_value in encoding_map:
        categorical_index = encoding_map[categorical_value]
        feature_vector[categorical_index] = 1
    if len(numeric_features) == 2:
        feature_vector[-2] = numeric_features[0]
        feature_vector[-1] = numeric_features[1]
    return feature_vector
