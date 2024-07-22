import pickle
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class PredictionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the trained model
        with open('Gradient-Boosting-A1.pkcls', 'rb') as model_file:
            self.model = pickle.load(model_file)
        
        # Define the encoding map
        self.encoding_map = {
            'cement': 0,
            'wood': 1,
            'steel': 2
        }
        
        # Define the number of binary features
        self.total_features = 102
        
        # Set up the GUI
        self.setWindowTitle('Prediction App')
        self.setGeometry(100, 100, 400, 300)
        
        # Create main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title Label
        self.title_label = QLabel('A1 Production Prediction')
        self.title_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Create and add widgets
        self.categorical_dropdown = QComboBox()
        self.categorical_dropdown.addItems(['cement', 'wood', 'steel'])
        self.categorical_dropdown.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        layout.addWidget(self.categorical_dropdown)
        
        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used')
        self.mass_input.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        layout.addWidget(self.mass_input)
        
        self.emission_input = QLineEdit()
        self.emission_input.setPlaceholderText('Enter carbon emission factor')
        self.emission_input.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        layout.addWidget(self.emission_input)
        
        self.predict_button = QPushButton('Predict')
        self.predict_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px; font-size: 16px;")
        self.predict_button.clicked.connect(self.predict)
        layout.addWidget(self.predict_button)
        
        self.result_label = QLabel('')
        self.result_label.setStyleSheet("font-size: 16px;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Set layout and widget
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
    
    def prepare_features(self, categorical_value, numeric_features):
        feature_vector = np.zeros(self.total_features)
        if categorical_value in self.encoding_map:
            categorical_index = self.encoding_map[categorical_value]
            feature_vector[categorical_index] = 1
        if len(numeric_features) == 2:
            feature_vector[-2] = numeric_features[0]
            feature_vector[-1] = numeric_features[1]
        return feature_vector

    def predict(self):
        try:
            categorical_value = self.categorical_dropdown.currentText()
            numeric_feature1 = float(self.mass_input.text())
            numeric_feature2 = float(self.emission_input.text())
            
            user_input = self.prepare_features(categorical_value, [numeric_feature1, numeric_feature2])
            prediction = self.model.predict([user_input])
            self.result_label.setText(f"Prediction: {prediction[0]}")
        except ValueError as e:
            self.result_label.setText(f"Invalid input: {e}")

if __name__ == '__main__':
    app = QApplication([])
    window = PredictionApp()
    window.show()
    app.exec()
