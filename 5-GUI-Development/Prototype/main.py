import pickle
import numpy as np

# Load the trained model and preprocessing pipeline if available
with open('Gradient-Boosting-A1.pkcls', 'rb') as model_file:
    model = pickle.load(model_file)

# Load or define the preprocessing pipeline or feature encoding map
# For this example, we'll define a simple encoding map for demonstration
encoding_map = {
    'cement': 0,
    'wood': 1,
    'steel': 2
}

# Define the number of binary features expected by the model
# This should match the number of features in the model (e.g., 102)
total_features = 102

# Function to encode categorical feature and initialize feature vector
def prepare_features(categorical_value, numeric_features):
    feature_vector = np.zeros(total_features)  # Initialize all features to 0
    
    # Encode and set the categorical feature
    if categorical_value in encoding_map:
        categorical_index = encoding_map[categorical_value]
        feature_vector[categorical_index] = 1  # Set the correct binary feature to 1
    
    # Set the numeric features (assuming they are placed at the end of the feature vector)
    if len(numeric_features) == 2:
        feature_vector[-2] = numeric_features[0]
        feature_vector[-1] = numeric_features[1]
    
    return feature_vector

# Get user input
try:
    categorical_value = input("Enter the type of raw material (e.g., 'cement', 'wood', 'steel'): ")
    numeric_feature1 = float(input("Enter the mass used: "))
    numeric_feature2 = float(input("Enter the carbon emission factor: "))
except ValueError as e:
    print(f"Invalid input: {e}")
    exit()

# Prepare the feature vector
user_input = prepare_features(categorical_value, [numeric_feature1, numeric_feature2])

# Perform prediction
try:
    prediction = model.predict([user_input])
    print(f"Prediction: {prediction}")
except Exception as e:
    print(f"An error occurred during prediction: {e}")
