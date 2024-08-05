import pickle
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
import pandas as pd

class ManufacturingStageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manufacturing Stage")
        self.setWindowIcon(QIcon("resources/A3-favicon.png"))
        self.setFixedSize(400,500)
        layout = QVBoxLayout(self)

        # Load the pickled model
        self.model = self.load_model()

        # Text for Manufacturing Stage page
        manufacturing_text = QLabel(
            """Provide the following information to estimate emissions:
            
1. Select manufacturing equipment/machinery.
2. Enter quantity.
3. Enter fuel consumption rate.
4. Enter hours of operation.
5. Enter carbon emission factor.
            """, self)
        layout.addWidget(manufacturing_text)

        # Create the form layout
        form_layout = QFormLayout()

        # Create widgets for the form
        self.equipment_combo = QComboBox()
        self.equipment_combo.addItems(['Excavator', 'Bulldozer', 'Crane'])  # Example items

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Enter quantity')

        self.fuel_consumption_input = QLineEdit()
        self.fuel_consumption_input.setPlaceholderText('Enter fuel consumption')

        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Enter hours of operation')

        self.carbon_factor_input = QLineEdit()
        self.carbon_factor_input.setPlaceholderText('Enter carbon emission factor')

        # Add form widgets to the form layout
        form_layout.addRow('Manufacturing Equipment:', self.equipment_combo)
        form_layout.addRow('Quantity:', self.quantity_input)
        form_layout.addRow('Fuel Consumption Rate:', self.fuel_consumption_input)
        form_layout.addRow('Hours of Operation:', self.hours_input)
        form_layout.addRow('Carbon Emission Factor:', self.carbon_factor_input)

        # Create a button and connect it to the predict method
        predict_button = QPushButton('Predict')
        predict_button.clicked.connect(self.predict)  # Connect button to predict method
        form_layout.addRow(predict_button)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Label for displaying results
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def load_model(self):
        # Load the pickled model from file
        model_path = 'models/Gradient-Boosting-A3.pkl'  # Path to your model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model

    def predict(self):
        # Get the input values
        equipment = self.equipment_combo.currentText()
        quantity = self.quantity_input.text()
        fuel_consumption = self.fuel_consumption_input.text()
        hours = self.hours_input.text()
        carbon_factor = self.carbon_factor_input.text()

        if not quantity or not fuel_consumption or not hours or not carbon_factor:
            QMessageBox.warning(self, "Input Error", "Please provide all numeric inputs.")
            return

        try:
            quantity = float(quantity)
            fuel_consumption = float(fuel_consumption)
            hours = float(hours)
            carbon_factor = float(carbon_factor)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity, Fuel Consumption, Hours of Operation, and Carbon Emission Factor must be numeric.")
            return

        # Convert categorical input to numerical
        equipment_mapping = {'Excavator': 0, 'Bulldozer': 1, 'Crane': 2}
        equipment_num = equipment_mapping.get(equipment, -1)

        if equipment_num == -1:
            QMessageBox.warning(self, "Input Error", "Invalid equipment type selected.")
            return

        # Prepare the feature vector
        features = pd.DataFrame({
            'Manufacturing_equipment': [equipment_num],
            'Quantity': [quantity],
            'Fuel_consumption_rate': [fuel_consumption],
            'Hours_of_operation': [hours],
            'Carbon_emission_factor': [carbon_factor]
        })

        # Perform prediction
        try:
            prediction = self.model.predict(features)[0]
            self.result_label.setText(f"Predicted Emission: {prediction:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"An error occurred during prediction: {str(e)}")
