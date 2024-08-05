import sys
import pickle
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox
)

# Load the saved model
with open('Gradient-Boosting-A1.pkl', 'rb') as file:
    pipeline = pickle.load(file)

class PredictionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prediction App")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.form_layout = QFormLayout()

        # Create input fields
        self.raw_material_combo = QComboBox()
        self.raw_material_combo.addItems(['Material1', 'Material2', 'Material3'])  # Replace with your categories

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText("Enter mass used")

        self.carbon_input = QLineEdit()
        self.carbon_input.setPlaceholderText("Enter carbon emission factor")

        # Create buttons and labels
        self.predict_button = QPushButton("Predict")
        self.result_label = QLabel("Prediction will appear here")

        self.predict_button.clicked.connect(self.make_prediction)

        # Add widgets to layout
        self.form_layout.addRow("Raw Material:", self.raw_material_combo)
        self.form_layout.addRow("Mass Used:", self.mass_input)
        self.form_layout.addRow("Carbon Emission Factor:", self.carbon_input)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.predict_button)
        self.layout.addWidget(self.result_label)

    def make_prediction(self):
        try:
            # Get user inputs
            raw_material = self.raw_material_combo.currentText()
            mass_used = float(self.mass_input.text())
            carbon_emission_factor = float(self.carbon_input.text())

            # Create input DataFrame
            input_data = pd.DataFrame({
                'Raw_material': [raw_material],
                'Mass_used': [mass_used],
                'Carbon_emission_factor': [carbon_emission_factor]
            })

            # Make prediction
            prediction = pipeline.predict(input_data)[0]
            self.result_label.setText(f"Predicted Value: {prediction:.2f}")

        except ValueError:
            self.result_label.setText("Please enter valid numeric values.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PredictionApp()
    window.show()
    sys.exit(app.exec())
