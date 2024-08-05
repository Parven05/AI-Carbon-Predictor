import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
import pandas as pd

class ProductionStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Production Stage")
        self.setWindowIcon(QIcon("resources/A1-favicon.png"))
        self.setFixedSize(400,400)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Production Stage page
        production_stage_text = QLabel(
            """Provide the following information to estimate emissions:
            
1. Select Raw material type.
2. Enter mass used (kg) | Recommnded: 50 - 2000 (kg).
3. Enter carbon emission factor (kgCO2/kg).
            """, self)
        layout.addWidget(production_stage_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.material_combo = QComboBox()
        self.material_combo.addItems(['Wood', 'Steel', 'Concrete'])  # Example items

        self.mass_input = QLineEdit()
        self.mass_input.setPlaceholderText('Enter mass used (kg)')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter emission factor (kgCO2/kg)')

        # Add form widgets to the form layout
        form_layout.addRow('Raw Material Type:', self.material_combo)
        form_layout.addRow('Mass Used:', self.mass_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button
        predict_button = QPushButton('Predict Total Carbon Emission')
        predict_button.clicked.connect(self.predict)
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A1.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def predict(self):
        # Get the input values
        material = self.material_combo.currentText()
        mass = self.mass_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not mass or not carbon_factor:
            QMessageBox.warning(self, "Input Error", "Please provide all numeric inputs.")
            return

        try:
            mass = float(mass)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Mass and Carbon Emission Factor must be numeric.")
            return

        # Convert categorical input to numerical
        material_mapping = {'Wood': 0, 'Steel': 1, 'Concrete': 2}
        material_num = material_mapping.get(material, -1)

        if material_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid material type selected.")
            return

        # Prepare the feature vector
        features = pd.DataFrame({
            'Raw_material': [material_num],
            'Mass_used': [mass],
            'Carbon_emission_factor': [carbon_factor]
        })

        # Perform prediction
        try:
            prediction = self.model.predict(features)[0]
            self.result_label.setText(f"Predicted Total Carbon Emission: {prediction:.2f} kgCo2e")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")

